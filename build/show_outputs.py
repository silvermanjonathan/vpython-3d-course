"""Print every output box on one or more session pages next to its label, for
checking the prose against the captured output. Usage: show_outputs.py 2 3"""
import html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
want = sys.argv[1:]
for f in sorted(os.listdir(SITE)):
    if not f.startswith("session") or not f.endswith(".html"):
        continue
    num = str(int(f[7:9]))
    if want and num not in want:
        continue
    t = open(os.path.join(SITE, f)).read()
    print("=" * 20, f)
    for m in re.finditer(r'<h2>(.*?)</h2>.*?<p class="outlabel">(.*?)</p><pre class="out">(.*?)</pre>(?:<p class="note">(Fed in[^<]*)</p>)?', t, re.S):
        title, lbl, out, fed = m.groups()
        print("---", html.unescape(title), "|", lbl)
        print(html.unescape(out))
        if fed:
            print("  [" + fed + "]")
