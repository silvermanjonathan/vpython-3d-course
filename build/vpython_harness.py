"""Run one student program against the real vpython library with no browser.

render.py uses this to capture the terminal output that goes in the page's output
boxes, the way the beginner course runs its pygame snippets headless. Nothing is
simulated on the Python side: the objects, vectors, defaults, event objects, and
widget callbacks are vpython's own. What is missing is the browser tab, so the
harness does three things the tab would normally do:

1. Lets import finish. In no-notebook mode vpython waits, at the first object, for
   a browser to fetch the page and open a websocket. A thread flips those two
   flags once vpython reaches that wait.
2. Feeds in events. Each injected item names a loop pass and an event, in the
   same dictionaries glowcomm.js sends: a key press, keys held down, a click at a
   point in the 3D world, or a widget. They are handed to vpython's own
   GlowWidget.handle_msg, so bound functions run through the real dispatch.
3. Ends the run. rate() counts loop passes and stops the program after the quota.

Usage: python3 vpython_harness.py <student file> <max passes> <inject json>

Inject items:
  [pass, "KEYDOWN", "r"]                  one keydown event, evt.key == "r"
  [pass, "HOLD", "right"]                 "right" is in keysdown() on that pass
  [pass, "CLICK", [x, y, z]]              a click whose ray passes through (x, y, z);
                                          scene.mouse.pick is the object containing
                                          that point, or None
  [pass, "MOUSEDOWN", [x, y, z]]          the left button pressed at that point
  [pass, "MOUSEMOVE", [x, y, z]]          the mouse moved to that point
  [pass, "MOUSEUP", [x, y, z]]            the left button released at that point
  [pass, "WIDGET", "fn", value]           the widget bound to function fn is used;
                                          value is the slider value, menu index,
                                          or checkbox state (omit for a button)
Pass numbers count calls to rate(): the events for pass 3 are fed in during the
third call, before the loop body runs for the third time.
"""

import json
import math
import os
import sys
import threading
import time
import traceback

os.environ["VPYTHON_NO_LAUNCH_BROWSER"] = "1"
if os.environ.get("VPY_SRC"):
    # a source checkout of vpython-jupyter, for machines with no wheel
    sys.path.insert(0, os.environ["VPY_SRC"])

STUDENT = sys.argv[1]
MAXF = int(sys.argv[2])
INJ = json.loads(sys.argv[3]) if len(sys.argv) > 3 else []
HERE = os.path.abspath(__file__)


def _unblock():
    # no_notebook waits for httpserving and websocketserving; a browser would set
    # them. Set them once the module has reached its wait loop (GW exists by then).
    while True:
        nn = sys.modules.get("vpython.no_notebook")
        if nn is not None and hasattr(nn, "GW"):
            nn.httpserving = True
            nn.websocketserving = True
            return
        time.sleep(0.002)


threading.Thread(target=_unblock, daemon=True).start()

import vpython                      # noqa: E402
import vpython.vpython as _vp       # noqa: E402

_norm = _vp.norm
_dot = _vp.dot
_vector = _vp.vector
_state = {"f": 0, "pick": None, "down": False}


def _finish(rc):
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(rc)


def _gw():
    return sys.modules["vpython.no_notebook"].GW


def _scene():
    return vpython.scene


def _send(evt):
    _gw().handle_msg({"content": {"data": [evt]}})


def _contains(obj, p):
    """True if point p is inside obj, for the shapes the course uses.

    Boxes and spheres are exact. A cylinder, cone, pyramid or arrow is treated as
    the box that runs from its pos along its axis, size.y tall and size.z deep,
    which is exact while the axis lies along x, y or z."""
    name = getattr(obj, "_objName", "")
    if not getattr(obj, "visible", True):
        return False
    if name == "box":
        s = obj.size
        d = p - obj.pos
        return (abs(d.x) <= s.x / 2 + 1e-9 and abs(d.y) <= s.y / 2 + 1e-9
                and abs(d.z) <= s.z / 2 + 1e-9)
    if name == "sphere":
        return (p - obj.pos).mag <= obj.radius + 1e-9
    if name in ("cylinder", "cone", "pyramid", "arrow"):
        a = obj.axis
        length = a.mag
        if length == 0:
            return False
        u = _norm(a)
        d = p - obj.pos
        along = _dot(d, u)
        if along < -1e-9 or along > length + 1e-9:
            return False
        across = d - along * u
        half = max(obj.size.y, obj.size.z) / 2
        return abs(across.x) <= half + 1e-9 and abs(across.y) <= half + 1e-9 and abs(across.z) <= half + 1e-9
    return False


