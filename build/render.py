"""Writes the VPython course site from the session files.

The HTML is generated. Edit sessions_a.py, sessions_b.py, sessions_c.py and
standards.py, not the HTML. Every snippet with a "run" key is executed through
vpython_harness.py against the installed vpython library with no browser, and the
captured terminal output is what the pages show. Set VPY_SRC to a source checkout
of vpython-jupyter on a machine with no vpython wheel for its Python.

Look and structure follow the Lecture Light style of the beginner course: light
ground for a projector, near-black text, three accents, no hairlines, code
coloured by role the way VS Code's Light+ theme does it.
"""

import html
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from standards import STANDARDS, RESOLVED_ON, CONNECTOR
from highlight import highlight
from sessions_a import SESSIONS_A
from sessions_b import SESSIONS_B
from sessions_c import SESSIONS_C

SESSIONS = SESSIONS_A + SESSIONS_B + SESSIONS_C
COURSE = "Python in 3D"
HUB = "vpython_course_hub"
LEDGER = "vpython_ledger_card"
STDMAP = "standards_map"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get("VPL_OUT", ROOT)
VERSION = "4"
TMP = os.environ.get("VPL_TMP",
                     os.path.join(tempfile.gettempdir(), "vpython_lesson_build"))
HARNESS = os.path.join(HERE, "vpython_harness.py")

os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

VERIFY_LOG = []


# ---------------------------------------------------------------- verification

