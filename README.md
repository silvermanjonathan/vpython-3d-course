# vpython-3d-course

Python in 3D: eleven 90-minute sessions of VPython for ages 10 to 11. A world made of
boxes and spheres, three numbers for every place, and programs that do something
when a key is pressed or the mouse is clicked. It ends with each student's own
project and a two-minute demo.

The course stands on its own. It assumes variables, `if` gates, a `while` loop, `def`
with parameters, and lists, and nothing else. Everything further is taught by a chunk
before any page uses it.

Homepage: `vpython_course_hub.html` at the repo root (there is no `index.html`).

## Pages

| File | What it is |
|---|---|
| `vpython_course_hub.html` | Course home. Session list, how a session runs, what the course assumes and never uses, the VS Code notes. |
| `vpython_ledger_card.html` | The printable card: eleven stamp boxes, a reference strip of every name the course uses, and the errors students will meet. |
| `standards_map.html` | Every standard code used, with its full statement, CASE identifier, and the sessions mapped to it. |
| `session01_3d_models_keys_and_clicks.html` | 3D models that answer keys and clicks |
| `session02_shapes_and_a_model_from_a_function.html` | Shapes, and a model built by a function |
| `session03_velocity_gravity_and_bouncing.html` | Motion: velocity, gravity, and bouncing |
| `session04_turning_things_and_the_camera.html` | Turning things, and turning the camera |
| `session05_a_car_with_wheels_that_roll.html` | A car with wheels that roll along a road |
| `session06_a_solar_system_objects_carry_their_numbers.html` | A solar system: objects that carry their own numbers |
| `session07_a_game_catch_the_falling_balls.html` | A game: catch the falling balls |
| `session08_a_grid_world_from_a_list_of_strings.html` | A grid world: a level from a list of strings |
| `session09_a_scene_editor_dragging_with_the_mouse.html` | A scene editor: dragging with the mouse |
| `session10_your_project.html` | Your project: three briefs, a plan sheet, a skeleton, one feature at a time |
| `session11_finish_polish_and_show.html` | Finish, polish, and show |

## The arc

| | Session | What it adds | Build |
|---|---|---|---|
| 1 | Models, keys, clicks | `vec`, `pos` is the middle, the loop with `rate(30)`, `scene.bind` and `evt.key`, `keysdown()`, `scene.mouse.pick`, widgets | a block builder |
| 2 | Shapes and a function | cylinder, cone, pyramid, `axis`, colours as `vec(r, g, b)`, opacity, a function that makes objects, one `height` that sets every size, a model as a list | a village with a rocket |
| 3 | Motion | velocity, `dt`, gravity on the velocity, the floor gate, flipping a sign, losing speed, keys that push, `round(x, 2)` | the bouncy room |
| 4 | Turning | `rotate` with `radians`, a spin counter, `origin=`, `norm`, `scene.center` / `range` / `forward`, `scene.camera.follow` | drive the car |
| 5 | A car with wheels | a wheel is a cylinder lifted by its radius, `parts` and `rolling` lists, a road from a loop, `step = speed * dt`, one circumference is one full turn, `radians(-turn)`, a loop-back gate on every part | the road trip |
| 6 | Solar system | `return` of an object, attributes the program gives (`planet.speed`), a list turned by one loop, a moon with two motions, a slider on `sun.factor`, `label`, `str` | the solar system |
| 7 | A game | `abs`, `randint`, a catch gate with `and`, `wtext`, lives, a `state` name, restart from the loop, harder each catch | the catch game in 3D |
| 8 | Grid world | a level as a list of strings, row then column, nested loops, row and col as attributes, `place`, `is_open` and `!=`, a goal, coins | the coin maze |
| 9 | Scene editor | `mousedown` / `mousemove` / `mouseup`, `evt.press`, what is held on `floor.held`, `project` at a height, snap with `round`, `menu`, `checkbox`, `elif` | the scene editor |
| 10 | Your project | a knob block, a skeleton that runs, one feature then run, the caption as the plan, the plan sheet; starter cards A, B, C | the project, part one |
| 11 | Finish and show | a start state and the space key, a `home` copy for Reset, three lines of polish, the partner test, the demo script | finish, test, polish, show |

Shared state between a bound function and the loop is always an attribute on an
object (`sun.factor`, `floor.held`, `player.score`), which session 6 teaches. The
course never uses `global`, dictionaries, classes, `break`, `try`, comprehensions,
file reading or writing, `compound`, 3D `text`, or `extrusion`.

## Dates

The pages are undated. Each session dict has a `"date"` key that is empty; put a
date string in it (`"Tue Oct 13"`) and the page and the hub both show it. Bump
`VERSION` in `build/render.py` after any content change so embedded pages are not
served from cache.

## Environment

VS Code on the desktop, the program run from the terminal, the 3D scene in a browser
tab. `pip install vpython`.

VPython 7.6.5 (March 2024, still the newest stable release in October 2026) runs on
Python 3.8 to 3.12. On a newer Python the import fails with
`ModuleNotFoundError: No module named 'pkg_resources'`, because setuptools 82 removed
that module; the fix is merged on GitHub but not yet released. Keep the room on
Python 3.12, and if the error appears run `pip install "setuptools<81"` once.

Key events do not reach a program that runs inside a Jupyter notebook. Everything on
these pages is run from the terminal.

The one loop idiom on the site is VPython's own:

```python
while True:
    rate(30)
```