def _resolve_pick(point):
    best = None
    best_vol = None
    for obj in list(_vp.baseObj.object_registry.values()):
        if not _contains(obj, point):
            continue
        s = obj.size
        vol = s.x * s.y * s.z
        if best is None or vol < best_vol:
            best, best_vol = obj, vol
    return best


def _mouse(kind, point):
    sc = _scene()
    p = _vector(*point)
    cam = sc.camera.pos
    ray = _norm(p - cam)
    fwd = _norm(sc._axis)
    t = _dot(sc.center - cam, fwd) / _dot(ray, fwd)
    pos = cam + t * ray
    target = _resolve_pick(p)
    _state["pick"] = target.idx if target is not None else None
    if kind == "mousedown":
        _state["down"] = True
    press = _state["down"] if kind == "mousemove" else kind == "mousedown"
    release = kind in ("mouseup", "click")
    if kind == "mouseup":
        _state["down"] = False
    _send({"event": kind, "canvas": sc.idx,
           "pos": [pos.x, pos.y, pos.z], "ray": [ray.x, ray.y, ray.z],
           "press": press, "release": release, "which": 1,
           "alt": False, "ctrl": False, "shift": False})


def _click(point):
    _mouse("click", point)


def _key(kind, key):
    sc = _scene()
    which = {"left": 37, "up": 38, "right": 39, "down": 40, "shift": 16,
             "ctrl": 17, "alt": 18, "backspace": 8, "delete": 46,
             "enter": 13, " ": 32}.get(key, ord(key[0].upper()) if key else 0)
    _send({"event": kind, "canvas": sc.idx, "key": key, "which": which,
           "alt": False, "ctrl": False, "shift": key.isupper()})


def _widget(fn, value):
    for obj in list(_vp.baseObj.object_registry.values()):
        b = getattr(obj, "_bind", None)
        if b is not None and getattr(b, "__name__", "") == fn:
            evt = {"idx": obj.idx, "widget": obj.objName, "value": value}
            if obj.objName == "winput":
                evt["text"] = str(value)
            _send(evt)
            return
    raise SystemExit("harness: no widget is bound to a function called " + fn)


def _fire(f):
    held = []
    for item in INJ:
        if item[0] != f:
            continue
        kind = item[1]
        if kind == "KEYDOWN":
            _key("keydown", item[2])
        elif kind == "KEYUP":
            _key("keyup", item[2])
        elif kind == "HOLD":
            held.append(item[2])
        elif kind == "CLICK":
            _click(item[2])
        elif kind in ("MOUSEDOWN", "MOUSEMOVE", "MOUSEUP"):
            _mouse(kind.lower(), item[2])
        elif kind == "WIDGET":
            _widget(item[2], item[3] if len(item) > 3 else 0)
        else:
            raise SystemExit("harness: unknown inject kind " + str(kind))
    _send({"event": "update_canvas", "canvas": _scene().idx, "keysdown": held})


def _rate(n):
    _state["f"] += 1
    if _state["f"] > MAXF:
        _finish(0)
    _fire(_state["f"])


def _wait(cvs):
    # Only scene.mouse.pick reaches here in this lesson. A browser would answer
    # with a pick event; answer with the object under the injected click.
    cvs._waitfor = None
    cvs.handle_event({"event": "pick", "canvas": cvs.idx,
                      "pick": _state["pick"], "segment": None})
    return cvs._waitfor


vpython.rate = _rate
_vp.rate = _rate
_vp._wait = _wait


def main():
    code = open(STUDENT).read()
    name = os.path.basename(STUDENT)
    ns = {"__name__": "__main__", "__file__": name}
    try:
        exec(compile(code, name, "exec"), ns)
    except SystemExit as e:
        _finish(0 if e.code in (None, 0) else 1)
    except BaseException:
        et, ev, tb = sys.exc_info()
        frames = [fr for fr in traceback.extract_tb(tb) if fr.filename != HERE]
        sys.stderr.write("Traceback (most recent call last):\n")
        sys.stderr.write("".join(traceback.format_list(frames)))
        sys.stderr.write("".join(traceback.format_exception_only(et, ev)))
        _finish(1)
    _finish(0)


main()