def run_snippet(code, maxf, inject, fname, timeout=60):
    path = os.path.join(TMP, fname)
    with open(path, "w") as fh:
        fh.write(code)
    try:
        proc = subprocess.run(
            [sys.executable, HARNESS, path, str(maxf), json.dumps(inject)],
            capture_output=True, text=True, timeout=timeout, cwd=TMP,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    out = proc.stdout
    err = proc.stderr.replace(TMP + "/", "").replace(TMP, "")
    if err.strip():
        trimmed = "\n".join(ln.rstrip() for ln in err.rstrip().splitlines() if ln.strip())
        if out.strip():
            return out.rstrip() + "\n" + trimmed, proc.returncode
        return trimmed, proc.returncode
    return out.rstrip(), proc.returncode


def student_file(num):
    return "Jonathan_vpython%02d.py" % num


def verify(chunk, tag, num):
    mode = chunk.get("run")
    if mode is None:
        return None, None
    if mode != "vpython":
        raise SystemExit("unknown run mode " + str(mode) + " for " + tag)
    out, rc = run_snippet(chunk["code"], chunk.get("frames", 1),
                          chunk.get("inject", []), student_file(num))
    if out == "TIMEOUT":
        raise SystemExit("snippet timed out: " + tag)
    if rc != 0 and not chunk.get("expect_error"):
        raise SystemExit("snippet " + tag + " ended with an error:\n" + out)
    VERIFY_LOG.append([tag, mode, "rc=" + str(rc), str(len(out.splitlines())) + " lines"])
    return out, mode


def describe_inject(inject):
    """One plain sentence saying what the build script fed in, in pass order."""
    if not inject:
        return ""
    parts = []
    holds = {}
    for item in sorted(inject, key=lambda x: x[0]):
        f, kind = item[0], item[1]
        if kind == "KEYDOWN":
            parts.append((f, "the " + key_name(item[2]) + " key pressed on pass " + str(f)))
        elif kind == "HOLD":
            holds.setdefault(item[2], []).append(f)
        elif kind in ("CLICK", "MOUSEDOWN", "MOUSEMOVE", "MOUSEUP"):
            p = item[2]
            what = {"CLICK": "a click", "MOUSEDOWN": "the button pressed",
                    "MOUSEMOVE": "the mouse moved", "MOUSEUP": "the button released"}[kind]
            parts.append((f, what + " at (" + ", ".join(str(v) for v in p) + ") on pass " + str(f)))
        elif kind == "WIDGET":
            fn = item[2]
            val = item[3] if len(item) > 3 else None
            if val is None or val == 0 and len(item) == 3:
                parts.append((f, "the widget bound to " + fn + " clicked on pass " + str(f)))
            else:
                parts.append((f, "the widget bound to " + fn + " set to " + str(val)
                              + " on pass " + str(f)))
    for key, frames in holds.items():
        frames = sorted(frames)
        runs = []
        for f in frames:
            if runs and f == runs[-1][-1] + 1:
                runs[-1].append(f)
            else:
                runs.append([f])
        for run in runs:
            if len(run) == 1:
                parts.append((run[0], "the " + key_name(key) + " key held on pass " + str(run[0])))
            else:
                parts.append((run[0], "the " + key_name(key) + " key held on passes "
                              + str(run[0]) + " to " + str(run[-1])))
    parts.sort(key=lambda x: x[0])
    return "Fed in by the build script: " + ", ".join(p[1] for p in parts) + "."


def key_name(k):
    names = {"left": "left arrow", "right": "right arrow", "up": "up arrow",
             "down": "down arrow", " ": "space"}
    return names.get(k, k)


# ---------------------------------------------------------------------- styling

CSS = """
/* Lecture Light: built for a projector in a room with the lights on.
   Light ground, near-black text, few accents, no hairlines. */
:root{
  --paper:#F4F0E6;
  --card:#FFFDF7;
  --ink:#17181B;
  --ink-soft:#4A4D53;
  --rule:#D3CBB8;
  --teal:#0E4D52;
  --teal-deep:#0A3A3E;
  --clay:#9C2B22;
  --ochre:#8A5A00;
  --ochre-line:#D99B12;
  --ochre-tint:#FBF2DC;
  --green:#1D5B39;
  --green-tint:#E8F1E9;
  --green-ink:#122B1C;
  --code-bg:#EDE7D9;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'DM Sans',system-ui,sans-serif; font-size:18px; font-weight:500;
  line-height:1.65;
}
header.top{
  background:var(--teal); color:#FFFDF7;
  border-bottom:6px solid var(--ochre-line); padding:30px 22px 26px;
}
.wrap{max-width:900px; margin:0 auto}
.eyebrow{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.14em;
  text-transform:uppercase; color:#F2D89B; margin:0 0 10px; font-weight:700;
}
h1{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:800;
  font-size:clamp(29px,4.8vw,44px); line-height:1.1; margin:0 0 10px;
}
h2{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:25px; line-height:1.2; margin:0 0 12px; color:var(--teal-deep);
}
h3{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:20px; margin:0 0 8px; color:var(--teal-deep);
}
header.top h1,header.top h2{color:#FFFDF7}
.sub{color:#EAE3D2; margin:0 0 16px; font-size:19px; font-weight:400}
.dates{
  display:flex; flex-wrap:wrap; gap:10px; margin-top:16px;
  font-family:'JetBrains Mono',monospace; font-size:13.5px;
}
.pill{
  border:2px solid rgba(255,253,247,.4); border-radius:999px; padding:5px 13px;
  background:rgba(255,253,247,.08);
}
.pill b{color:#F2D89B; font-weight:700}
main{padding:28px 22px 12px}
section{
  background:var(--card); border:2px solid var(--rule); border-radius:6px;
  padding:22px 24px; margin:0 0 20px;
}
section.opener{border-left:8px solid var(--green)}
section.chunk{border-left:8px solid var(--ochre-line)}
section.hinge{border-left:8px solid var(--clay)}
section.brief{border-left:8px solid var(--teal)}
.chunk-no{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ochre); margin:0 0 8px; font-weight:700;
}
p{margin:0 0 14px}
ul,ol{margin:0 0 14px; padding-left:24px}
li{margin:0 0 8px}
code,pre{
  /* JetBrains Mono ligatures turn != into a slashed equals and <= into a single
     glyph; students then type a character that does not exist. Keep every
     operator as the keys that produce it. */
  font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0,"dlig" 0;
}
code{
  font-family:'JetBrains Mono',monospace; font-size:.9em; font-weight:700;
  background:var(--code-bg); color:#1E2A2B;
  padding:2px 6px; border-radius:3px;
}
pre{
  font-family:'JetBrains Mono',monospace; font-size:15.5px; line-height:1.6;
  background:var(--code-bg); color:var(--ink); border:2px solid var(--rule);
  border-left:6px solid #B9AF96; border-radius:4px;
  padding:16px 18px; overflow-x:auto; margin:0 0 16px; font-weight:500;
}
/* Code colours by role, from VS Code's Light+ theme. Four are darkened within the same
   hue so every one clears 4.5:1 on the code background. Colour only, never bold or
   italic, so every character keeps its width. */
.tk-ctl{color:#9A00C2}  /* control words: if elif else for while return import */
.tk-kw{color:#0000FF}   /* def, class, and, or, not, True, False, None, f-string parts */
.tk-str{color:#A31515}  /* strings */
.tk-num{color:#06704A}  /* numbers */
.tk-com{color:#3B6E2A}  /* comments */
.tk-fn{color:#795E26}   /* functions */
.tk-cls{color:#1D6A80}  /* classes, types, modules */
.tk-var{color:#001080}  /* variables */
pre.anatomy{background:#FFFDF7; border-left:6px solid var(--teal)}
pre.anatomy .cond{background:#FBF2DC; border-bottom:3px solid var(--ochre-line); padding:1px 2px}
pre.anatomy .blk{background:#E8F1E9; border-left:3px solid var(--green); padding:1px 2px}
pre.anatomy .nm{background:#E3EDEE; border-bottom:3px solid var(--teal); padding:1px 2px}
pre.anatomy .arg{background:#F7E4E1; border-bottom:3px solid var(--clay); padding:1px 2px}
pre.anatomy .lbl{color:var(--ink-soft); font-weight:700}
pre.anatomy .lbl-n{color:var(--teal)}
pre.anatomy .lbl-a{color:var(--clay)}
.legend i.n{background:#E3EDEE; border-bottom:3px solid var(--teal)}
.legend i.a{background:#F7E4E1; border-bottom:3px solid var(--clay)}
pre.anatomy .lbl-c{color:var(--ochre)}
pre.anatomy .lbl-b{color:var(--green)}
.legend{display:flex; flex-wrap:wrap; gap:10px 22px; font-size:16px; margin:0 0 16px}
.legend span{display:inline-flex; align-items:center; gap:8px; margin-right:18px}
.legend i{display:inline-block; width:22px; height:16px; border-radius:2px; margin-right:8px}
.legend i.c{background:#FBF2DC; border-bottom:3px solid var(--ochre-line)}
.legend i.b{background:#E8F1E9; border-left:3px solid var(--green)}
pre.out{
  background:var(--green-tint); border-color:#A9C6B2;
  border-left:6px solid var(--green); color:var(--green-ink);
}
.outlabel{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--green); margin:0 0 7px; font-weight:700;
}
.predict{
  border:2px dashed var(--ochre); border-radius:5px;
  padding:16px 18px; margin:0 0 16px; background:var(--ochre-tint);
}
.predict p{margin:0 0 12px}
.predict .q{font-weight:700}
button.rev{
  font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700;
  background:var(--teal); color:#FFFDF7; border:0; border-radius:4px;
  padding:10px 18px; cursor:pointer;
}
button.rev:hover{background:var(--teal-deep)}
button.rev.hint{background:var(--card); color:var(--ochre); border:2px solid var(--ochre-line); margin:0 10px 10px 0}
button.rev.hint:hover{background:var(--ochre-tint)}
.hints .ans{margin:0 0 12px; padding-top:10px; border-top:2px solid var(--ochre-line)}
.ans{display:none; margin-top:16px; padding-top:16px; border-top:2px solid var(--rule)}
.ans.open{display:block}
table{border-collapse:collapse; width:100%; margin:0 0 16px; font-size:16.5px}
th,td{border:2px solid var(--rule); padding:9px 11px; text-align:left; vertical-align:top}
th{background:#EFE9DA; font-weight:700; font-size:15px; color:var(--teal-deep)}
td.fill{background:#FBF9F3; min-width:100px}
.exits{display:grid; gap:14px; grid-template-columns:1fr}
@media(min-width:760px){.exits{grid-template-columns:repeat(3,1fr)}}
.exit{border:2px solid var(--rule); border-radius:5px; padding:16px}
.exit .tag{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; margin:0 0 8px; font-weight:700;
}
.exit.floor{border-top:6px solid var(--green)}
.exit.floor .tag{color:var(--green)}
.exit.middle{border-top:6px solid var(--ochre-line)}
.exit.middle .tag{color:var(--ochre)}
.exit.stretch{border-top:6px solid var(--clay)}
.exit.stretch .tag{color:var(--clay)}
details.teacher{
  background:var(--card); border:2px solid var(--rule);
  border-left:8px solid var(--clay); border-radius:6px;
  padding:18px 22px; margin:0 0 20px;
}
details.teacher summary{
  cursor:pointer; font-family:'Bricolage Grotesque','DM Sans',sans-serif;
  font-weight:700; font-size:21px; color:var(--clay);
}
details.teacher[open] summary{margin-bottom:14px}
.note{
  font-size:16.5px; color:var(--ink-soft); border-left:4px solid var(--rule);
  padding-left:14px; margin:0 0 14px;
}
.pager{
  max-width:900px; margin:0 auto; padding:8px 22px 34px;
  display:flex; justify-content:space-between; gap:12px;
  font-family:'JetBrains Mono',monospace; font-size:14px;
}
.pager a{
  color:var(--teal); text-decoration:none; font-weight:700;
  border:2px solid var(--rule); background:var(--card);
  border-radius:4px; padding:10px 14px;
}
.pager a:hover{background:#EFE9DA}
footer{
  background:#EAE4D5; border-top:4px solid var(--teal); padding:22px 22px 36px;
  font-size:15px; color:var(--ink-soft);
}
footer a{color:var(--teal); font-weight:700}
a{color:var(--teal)}
.toolbar{display:flex; gap:12px; flex-wrap:wrap; margin:0 0 20px}
a.btn{
  display:inline-block; font-family:'DM Sans',sans-serif; font-size:17px; font-weight:700;
  background:var(--teal); color:#FFFDF7; text-decoration:none; border-radius:4px;
  padding:12px 20px; border:2px solid var(--teal);
}
a.btn:hover{background:var(--teal-deep)}
a.btn.quiet{background:var(--card); color:var(--teal)}
a.btn.quiet:hover{background:#EFE9DA}
.grid2{display:grid; gap:16px; grid-template-columns:1fr}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}}
.card{border:2px solid var(--rule); border-radius:5px; padding:16px; background:#FFFDF7}
.card h3{margin-bottom:8px}
.sessionlist{list-style:none; padding:0; margin:0}
.sessionlist li{
  border:2px solid var(--rule); border-left:8px solid var(--teal);
  border-radius:5px; margin:0 0 12px; padding:14px 16px;
  display:flex; gap:16px; align-items:flex-start; background:#FFFDF7;
}
.sessionlist .n{
  font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:700;
  color:var(--teal); min-width:38px;
}
.sessionlist a{font-weight:700; text-decoration:none; font-size:19px}
.sessionlist .meta{
  font-family:'JetBrains Mono',monospace; font-size:13px; color:var(--ink-soft);
  display:block; margin-top:4px;
}
.bonus{border-left-color:var(--clay)}
.bonus .n{color:var(--clay)}
.flag{
  background:#F7E4E1; border:2px solid var(--clay); border-left:8px solid var(--clay);
  border-radius:5px; padding:14px 16px; margin:0 0 18px; font-size:16.5px;
  color:#3A1512;
}
.stamp{
  border:3px dashed #BFB49A; border-radius:5px; padding:14px;
  font-size:15px; min-height:100px; background:#FFFDF7;
}
.stampgrid{display:grid; gap:12px; grid-template-columns:1fr 1fr}
@media(min-width:820px){.stampgrid{grid-template-columns:repeat(3,1fr)}}
.stamp .no{
  font-family:'JetBrains Mono',monospace; color:var(--ochre); font-size:12.5px;
  letter-spacing:.1em; text-transform:uppercase; display:block; margin-bottom:6px;
  font-weight:700;
}
@media print{
  body{background:#fff; font-size:11pt}
  header.top{background:#fff; color:#111; border-bottom:3px solid #111}
  header.top h1,header.top .sub,header.top .eyebrow,.pill b{color:#111}
  .pill{border-color:#666}
  footer,.pager,details.teacher{background:#fff}
  section,.stamp,.card{background:#fff; break-inside:avoid}
  .noprint,.toolbar{display:none}
  a{color:#111}
}
"""

JS = """
document.addEventListener('click', function(e){
  var b = e.target.closest('button.rev');
  if(!b) return;
  var t = document.getElementById(b.getAttribute('data-target'));
  if(!t) return;
  var open = t.classList.toggle('open');
  b.setAttribute('aria-expanded', open ? 'true' : 'false');
  b.textContent = open ? b.getAttribute('data-hide') : b.getAttribute('data-show');
});
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?'
         'family=Bricolage+Grotesque:opsz,wght@12..96,400..800&'
         'family=DM+Sans:wght@400;500;700&'
         'family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">')


def link(slug):
    return slug + ".html?v=" + VERSION


def page(title, body, head_extra=""):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + html.escape(title) + '</title>\n'
        + FONTS + '\n<style>' + CSS + '</style>\n' + head_extra + '</head>\n<body>\n'
        + body +
        '\n<script>' + JS + '</script>\n</body>\n</html>\n'
    )


def code_block(code):
    # Coloured by role, the way VS Code's Light+ theme colours Python. Output boxes
    # (out_block) stay plain: they are output, not code.
    return '<pre>' + highlight(code.rstrip("\n")) + '</pre>'


def out_block(text, label="What actually happens"):
    return ('<p class="outlabel">' + label + '</p><pre class="out">'
            + html.escape(text) + '</pre>')


def hint_buttons(idx, hints):
    """One 'Show hint' button per hint, each with its own hidden block."""
    if not hints:
        return ""
    if isinstance(hints, str):
        hints = [hints]
    out = []
    for k, h in enumerate(hints):
        hid = idx + "-hint" + str(k + 1)
        label = "Show a hint" if len(hints) == 1 else "Show hint " + str(k + 1)
        out.append('<button class="rev hint" data-target="' + hid + '" aria-controls="' + hid + '" '
                   'aria-expanded="false" data-show="' + label + '" '
                   'data-hide="Hide the hint">' + label + '</button>'
                   '<div class="ans" id="' + hid + '"><p>' + h + '</p></div>')
    return '<div class="hints">' + "".join(out) + '</div>'


def reveal(idx, question, answer, qlabel="Predict", extra="",
           show="Show the answer", hide="Hide the answer", hints=None):
    return (
        '<div class="predict"><p class="q">' + qlabel + ': ' + question + '</p>'
        + hint_buttons(idx, hints) +
        '<button class="rev" data-target="' + idx + '" aria-controls="' + idx + '" '
        'aria-expanded="false" data-show="' + show + '" '
        'data-hide="' + hide + '">' + show + '</button>'
        '<div class="ans" id="' + idx + '">' + extra + '<p>' + answer + '</p></div></div>'
    )


def standards_table(codes):
    rows = ""
    for c in codes:
        s = STANDARDS[c]
        rows += ('<tr><td><code>' + c + '</code></td><td>' + s["jurisdiction"]
                 + '</td><td>' + s["framework"] + '</td><td>' + s["grades"]
                 + '</td><td>' + html.escape(s["statement"]) + '</td></tr>')
    return ('<table><tr><th>Code</th><th>Jurisdiction</th><th>Framework</th>'
            '<th>Grade</th><th>Statement</th></tr>' + rows + '</table>')


def output_extra(ch, out, mode, tag):
    """The verified output box, or the note that nothing printed, plus the
    sentence that says what the build script fed in."""
    loops = "while True" in ch["code"]
    fed = describe_inject(ch.get("inject", []))
    extra = ""
    if out:
        lbl = "What it actually prints"
        if mode == "vpython" and loops:
            lbl = ("What it actually prints (run without a browser, quit after "
                   + str(ch.get("frames", 1)) + " passes of the loop)")
        elif mode == "vpython":
            lbl = "What it actually prints (run without a browser)"
        extra = out_block(out, lbl)
    elif mode == "vpython":
        tail = (" and quit after " + str(ch.get("frames", 1)) + " passes of the loop"
                if loops else "")
        extra = ('<p class="note">Nothing printed in the terminal. This was run '
                 'without a browser' + tail + ', and it printed nothing because the '
                 'browser tab is the output. Words go in the terminal, pictures go in '
                 'the tab.</p>')
    if fed:
        extra = extra + '<p class="note">' + fed + '</p>'
    if ch.get("code_a"):
        extra = extra + code_block(ch["code_a"])
    return extra


# ------------------------------------------------- shape settings reference

# Every setting a shape or widget is given by name on the pages. Each session
# page shows the rows for the settings its own code uses, found by scanning the
# code, so the table never falls out of step with the programs.
PARAMS = [
    ("pos", "Where the shape is: three numbers, <code>vec(x, y, z)</code>. x is right, y is up, z is toward you. For a box or a sphere, pos is the middle. For a cylinder, cone, or arrow, pos is one end."),
    ("size", "A box's three measurements, <code>vec(long, tall, deep)</code>: along x, along y, along z. Each starts at 1 if you do not say."),
    ("radius", "How big round a sphere, cylinder, cone, or ring is: the distance from the middle to the edge. The lowest point is the radius below the middle."),
    ("axis", "For a cylinder, cone, or arrow: which way it points and how long it is, as a vector. The far end is at <code>pos + axis</code>. A wheel's axis points sideways, along z, so its round side touches the ground. For <code>rotate</code>: the line the thing turns around."),
    ("angle", "How far <code>rotate</code> turns, always written <code>radians(degrees)</code>. A minus sign turns the other way."),
    ("origin", "For <code>rotate</code>: a point to turn around instead of the shape's own pos, like a moon going around a planet."),
    ("color", "<code>color.red</code>, <code>color.gray(0.4)</code>, or <code>vec(r, g, b)</code> with each number from 0 to 1."),
    ("opacity", "How see-through: 1 is solid, 0 is invisible, 0.5 is glass."),
    ("text", "The words a label, button, or wtext shows."),
    ("height", "For a label: the size of its letters, in pixels."),
    ("box", "For a label: <code>box=False</code> takes away the frame drawn around its words."),
    ("yoffset", "For a label: how many pixels above its pos the words sit."),
    ("bind", "The name of the function to run when a key, click, or widget happens. The name alone, no brackets."),
    ("min", "The smallest number a slider can be set to."),
    ("max", "The biggest number a slider can be set to."),
    ("value", "The number a slider starts at."),
    ("step", "How much a slider moves when it is nudged."),
    ("choices", "The list of words a menu offers."),
    ("normal", "For <code>scene.mouse.project</code>: which way the flat plane faces. <code>vec(0, 1, 0)</code> is a plane facing up, like a floor."),
    ("point", "For <code>scene.mouse.project</code>: one point the flat plane passes through, which sets its height."),
]


def params_section(s):
    codes = [c["code"] for c in s["chunks"]] + [c["code"] for c in s["brief"].get("cards", [])]
    used = set()
    for c in codes:
        used |= set(re.findall(r"\b(\w+)=", c))
    rows = [(k, v) for k, v in PARAMS if k in used]
    if not rows:
        return ""
    b = ['<section><h2>Settings used on this page</h2>'
         '<p>Every shape and widget is made by naming its settings, like '
         '<code>box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1))</code>. These are the '
         'ones the programs on this page use. The name before the <code>=</code> is the '
         'setting, and the value after it is what you give it.</p>'
         '<table><tr><th>Setting</th><th>What it means</th></tr>']
    for k, v in rows:
        b.append('<tr><td><code>' + k + '</code></td><td>' + v + '</td></tr>')
    b.append('</table></section>')
    return "".join(b)


# ---------------------------------------------------------------- session page

def render_session(s, prev_s, next_s):
    n = s["num"]
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; VPython &middot; Session '
             + str(n) + ' of ' + str(len(SESSIONS)) + '</p>')
    b.append('<h1>' + html.escape(s["title"]) + '</h1>')
    b.append('<p class="sub">' + html.escape(s["subtitle"]) + '</p>')
    b.append('<div class="dates">')
    if s.get("date"):
        b.append('<span class="pill"><b>Date</b> ' + html.escape(s["date"]) + '</span>')
    b.append('<span class="pill"><b>Length</b> 90 minutes</span>')
    b.append('<span class="pill"><b>Ages</b> 10 to 11</span>')
    if s["new"]:
        b.append('<span class="pill"><b>New</b> ' + str(len(s["new"])) + ' items</span>')
    else:
        b.append('<span class="pill"><b>New</b> nothing</span>')
    b.append('</div></div></header>')

    b.append('<main><div class="wrap">')

    if s["new"]:
        b.append('<section><h2>What is new today</h2><p>'
                 + ", ".join(html.escape(x) for x in s["new"]) + '.</p>')
    else:
        b.append('<section><h2>What is new today</h2><p>No new syntax. '
                 'Everything today uses what is already on your ledger card.</p>')
    if s["reuse"]:
        b.append('<p><b>Deliberately re-used:</b> ' + html.escape(s["reuse"]) + '.</p>')
    b.append('<p class="note">' + s["reuse_note"] + '</p></section>')

    b.append(params_section(s))

    op = s["opener"]
    b.append('<section class="opener"><p class="chunk-no">Opener &middot; '
             + str(op["minutes"]) + ' minutes</p><h2>' + html.escape(op["title"]) + '</h2>')
    b.append('<p>' + op["body"] + '</p>')
    for i, q in enumerate(op["questions"]):
        if q.get("code"):
            b.append(code_block(q["code"]))
        extra = code_block(q["code_a"]) if q.get("code_a") else ""
        b.append(reveal("s%d-op%d" % (n, i), q["q"], q["a"], "Question", extra))
    b.append('</section>')

    for i, ch in enumerate(s["chunks"]):
        tag = "s%d-c%d" % (n, i + 1)
        out, mode = verify(ch, tag, n)
        b.append('<section class="chunk"><p class="chunk-no">Chunk ' + str(i + 1)
                 + ' of ' + str(len(s["chunks"])) + '</p>')
        b.append('<h2>' + html.escape(ch["title"]) + '</h2>')
        b.append('<p>' + ch["teach"] + '</p>')
        if ch.get("figure"):
            b.append(ch["figure"])
        b.append(code_block(ch["code"]))
        b.append(reveal(tag, ch["predict"], ch["reveal"], "Predict",
                        output_extra(ch, out, mode, tag),
                        "Run it first, then check here", "Hide", ch.get("hint")))
        b.append('</section>')

    for sec in s.get("sections", []):
        b.append('<section><h2>' + html.escape(sec["title"]) + '</h2>' + sec["html"] + '</section>')

    h = s["hinge"]
    m = re.match(r"From session (\d+)", h["q"])
    if m:
        cap = "reaches back to session " + m.group(1)
    elif h["q"].startswith("Pick any stamp"):
        cap = "reaches back across the ledger card"
    else:
        cap = "from today's chunks"
    b.append('<section class="hinge"><p class="chunk-no">Hinge question &middot; '
             + cap + '</p><h2>Before you build</h2>')
    extra = ""
    if h.get("code"):
        b.append(code_block(h["code"]))
    if h.get("code_a"):
        extra = extra + code_block(h["code_a"])
    b.append(reveal("s%d-hinge" % n, h["q"], h["a"], "Question", extra))
    b.append('</section>')

    br = s["brief"]
    b.append('<section class="brief"><p class="chunk-no">Build &middot; '
             + str(br["minutes"]) + ' minutes</p><h2>' + html.escape(br["title"]) + '</h2>')
    if br.get("intro"):
        b.append('<p>' + br["intro"] + '</p>')
    b.append('<ol>')
    for st in br["steps"]:
        b.append('<li>' + st + '</li>')
    b.append('</ol>')
    for j, card in enumerate(br.get("cards", [])):
        tag = "s%d-card%d" % (n, j + 1)
        out, mode = verify(card, tag, n)
        b.append('<h3>' + html.escape(card["title"]) + '</h3>')
        if card.get("teach"):
            b.append('<p>' + card["teach"] + '</p>')
        b.append(code_block(card["code"]))
        b.append(reveal(tag, card["predict"], card["reveal"], "Predict",
                        output_extra(card, out, mode, tag),
                        "Run it first, then check here", "Hide"))
    b.append('<h3>Expected and got</h3>'
             '<p>Fill in the left column before you run. Fill in the right column after.</p>')
    b.append('<table><tr><th>Expected</th><th>Got</th></tr>')
    for row in br["expected_got"]:
        b.append('<tr><td>' + row[0] + '</td><td class="fill"></td></tr>')
    b.append('</table></section>')

    ex = s["exits"]
    b.append('<section><h2>Where you can stop</h2>'
             '<p>All three are real places to stop. Nobody is behind for finishing at the floor.</p>'
             '<div class="exits">')
    b.append('<div class="exit floor"><p class="tag">Floor</p><p>' + ex["floor"] + '</p></div>')
    b.append('<div class="exit middle"><p class="tag">Middle</p><p>' + ex["middle"] + '</p></div>')
    b.append('<div class="exit stretch"><p class="tag">Stretch</p><p>' + ex["stretch"] + '</p></div>')
    b.append('</div></section>')

    b.append('<section><h2>Ledger card</h2><p>' + s["ledger"] + '</p>'
             '<p><a href="' + link(LEDGER) + '">Open the course ledger card</a></p></section>')

    t = s["teacher"]
    b.append('<details class="teacher"><summary>Teacher panel</summary>')
    b.append('<h3>Timing, 90 minutes</h3><ul>')
    for x in t["timing"]:
        b.append('<li>' + html.escape(x) + '</li>')
    b.append('</ul><p class="note">Pacing: most rooms will not reach the end of '
             'the build brief. The exits exist so that stopping there is a finish, not a failure.</p>')
    b.append('<h3>What you will see, and what to do</h3>'
             '<table><tr><th>In the room</th><th>Redirect</th></tr>')
    for m in t["misconceptions"]:
        b.append('<tr><td>' + m[0] + '</td><td>' + m[1] + '</td></tr>')
    b.append('</table>')
    b.append('<h3>Mapped to</h3>')
    b.append(standards_table(t["standards"]))
    lcs = []
    for c in t["standards"]:
        for l in STANDARDS[c]["lcs"]:
            lcs.append((c, l))
    if lcs:
        b.append('<h3>Learning components behind those codes</h3><ul>')
        for c, l in lcs:
            b.append('<li><code>' + c + '</code> ' + html.escape(l) + '</li>')
        b.append('</ul>')
    b.append('<h3>If time runs out</h3><p>' + t["routing"] + '</p>')
    if t.get("setup"):
        b.append('<h3>Setup and how this page was checked</h3><p>' + t["setup"] + '</p>')
    b.append('</details>')

    if s.get("env_note"):
        b.append(env_section(n))

    b.append('</div></main>')
    b.append(pager(prev_s, next_s))
    b.append(footer())
    return page(s["title"], "\n".join(b))


ENV_ONCE = ('Open the terminal in VS Code and install the library: '
            '<code>pip install vpython</code>. Check it worked with '
            '<code>python -c "import vpython"</code>. It should print nothing at all and '
            'give you the prompt back. A traceback here is an install problem, not a '
            'problem with your program.')
ENV_EVERY = ('Save your file as <code>YourName_vpython%02d.py</code>: your first name, an '
             'underscore, then <code>vpython%02d</code>. Run it from the terminal. The 3D '
             'scene opens in a new browser tab, sometimes behind VS Code, so look for it '
             'before deciding that nothing happened. Click inside the scene before pressing '
             'any key. To end the program, close the tab or press Ctrl+C in the terminal. '
             'The program is written to run until you do. Run the file again and you get a '
             'fresh tab.')
ENV_NOTE = ('VPython draws solid shapes that you can turn and zoom. Everything you print '
            'still goes to the terminal, and everything you draw goes to the browser tab. '
            'Words in the terminal, pictures in the tab.')


def env_section(n):
    return ('<section><h2>Running this in VS Code</h2><div class="grid2">'
            '<div class="card"><h3>Once, before the first run</h3>'
            '<p>' + ENV_ONCE + '</p></div>'
            '<div class="card"><h3>Every run after that</h3>'
            '<p>' + (ENV_EVERY % (n, n)) + '</p></div></div>'
            '<p class="note">' + ENV_NOTE + '</p></section>')


def pager(prev_s, next_s):
    b = ['<nav class="pager">']
    if prev_s:
        b.append('<a href="' + link(prev_s["slug"]) + '">&larr; '
                 + html.escape(prev_s["title"]) + '</a>')
    else:
        b.append('<span></span>')
    b.append('<a href="' + link(HUB) + '">Course home</a>')
    if next_s:
        b.append('<a href="' + link(next_s["slug"]) + '">'
                 + html.escape(next_s["title"]) + ' &rarr;</a>')
    else:
        b.append('<span></span>')
    b.append('</nav>')
    return "".join(b)


def footer():
    return ('<footer><div class="wrap">'
            '<p>' + COURSE + ': eleven sessions of VPython for ages 10 to 11, in the Lecture '
            'Light style, light ground for a projector, predict before reveal, three '
            'places to stop in every session.</p>'
            '<p>Mapped to NY Next Generation Learning Standards and the Standards for '
            'Mathematical Practice. Codes resolved through the ' + CONNECTOR + ' on '
            + RESOLVED_ON + '. <a href="' + link(STDMAP) + '">Full standards map</a> '
            '&middot; <a href="' + link(LEDGER) + '">Ledger card</a></p>'
            '</div></footer>')


# ---------------------------------------------------------------------- hub

def render_hub():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; VPython &middot; Course home</p>')
    b.append('<h1>' + COURSE + ': 3D models, keys, and clicks</h1>')
    b.append('<p class="sub">Eleven sessions of VPython for ages 10 to 11. A world made of '
             'boxes and spheres, three numbers for every place, and programs that do '
             'something when you press a key or click the mouse.</p>')
    b.append('<div class="dates"><span class="pill"><b>Sessions</b> ' + str(len(SESSIONS))
             + '</span><span class="pill"><b>Length</b> 90 minutes each</span>'
             '<span class="pill"><b>Needs</b> Python 3.12 and pip install vpython</span></div>')
    b.append('</div></header><main><div class="wrap">')

    b.append('<section><h2>Sessions</h2><ul class="sessionlist">')
    for s in SESSIONS:
        meta = str(len(s["chunks"])) + ' chunks &middot; ' + s["brief"]["title"].replace("Build: ", "build: ")
        if s.get("date"):
            meta = html.escape(s["date"]) + ' &middot; ' + meta
        b.append('<li><span class="n">' + str(s["num"]) + '</span><div><a href="'
                 + link(s["slug"]) + '">' + html.escape(s["title"]) + '</a>'
                 '<span class="meta">' + meta + '</span></div></li>')
    b.append('</ul></section>')

    b.append('<section><h2>How a session runs</h2>'
             '<div class="grid2">'
             '<div class="card"><h3>Opener, 10 minutes</h3><p>Three retrieval questions '
             'about the ideas from the session before, on paper or talked out. Not the '
             'numbers: the ideas.</p></div>'
             '<div class="card"><h3>Chunks</h3><p>Each chunk is one idea, one program, and '
             'one prediction. Students run the program before the page shows what it '
             'prints. The reveal shows the real terminal output and the explanation '
             'together.</p></div>'
             '<div class="card"><h3>Hinge question</h3><p>One question that decides whether '
             'the room is ready to build. Talked through before the build brief.</p></div>'
             '<div class="card"><h3>Build brief</h3><p>A scene to make, with numbered steps, '
             'a worked card, and an expected-and-got sheet to fill in before and after '
             'running.</p></div>'
             '<div class="card"><h3>Three places to stop</h3><p>Floor, middle, and stretch. '
             'All three are finishes. The teacher panel on each page says what to cut '
             'when time runs out.</p></div>'
             '<div class="card"><h3>Ledger stamp</h3><p>One line per session on the <a href="'
             + link(LEDGER) + '">ledger card</a>: the names and ideas that session added.</p></div>'
             '</div></section>')

    b.append('<section><h2>What the course assumes, and what it never uses</h2>'
             '<p>Students arrive with variables, <code>if</code> gates, a <code>while</code> '
             'loop, <code>def</code> with parameters, and lists. Session 1 uses nothing else '
             'from Python. Later sessions add, one at a time and only after a chunk teaches '
             'it: <code>return</code>, attributes that an object carries '
             '(<code>planet.speed = 2</code>), <code>abs</code>, <code>round(x, 2)</code>, '
             '<code>str</code>, <code>randint</code>, indexing a string, nested loops, '
             '<code>!=</code>, <code>or</code>, and <code>elif</code>.</p>'
             '<p>Every program has the same shape: <code>from vpython import *</code>, make '
             'the objects, define the functions, bind them, then <code>while True:</code> '
             'with <code>rate(30)</code> inside it. The loop is VPython\'s own idiom, and '
             'the program ends when the browser tab is closed or Ctrl+C is pressed in the '
             'terminal.</p>'
             '<p>Not used anywhere in the course: <code>global</code>, dictionaries, '
             'classes, <code>break</code>, <code>try</code>, list comprehensions, file '
             'reading or writing, <code>compound</code>, 3D <code>text</code>, and '
             '<code>extrusion</code>. Shared state lives on objects as attributes, which '
             'session 6 teaches. Every output box on the site was captured by running the '
             'program; nothing was typed from expectation.</p></section>')

    b.append(env_section(1).replace('vpython01', 'vpythonNN').replace(
        'then <code>vpythonNN</code>', 'then <code>vpython</code> and the session number, '
        'two digits'))

    b.append('</div></main>')
    b.append(footer())
    return page(COURSE + ": VPython course home", "\n".join(b))


# -------------------------------------------------------------- ledger card

REFERENCE = [
    ("Shapes", "box(pos, size) &middot; sphere(pos, radius) &middot; cylinder(pos, axis, radius) &middot; "
               "cone(pos, axis, radius) &middot; pyramid(pos, size, axis) &middot; arrow(pos, axis) &middot; "
               "ring(pos, axis, radius, thickness) &middot; label(pos, text)"),
    ("Places", "vec(x, y, z): x right, y up, z toward you &middot; pos is the middle of a box or sphere "
               "and one end of a cylinder, cone or arrow &middot; pos + axis is the other end &middot; "
               "mag(v) is a length &middot; norm(v) is the direction only"),
    ("Looks", "color.red &middot; vec(r, g, b) from 0 to 1 &middot; opacity 0 to 1 &middot; visible = False"),
    ("Motion", "while True: rate(30) &middot; dt = 1 / 30 &middot; pos = pos + vel * dt &middot; "
               "vel = vel + gravity * dt &middot; vel.y = -vel.y to bounce &middot; "
               "obj.rotate(angle=radians(d), axis=vec(0, 1, 0), origin=p)"),
    ("Keys", "scene.bind(\"keydown\", f) and evt.key &middot; keysdown() inside the loop &middot; "
             "key names: \"a\", \"left\", \"right\", \"up\", \"down\", \" \""),
    ("Mouse", "scene.bind(\"click\", f) &middot; scene.mouse.pick, or None &middot; "
              "scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0.5, 0)) &middot; "
              "mousedown, mousemove, mouseup"),
    ("Widgets", "button(text, bind=f) &middot; slider(min, max, value, bind=f) and s.value &middot; "
                "checkbox(text, bind=f) and c.checked &middot; menu(choices, bind=f) and m.selected &middot; "
                "wtext(text) &middot; scene.caption"),
    ("Camera", "scene.center &middot; scene.range &middot; scene.forward &middot; scene.autoscale = False "
               "&middot; scene.camera.follow(obj) &middot; right-drag turns, scroll zooms"),
]

ERRORS = [
    ("ModuleNotFoundError: No module named 'vpython'", "The library is not installed in the Python you are running. pip install vpython, in the VS Code terminal."),
    ("AttributeError: 'NoneType' object has no attribute ...", "scene.mouse.pick was None, because the click hit empty space. Gate on None first."),
    ("TypeError: paint() missing 1 required positional argument", "You wrote paint() with brackets inside scene.bind. Name the function without brackets."),
    ("AttributeError: 'sphere' object has no attribute 'speed'", "You read an attribute before giving it a value. Assign planet.speed = 2 first."),
    ("IndexError: string index out of range", "A row or column number is past the edge of the level. Keep a wall of # around the edge."),
    ("Nothing happens when a key is pressed", "Not an error. Click inside the 3D scene first, then check that the loop at the bottom is still running."),
]


def render_ledger():
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; VPython &middot; Ledger card</p>')
    b.append('<h1>Ledger card</h1>')
    b.append('<p class="sub">One stamp per session. Print it, keep it in the folder, and bring it '
             'every week. The reference strip below it is every name the course uses.</p>')
    b.append('</div></header><main><div class="wrap">')
    b.append('<section><h2>Stamps</h2><div class="stampgrid">')
    for s in SESSIONS:
        b.append('<div class="stamp"><span class="no">Session ' + str(s["num"]) + '</span>'
                 + s["ledger"].split(": ", 1)[1] + '</div>')
    b.append('</div></section>')
    b.append('<section><h2>Reference strip</h2><table><tr><th>Topic</th><th>Names</th></tr>')
    for t, names in REFERENCE:
        b.append('<tr><td><b>' + t + '</b></td><td>' + names + '</td></tr>')
    b.append('</table></section>')
    b.append('<section><h2>Errors you will meet, and what each one means</h2>'
             '<table><tr><th>What the terminal says</th><th>What it means</th></tr>')
    for e, m in ERRORS:
        b.append('<tr><td><code>' + html.escape(e) + '</code></td><td>' + html.escape(m) + '</td></tr>')
    b.append('</table></section>')
    b.append('</div></main>')
    b.append('<nav class="pager"><span></span><a href="' + link(HUB) + '">Course home</a><span></span></nav>')
    b.append(footer())
    return page(COURSE + ": ledger card", "\n".join(b))


# ------------------------------------------------------------ standards map

def render_standards_map():
    used = {}
    for s in SESSIONS:
        for c in s["teacher"]["standards"]:
            used.setdefault(c, []).append(s["num"])
    b = ['<header class="top"><div class="wrap">']
    b.append('<p class="eyebrow">' + COURSE + ' &middot; VPython &middot; Standards map</p>')
    b.append('<h1>Standards map</h1>')
    b.append('<p class="sub">Every code used on the site, with its full statement and CASE '
             'identifier, and the sessions that are mapped to it.</p>')
    b.append('</div></header><main><div class="wrap">')
    b.append('<section><p>Codes were resolved through the ' + CONNECTOR + ' on ' + RESOLVED_ON
             + '. Nothing was written from memory. At most three codes per session, footered '
             'as "mapped to" rather than "aligned with". No computer science code appears, '
             'because the connector cannot verify them.</p></section>')
    b.append('<section><table><tr><th>Code</th><th>Framework</th><th>Grade</th>'
             '<th>Statement</th><th>Sessions</th><th>CASE identifier</th></tr>')
    for c in sorted(used, key=lambda k: (STANDARDS[k]["framework"], k)):
        st = STANDARDS[c]
        b.append('<tr><td><code>' + c + '</code></td><td>' + st["framework"] + '</td><td>'
                 + st["grades"] + '</td><td>' + html.escape(st["statement"]) + '</td><td>'
                 + ", ".join(str(x) for x in used[c]) + '</td><td><code>' + st["uuid"]
                 + '</code></td></tr>')
    b.append('</table></section>')
    b.append('</div></main>')
    b.append('<nav class="pager"><span></span><a href="' + link(HUB) + '">Course home</a><span></span></nav>')
    b.append(footer())
    return page(COURSE + ": standards map", "\n".join(b))


def write(name, text):
    path = os.path.join(OUT, name + ".html")
    with open(path, "w") as fh:
        fh.write(text)
    print("wrote %-52s %6.1f kB" % (name + ".html", len(text) / 1024.0))


def main():
    only = os.environ.get("VPL_ONLY")
    for i, s in enumerate(SESSIONS):
        if only and str(s["num"]) not in only.split(","):
            continue
        prev_s = SESSIONS[i - 1] if i > 0 else None
        next_s = SESSIONS[i + 1] if i + 1 < len(SESSIONS) else None
        write(s["slug"], render_session(s, prev_s, next_s))
    write(HUB, render_hub())
    write(LEDGER, render_ledger())
    write(STDMAP, render_standards_map())
    print("\nverification log")
    for row in VERIFY_LOG:
        print("  " + "  ".join(row))


if __name__ == "__main__":
    main()