The program ends when the browser tab is closed or Ctrl+C is pressed in the
terminal. The pages say so wherever the loop appears.

Student files are named with the student's first name, an underscore, then
`vpython` and the two-digit session number: `Jonathan_vpython07.py`. Jonathan stands
in for the name on the pages and in any traceback the build captures.

## Look and behaviour

The pages use the Lecture Light style of the beginner Python course: light ground for
a projector in a room with the lights on, near-black text, three accents, 2px rules
and 6 to 8px accent edges, 18px body text, code coloured by role the way VS Code's
Light+ theme colours it. `build/highlight.py` is the same file the beginner course
uses; stripping its spans gives back every snippet exactly.

Every chunk shows the code, then the prediction question, then a button reading
"Run it first, then check here". The button reveals the verified terminal output and
the explanation together. Nothing about what a program prints is visible until the
button is clicked. Under every output box the page says what the build script fed
in, in pass order.

## Repo conventions

- Flat repo. No subdirectories except `build/`, no `index.html`.
- All CSS and JavaScript inline. Google Fonts is the only external dependency.
- No `localStorage`, no `sessionStorage`, no `indexedDB`.
- Internal links carry a version pin, `?v=1`. Bump it on every content change.
- Zero em-dash and en-dash characters anywhere in the prose. The validator fails
  the build if one appears.
- No reference to any other course, camp, or term, on the pages or in the programs.

## Standards

The codes on the site were resolved through the Learning Commons Knowledge Graph
connector (CASE Network) on 2026-10-05 (NY-7.G.4 on 2026-10-26) and are printed with their CASE identifiers.
At most three per session, footered as "mapped to", not "aligned with".

- New York Next Generation Mathematics: NY-4.MD.5, NY-5.G.1, NY-5.G.2, NY-6.EE.2,
  NY-6.EE.5, NY-6.EE.9, NY-6.NS.5, NY-6.NS.6, NY-6.NS.8, NY-7.G.4
- Standards for Mathematical Practice, Multi-State: MP1, MP6, MP7, MP8
- New York Next Generation ELA: 5SL4, 5W2

No computer science code appears, because the connector cannot verify them.

## Build

The HTML is generated. Edit the content files, not the HTML.

```
build/sessions_a.py       sessions 1 to 3
build/sessions_b.py       sessions 4 to 7
build/sessions_c.py       sessions 8 to 11
build/standards.py        the resolved standards registry
build/render.py           runs every snippet, then writes the site (hub, ledger, standards map are functions in it)
build/vpython_harness.py  runs one snippet against the real vpython library, no browser
build/validate.py         checks the written site
build/highlight.py        colours code blocks by role, the way VS Code's Light+ theme does
build/show_outputs.py     prints every output box on the chosen session pages, for checking prose against output
```

```
pip install vpython
python3 build/render.py
python3 build/validate.py
```

`VPL_ONLY=4,5 python3 build/render.py` rebuilds only those sessions (the hub, ledger
and standards map are always rewritten).

On a machine whose Python has no vpython wheel, point the build at a source checkout
instead of installing:

```
git clone --depth 1 https://github.com/vpython/vpython-jupyter
VPY_SRC=$PWD/vpython-jupyter python3 build/render.py
```

A checkout that is not installed has no package version, so `vpython/__init__.py`
needs `__version__` set in its `except PackageNotFoundError:` branch. This site was
built against the October 2026 `master` with that one line added.

## Verification

`render.py` executes every snippet and pastes the real captured output into the
pages. No output box on this site was typed from expectation. 75 output blocks, 117
reveal buttons, 14 pages.

- Each snippet runs in its own process through `build/vpython_harness.py`, against
  the real `vpython` library: the objects, vectors, starting values, event objects,
  and widget callbacks are VPython's own.
- There is no browser. In no-notebook mode VPython waits at the first object for a
  browser to fetch the page and open a websocket; the harness flips those two flags
  once VPython reaches that wait, and sets `VPYTHON_NO_LAUNCH_BROWSER`.
- Keys, holds, clicks, presses, moves, releases and widget events are fed in through
  VPython's own dispatch (`GlowWidget.handle_msg`), in the same dictionaries the
  browser's `glowcomm.js` sends. A mouse event names a point in the 3D world;
  `scene.mouse.pick` becomes the object that contains that point, or `None`, and
  `scene.mouse.project` runs VPython's own arithmetic on the injected ray. Boxes and
  spheres are picked exactly; a cylinder, cone, pyramid or arrow is picked by the
  box along its axis.
- `rate()` counts loop passes and ends the program after the quota, so every snippet
  that contains the loop says on the page how many passes it ran. Events for pass
  n are fed in during the nth call to `rate()`, before that pass's body runs.
- Two snippets end in an error on purpose (session 6, chunk 2, and the AttributeError
  quoted in session 1). A snippet marked `expect_error` may exit non-zero; any other
  non-zero exit fails the build.
- What is not checked: the picture. Run each session's programs once on the
  projector machine before class.

`validate.py` checks tag balance, reveal-button to answer-block parity, duplicate
reveal ids, `aria-controls` and `aria-expanded` on every reveal button, escaped angle
brackets inside `<pre>` blocks, absence of storage APIs, dash characters, banned
filler phrases (including any mention of another course), dead internal links, the
presence of a title and an h1 on every page, and that every teacher panel's timing
rows sum to 90 minutes and include a ledger stamp row.
