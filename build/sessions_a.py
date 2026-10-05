"""Sessions 1 to 3 of the VPython course: every word and every snippet.

Same shape as the beginner course's session files. render.py runs each snippet
through vpython_harness.py and pastes the real terminal output into the page.
"""


def code(text):
    # Snippets are written as triple-quoted blocks for readability. Strip the
    # leading newline so the student file starts on line 1.
    return text.lstrip("\n").rstrip() + "\n"


SESSIONS_A = [

# =====================================================================
{
 "num": 1,
 "slug": "session01_3d_models_keys_and_clicks",
 "title": "3D models that answer keys and clicks",
 "subtitle": "A world made of boxes and spheres, three numbers for every place, and the first program that does something when you press a key or click the mouse",
 "new": ["from vpython import *", "sphere and box", "vec(x, y, z)", "pos, size, radius, color", "while True with rate(30)", "scene.bind and evt.key", "keysdown()", "scene.mouse.pick", "button and slider"],
 "reuse": "Variables, if gates, a while loop, def with one parameter, and a list",
 "env_note": True,
 "reuse_note": "Nothing today needs a new Python idea except the library. Every program on this page has the same four parts: make the objects, write a function, bind it, and keep the loop at the bottom running. Say that before chunk 5, because the four programs in chunks 5 to 8 otherwise look like four different shapes.",
 "opener": {
   "title": "Retrieval: graphs, functions, and loops",
   "minutes": 10,
   "body": "Paper first. Three questions about things you already know, because every one of them does a job in today's programs.",
   "questions": [
     {"q": "A point on a graph is written (2, 3). Which number says how far across, and which says how far up?",
      "a": "The first number, 2, is across. The second number, 3, is up. Today every place gets a third number that says how far toward you, so a place is three numbers instead of two."},
     {"q": "Does the print line run when Python reads the <code>def</code>, or only later?",
      "code": 'def hello(name):\n    print("hello", name)',
      "a": "Only later, when something calls <code>hello</code>. The def makes the function and stores it under the name <code>hello</code>. Today you write functions that you never call yourself. VPython calls them when a key goes down or the mouse is clicked."},
     {"q": "What does a <code>while</code> loop do that an <code>if</code> gate does not?",
      "a": "It repeats. The gate checks its condition once and runs its body once or not at all. The loop checks its condition before every pass and runs the body again each time the condition is True. Every program today ends with a loop whose condition is always True, so it runs until you stop it."},
   ],
 },
 "chunks": [
  {"title": "One line makes a world",
   "teach": "VPython is a library: a file of functions that someone else wrote. <code>from vpython import *</code> gives your program every one of them. <code>sphere()</code> makes a ball and opens a browser tab to show it. The tab is where the pictures go. The terminal still shows what you print.</p><p>Every object has a <b>pos</b>: three numbers that say where its middle is. The program never gives the sphere a pos, so it gets the starting value.",
   "code": code('''
from vpython import *

ball = sphere()
print("the ball is at", ball.pos)
print("its radius is", ball.radius)
'''),
   "run": "vpython",
   "predict": "The program never says where to put the ball. The first print line shows <code>ball.pos</code> as three numbers. What are the three numbers, and what is the radius?",
   "reveal": "All three numbers are 0, printed as <code>&lt;0, 0, 0&gt;</code>. That is the middle of the world, and the camera looks straight at it. The radius is 1. Both are the starting values VPython gives a sphere when you do not say otherwise. Right-drag inside the tab to turn the camera, and scroll to zoom. Close the tab, or press Ctrl+C in the terminal, when you are done looking."},

  {"title": "Three numbers for every place",
   "teach": "<code>vec(2, 0, 0)</code> is a <b>vector</b>: three numbers held in one value, in the order x, y, z. x is how far to the right. y is how far up. z is how far toward you, out of the screen. A negative number goes the other way: left, down, or away from you.</p><p>You can add two vectors. Each number adds to its own partner: x with x, y with y, z with z. Adding <code>vec(0, 3, 0)</code> to a pos leaves x and z alone and raises y by 3.</p><p>The three arrows are the axes. Red points along x, green along y, blue along z. Keep them in your programs until the directions feel obvious.",
   "code": code('''
from vpython import *

arrow(axis=vec(3, 0, 0), color=color.red)
arrow(axis=vec(0, 3, 0), color=color.green)
arrow(axis=vec(0, 0, 3), color=color.blue)

crate = box(pos=vec(2, 0, 0), color=color.orange)
print("crate is at", crate.pos)

crate.pos = crate.pos + vec(0, 3, 0)
print("crate is now at", crate.pos)

crate.pos = crate.pos + vec(-2, 0, -4)
print("and now at", crate.pos)
'''),
   "run": "vpython",
   "predict": "The last pos line adds <code>vec(-2, 0, -4)</code>. Which of the three numbers change? And where does the crate end up: left or right of where it was, higher or lower, closer to you or farther away?",
   "reveal": "x and z change. y stays 3.</p><p>Left or right: left, by 2. x goes from 2 to 0, so the crate is straight above the middle of the world.</p><p>Higher or lower: neither. The y number did not change, so the crate is still 3 up.</p><p>Closer or farther: farther away, by 4. z goes from 0 to -4, and negative z is away from you. The output box shows <code>&lt;0, 3, -4&gt;</code>. Turn the camera with a right-drag and you can see the crate sitting behind the arrows."},

  {"title": "pos is the middle, so things sink",
   "teach": "A box has a <b>size</b>: three numbers for how long, how tall, and how deep it is. Each of the three starts at 1 when you do not say. <code>pos</code> is the middle of the box, not its bottom. A box 1 tall with its pos at y = 0 reaches from y = -0.5 up to y = 0.5.</p><p>The ground here is a wide, flat box. Its middle is at y = -0.1 and it is 0.2 tall, so its top face is at y = 0. Put a crate at y = 0 and half of the crate is under the ground.</p><p><code>crate.pos.y</code> is the y number on its own. You can read it, and you can assign to it.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
crate = box(pos=vec(0, 0, 0), color=color.orange)
print("crate middle is at y =", crate.pos.y)
print("crate bottom is at y =", crate.pos.y - crate.size.y / 2)

crate.pos.y = 0.5
print("after the fix, crate bottom is at y =", crate.pos.y - crate.size.y / 2)
'''),
   "run": "vpython",
   "predict": "The ground's top face is at y = 0 and the crate's pos is at y = 0. How much of the crate is under the ground? And after the fix line, what number is in <code>crate.pos.y</code>, and where is the bottom of the crate?",
   "reveal": "Half of the crate is under the ground. pos is the middle and the crate is 1 tall, so its bottom is at y = -0.5, which the second output line shows.</p><p>After the fix, <code>crate.pos.y</code> is 0.5. That lifts the middle by half the height, so the bottom is at y = 0.0, exactly on the ground. A taller crate needs a bigger lift: half of its height, every time."},

  {"title": "The loop at the bottom, and why rate(30) is in it",
   "teach": "A program that has reached its last line is finished. VPython's own instructions say to end every program with a loop that never stops, so the program keeps running and can keep listening for keys and clicks. <code>while True:</code> is that loop. Its condition is always True, so the body runs pass after pass until you close the tab or press Ctrl+C in the terminal.</p><p><code>rate(30)</code> is the one line the loop must have. It makes the loop pause so that it runs 30 passes in a second and no more, which leaves the computer time to draw the picture between passes.</p><p>Everything else in the body happens once per pass. Move the ball by 0.1 on every pass and it travels 3 in one second.",
   "code": code('''
from vpython import *

ball = sphere(color=color.yellow)
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos.x = ball.pos.x + 0.1
    if passes == 30:
        print("after", passes, "passes the ball is at", ball.pos)
    if passes == 60:
        print("after", passes, "passes the ball is at", ball.pos)
'''),
   "run": "vpython",
   "frames": 60,
   "predict": "Thirty passes take one second. How far along x has the ball moved after one second, and how far after two? Say what you would see in the tab.",
   "reveal": "After one second x is 3: thirty passes, and 0.1 added on each one. After two seconds x is 6. The output box shows <code>&lt;3, 0, 0&gt;</code> and then <code>&lt;6, 0, 0&gt;</code>.</p><p>In the tab, the ball slides to the right and keeps going until you stop the program. The number in <code>rate</code> is the passes per second, so <code>rate(60)</code> with the same 0.1 would move the ball twice as fast."},

  {"title": "A key press is an event, and a function answers it",
   "teach": "Pressing a key is an <b>event</b>: something that happens while the program runs, at a moment the program does not choose. You do not call the function yourself. You <b>bind</b> it. <code>scene.bind(\"keydown\", paint)</code> tells VPython to call <code>paint</code> every time a key goes down. Write the function's name without brackets, because you are naming it, not calling it.</p><p>VPython calls the function with one argument, the event. <code>evt.key</code> is the name of the key as a string: <code>\"r\"</code>, <code>\"g\"</code>, <code>\"left\"</code>, <code>\"up\"</code>, and so on. Three flat gates compare it with the three letters. A key that none of the gates name changes nothing.</p><p>The tab only hears keys when it has the focus. Click inside the 3D scene once before pressing anything. The caption line above the scene is there to remind you.",
   "code": code('''
from vpython import *

scene.caption = "Click the 3D scene, then press r, g, or b."
ball = sphere(color=color.white)

def paint(evt):
    if evt.key == "r":
        ball.color = color.red
    if evt.key == "g":
        ball.color = color.green
    if evt.key == "b":
        ball.color = color.blue
    print("key pressed:", evt.key, " ball colour is now", ball.color)

scene.bind("keydown", paint)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 10,
   "inject": [[2, "KEYDOWN", "g"], [5, "KEYDOWN", "b"], [7, "KEYDOWN", "x"]],
   "predict": "Three keys are pressed in turn: g, then b, then x. What colour is the ball after each one? Which of the three print lines shows a colour that did not change, and why did that line print at all?",
   "reveal": "After g the ball is green and the print shows <code>&lt;0, 1, 0&gt;</code>. A colour is a vector too: red, green, and blue, each from 0 to 1. After b the ball is blue, <code>&lt;0, 0, 1&gt;</code>. After x the ball is still blue.</p><p>The third print line shows the colour that did not change, the same <code>&lt;0, 0, 1&gt;</code> as the second. It printed because <code>paint</code> runs on every key press: VPython calls it for x the same way it calls it for g and b. The three gates decide whether a colour is assigned, and for x all three are False, so the print line is the only line in the body that runs."},

  {"title": "Holding a key down",
   "teach": "A keydown event happens once per press. Hold the arrow down and nothing more happens. For a box that keeps moving while the key is held, ask a different question on every pass: <code>keysdown()</code> returns a list of the keys that are down right now. <code>\"right\" in keys</code> is True on every pass while the right arrow is held.</p><p>This program has no bound function. The four gates are inside the loop, so they run 30 times a second, and every pass with the key held adds <code>speed</code> once more.</p><p>The print line runs only on passes where the list is not empty, so the terminal shows one line per pass while a key is held and nothing in between.",
   "code": code('''
from vpython import *

scene.caption = "Click the 3D scene, then hold an arrow key."
floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
player = box(pos=vec(0, 0.5, 0), color=color.orange)
speed = 0.2

while True:
    rate(30)
    keys = keysdown()
    if "right" in keys:
        player.pos.x = player.pos.x + speed
    if "left" in keys:
        player.pos.x = player.pos.x - speed
    if "up" in keys:
        player.pos.z = player.pos.z - speed
    if "down" in keys:
        player.pos.z = player.pos.z + speed
    if len(keys) > 0:
        print(keys, "player is at", player.pos)
'''),
   "run": "vpython",
   "frames": 10,
   "inject": [[3, "HOLD", "right"], [4, "HOLD", "right"], [5, "HOLD", "right"], [8, "HOLD", "up"]],
   "predict": "The right arrow is held down for three passes, then let go, then the up arrow is held for one pass. Which of the three pos numbers changes while right is held, and by how much in total? When up is held, does the z number go up or down, and does the box rise?",
   "reveal": "While right is held, the first number, x, changes: by 0.6 in total, 0.2 on each of the three passes. The output box shows x at 0.2, then 0.4, then 0.6.</p><p>When up is held, z goes down, from 0 to -0.2. The up arrow is wired to the gate that subtracts <code>speed</code> from <code>player.pos.z</code>, and negative z is away from you, so the box moves away across the floor. The box does not rise: y stays 0.5 on every line. To make the up arrow lift the box instead, change <code>player.pos.z</code> to <code>player.pos.y</code> in that gate and change the minus to a plus."},

  {"title": "Clicking on a thing",
   "teach": "A click is an event too. Bind a function to <code>\"click\"</code>. Inside it, <code>scene.mouse.pick</code> is the object that was under the mouse at the moment of the click. The house word for this object is the <b>pick</b>.</p><p>When the mouse is over empty space there is no object, and the pick is <code>None</code>. None is Python's value for nothing. The gate <code>if thing is None:</code> catches that case. Without it, the colour line would try to colour nothing, and the program would stop with an error that starts <code>AttributeError: 'NoneType' object has no attribute 'color'</code>.</p><p>The seven boxes have no names of their own. The pick is whichever one was clicked, and <code>thing</code> is its name inside the function. A right-drag turns the camera and is not a click, so the function does not run for it.",
   "code": code('''
from vpython import *

scene.caption = "Click a box. Then click the gap between two boxes."
for x in range(-3, 4):
    box(pos=vec(x * 1.5, 0, 0), color=color.cyan)

def clicked(evt):
    thing = scene.mouse.pick
    if thing is None:
        print("clicked empty space")
    else:
        thing.color = color.red
        print("clicked the box at", thing.pos)

scene.bind("click", clicked)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[2, "CLICK", [1.5, 0, 0]], [4, "CLICK", [0.75, 0.1, 0]]],
   "predict": "The first click lands on the box whose pos is <code>&lt;1.5, 0, 0&gt;</code>. The second lands in the gap between that box and the middle one. What does the program print for each click, and does any box change colour on the second click?",
   "reveal": "First click: it prints <code>clicked the box at &lt;1.5, 0, 0&gt;</code>, and that box turns red. The pick is the box, so the else branch runs.</p><p>Second click: it prints <code>clicked empty space</code>. The pick is None, the gate on None is True, and the else branch does not run, so no box changes colour."},

  {"title": "Buttons and sliders",
   "teach": "A <b>widget</b> is a control that appears under the scene: a button, a slider, a checkbox, a menu. Each one is made with a function call, and each takes a <code>bind=</code> argument naming the function to run when the widget is used.</p><p>The bound function receives the widget itself. For a slider, <code>s.value</code> is the number it is set to. For a button there is nothing to read: the click is the message.</p><p><code>scene.append_to_caption</code> adds words under the scene, so the slider has a label beside it. The Reset button puts the ball's pos and radius back to their starting values, however many times the ball was nudged.",
   "code": code('''
from vpython import *

ball = sphere(color=color.magenta)

def reset(b):
    ball.pos = vec(0, 0, 0)
    ball.radius = 1
    print("Reset clicked: pos", ball.pos, " radius", ball.radius)

def resize(s):
    ball.radius = s.value
    print("slider moved to", s.value)

def nudge(evt):
    if evt.key == "right":
        ball.pos.x = ball.pos.x + 1
        print("nudged to", ball.pos)

button(text="Reset", bind=reset)
scene.append_to_caption("   Size: ")
slider(min=0.2, max=3, value=1, bind=resize)
scene.bind("keydown", nudge)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[2, "KEYDOWN", "right"], [3, "KEYDOWN", "right"], [5, "WIDGET", "resize", 2.5], [7, "WIDGET", "reset"]],
   "predict": "The right arrow is pressed twice, the slider is dragged to 2.5, and then Reset is clicked. Where is the ball, and how big is it, after each of those four events?",
   "reveal": "After the first press the pos is <code>&lt;1, 0, 0&gt;</code>. After the second it is <code>&lt;2, 0, 0&gt;</code>. The radius is still 1 for both, because <code>nudge</code> touches only x.</p><p>The slider sets the radius to 2.5, and the ball grows but stays at x = 2, because <code>resize</code> touches only the radius.</p><p>Reset puts the pos back to <code>&lt;0, 0, 0&gt;</code> and the radius back to 1, and the last output line shows both. The slider's knob stays where you dragged it, because the program did not move it. Drag it again and the ball grows again."},
 ],
 "hinge": {"q": "Two students each built a box that moves with the arrow keys. One box jumps one step per tap and stays still when the key is held down. The other box glides while the key is held and stops when it is let go. Which pattern did each student use: a bound keydown function from chunk 5, or <code>keysdown()</code> inside the loop from chunk 6? Then say which pattern you would pick for a game where one tap moves the player exactly one tile.",
           "a": "The box that jumps once per tap uses a bound keydown function. VPython calls the function once for each press, and holding the key down is not another press.</p><p>The box that glides uses <code>keysdown()</code> inside the loop. The gate runs again on every pass, and the key is in the list on every pass while it is held, so the box moves 30 times a second.</p><p>For one tile per tap, pick the bound keydown function, because one press should mean exactly one move."},
 "brief": {
   "title": "Build: a block builder",
   "minutes": 10,
   "intro": "You are making a small building game. There is a green floor, 16 wide and 16 deep, with its top face at y = 0. A left-click on the floor puts a block there, standing on the floor. A click on a block that is already standing puts a new block on top of it. A paint pot block in the corner holds the colour of the next block, and a menu under the scene changes it. A Reset button clears the floor. The camera still turns with a right-drag and zooms with the scroll wheel, so a builder can walk around the model.",
   "steps": [
     "Start from the card below: the floor, the three camera lines, the <code>build</code> function bound to <code>\"click\"</code>, and the loop.",
     "Add a paint pot: <code>pot = box(pos=vec(-7, 0.5, 7), color=color.red)</code>, above the function. In <code>build</code>, give each new block <code>color=pot.color</code>. Then add <code>menu(choices=[\"Red\", \"Blue\", \"Yellow\", \"White\"], bind=pick_colour)</code> under the scene. Its bound function gets the menu as <code>m</code>, and <code>m.selected</code> is the chosen word. Four flat gates, one per word, each assigning <code>pot.color</code>.",
     "Stacking: in <code>build</code>, add a second gate for a click on a block. When the pick is not None and is not the floor and is not the pot, place the new block at <code>hit.pos + vec(0, 1, 0)</code>.",
     "Reset: make an empty list <code>blocks = []</code> above the function, and append every block you place: <code>blocks.append(box(...))</code>. A Reset button's function loops over the list, sets <code>b.visible = False</code> on each block, then empties the list with <code>blocks.clear()</code>.",
     "Put a caption above the scene that says what a left-click does and what a right-drag does.",
   ],
   "cards": [
     {"title": "Where on the floor did the click land?",
      "teach": "The pick says which object was clicked. It does not say where on that object. <code>scene.mouse.project</code> answers that: it finds the point where the click lands on a flat plane. <code>normal=vec(0, 1, 0)</code> says the plane faces up, and <code>point=vec(0, 0, 0)</code> says it passes through the middle of the world, which is where the floor's top face is. <code>round</code> moves each number to the nearest whole number, so the blocks line up on a grid.</p><p>The three camera lines matter. <code>scene.forward</code> tilts the camera so it looks down at the floor instead of straight along it. <code>scene.autoscale = False</code> and <code>scene.range = 8</code> stop the camera from zooming out on its own every time a block is added.",
      "code": code('''
from vpython import *

scene.caption = "Click the floor to place a block."
scene.autoscale = False
scene.range = 8
scene.forward = vec(0, -0.6, -1)
floor = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 16), color=color.green)

def build(evt):
    hit = scene.mouse.pick
    if hit is floor:
        spot = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0, 0))
        print("floor click at", spot)
        box(pos=vec(round(spot.x), 0.5, round(spot.z)), color=color.red)
        print("block placed at", vec(round(spot.x), 0.5, round(spot.z)))

scene.bind("click", build)

while True:
    rate(30)
'''),
      "run": "vpython",
      "frames": 6,
      "inject": [[2, "CLICK", [3.2, 0, -1.8]], [4, "CLICK", [3.2, 0.5, -1.8]], [5, "CLICK", [-6.49, 0, 6.51]]],
      "predict": "Three clicks. The first lands on the floor at (3.2, 0, -1.8). The second lands on the block that the first click placed. The third lands on the floor at (-6.49, 0, 6.51). How many blocks are standing at the end, and where is the third click's block?",
      "reveal": "Two blocks are standing. The first click prints the floor point and places a block at <code>&lt;3, 0.5, -2&gt;</code>: 3.2 rounds to 3, -1.8 rounds to -2, and y is 0.5 so the bottom of the block sits on the floor.</p><p>The second click lands on that block, so the pick is the block, not the floor. The gate is False, and nothing is printed or placed. Stacking on top is step 3 of the brief.</p><p>The third click's block is at <code>&lt;-6, 0.5, 7&gt;</code>: -6.49 rounds to -6, and 6.51 rounds to 7."},
   ],
   "expected_got": [
     ["A block placed on the floor stands on it, not half under it", ""],
     ["Clicking a standing block puts the new block on top of it, not inside it", ""],
     ["Picking Blue in the menu changes the next block and leaves the standing blocks alone", ""],
     ["Reset hides every placed block and leaves the floor and the paint pot", ""],
     ["A right-drag turns the camera and places nothing", ""],
   ],
 },
 "exits": {
   "floor": "A floor, the three axis arrows, and three blocks placed by typing their pos, each standing on the floor and not sunk into it. One key that recolours one of the blocks.",
   "middle": "The block builder: click the floor to place a block, click a block to stack one on top, the paint pot and the menu for colour.",
   "stretch": "A Delete mode checkbox under the scene. While it is ticked, a click on a block sets its <code>visible</code> to False instead of stacking. Then a <code>wtext</code> under the scene that shows how many blocks are standing, updated by every click and by Reset.",
 },
 "ledger": "Stamp 1: <code>from vpython import *</code>, <code>vec(x, y, z)</code> with x right, y up, z toward you, <code>pos</code> is the middle, <code>while True:</code> with <code>rate(30)</code> in it, <code>scene.bind(\"keydown\", f)</code> and <code>evt.key</code>, <code>keysdown()</code> inside the loop, <code>scene.mouse.pick</code> and the gate on None, <code>button</code> and <code>slider</code> with <code>bind=</code>.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 to 3, the world and vec, 18 min (chunk 3 is where the sinking crate gets fixed; do not skip it)",
     "0:28 chunk 4, the loop, 7 min",
     "0:35 chunks 5 and 6, keys, 18 min",
     "0:53 chunks 7 and 8, clicks and widgets, 17 min",
     "1:10 hinge question, 5 min",
     "1:15 build brief, 10 min (most rooms place blocks on the floor and stop; stacking is the middle exit)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Presses a key and nothing happens.", "The tab does not have the focus. Click inside the 3D scene first. If that does not fix it, look at the terminal: if the prompt is back, the program has finished. It needs the loop at the bottom to keep running."],
     ["Puts a block at y = 0, sees it half under the floor, and says the floor is broken.", "pos is the middle. Ask where the bottom of a box 1 tall is when its middle is at 0, then have them print <code>crate.pos.y - crate.size.y / 2</code> as chunk 3 does."],
     ["Expects the up arrow to lift the box.", "In chunk 6 the up arrow changes z, which is toward you and away from you. Have them change that gate to <code>player.pos.y</code>, run it, and say which arrow now does which."],
     ["Writes <code>scene.bind(\"keydown\", paint())</code> with brackets.", "The brackets call <code>paint</code> once, now, with no event, and Python stops with <code>TypeError: paint() missing 1 required positional argument: 'evt'</code>. bind wants the function's name without brackets, so that VPython can call it later."],
     ["Makes a box inside the loop and the tab slows to a crawl.", "<code>box(...)</code> inside the loop makes 30 boxes a second. Make things above the loop, or inside a bound function, which runs once per click."],
     ["Says Reset deleted the blocks because they vanished.", "<code>visible = False</code> hides a block. The list still holds it until the list is cleared, and a hidden block still counts. That is why step 4 clears the list."],
   ],
   "standards": ["NY-5.G.1", "NY-6.NS.6", "MP6"],
   "routing": "The build brief is the first thing to cut. Chunks 1 to 7 are the lesson, and the paint pot, the menu, and Reset can be a second session. If the room has not used <code>def</code> before, stop at chunk 4 and do chunk 5 on the projector, with students calling out which gate is True for each key.",
   "setup": "VPython 7.6.5 installs with <code>pip install vpython</code> and runs on Python 3.8 to 3.12. On a newer Python the import fails before anything is drawn, with <code>ModuleNotFoundError: No module named 'pkg_resources'</code>; as of October 2026 the fix is on GitHub but not yet released, so keep the room on Python 3.12 and, if the error appears, run <code>pip install \"setuptools&lt;81\"</code> once. Key events do not reach a program that runs inside a Jupyter notebook, so run every file from the VS Code terminal. The output boxes on this page come from running each snippet against the installed library with no browser open and the keys and clicks fed in by the build script. The picture itself is not checked, so run the page's programs once on the projector machine before class.",
 },
},

# =====================================================================
{
 "num": 2,
 "slug": "session02_shapes_and_a_model_from_a_function",
 "title": "Shapes, and a model built by a function",
 "subtitle": "Cylinders and cones that point somewhere, colours that are three numbers, and a function that builds a tree wherever you ask",
 "new": ["cylinder and cone", "axis", "pyramid", "colours as vec(r, g, b)", "opacity", "a function that makes objects", "one number that sets every size", "a model kept in a list"],
 "reuse": "Session 1: vec, pos, size, keysdown inside the loop, and a function with a parameter",
 "env_note": True,
 "reuse_note": "The new idea is that a function can make objects, not only print or return. Students who have only used def to compute a number will expect make_tree to give something back. Say in chunk 3 that this function's job is the side effect: after the call, there are two more objects in the world.",
 "opener": {
   "title": "Retrieval: places, the middle, and binding",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "In <code>vec(x, y, z)</code>, which number is up, and which is toward you?",
      "a": "y is up. z is toward you, out of the screen. x is to the right. A negative number goes the other way."},
     {"q": "A box 1 tall has its pos at y = 0, and the floor's top face is at y = 0. What does it look like, and what is the fix?",
      "a": "Half of the box is under the floor, because pos is the middle of the box. The fix is pos.y = 0.5, half the height, so the bottom face is on the floor."},
     {"q": "<code>scene.bind(\"keydown\", paint)</code> has no brackets after paint. Why not, and who calls paint?",
      "a": "Brackets would call paint right now, once, with no event. Without them you are naming the function so VPython can call it later. VPython calls it every time a key goes down, and passes the event as the argument."},
   ],
 },
 "chunks": [
  {"title": "A cylinder starts at pos and points along its axis",
   "teach": "A <b>cylinder</b> is a tube. Its <code>pos</code> is the middle of its bottom face, not the middle of the tube, and its <b>axis</b> is a vector that says which way it points and how long it is. <code>axis=vec(0, 3, 0)</code> is a tube 3 tall pointing straight up. <code>mag</code> gives the length of a vector.</p><p>A <b>cone</b> works the same way: pos is the middle of its flat end, and axis goes from there to the point. To stack a cone on a cylinder, start the cone where the cylinder ends, at <code>pos + axis</code>.",
   "code": code('''
from vpython import *

post = cylinder(pos=vec(0, 0, 0), axis=vec(0, 3, 0), radius=0.5, color=color.orange)
print("post starts at", post.pos)
print("post axis is", post.axis, "so its length is", mag(post.axis))
print("the top of the post is at", post.pos + post.axis)

roof = cone(pos=post.pos + post.axis, axis=vec(0, 1.5, 0), radius=0.8, color=color.red)
print("roof starts at", roof.pos, "and its point is at", roof.pos + roof.axis)
'''),
   "run": "vpython",
   "predict": "The post's axis is <code>vec(0, 3, 0)</code> and the roof's axis is <code>vec(0, 1.5, 0)</code>. Where is the top of the post, and where is the point of the roof?",
   "reveal": "The top of the post is at <code>&lt;0, 3, 0&gt;</code>: pos plus axis. The point of the roof is at <code>&lt;0, 4.5, 0&gt;</code>: the roof starts at the top of the post and its axis adds 1.5 more.</p><p>A box and a sphere put their pos in the middle. A cylinder, a cone and an arrow put it at one end. That is the one thing to remember when a shape lands somewhere you did not expect."},

  {"title": "A colour is three numbers",
   "teach": "<code>color.red</code> is not a special kind of value. It is a vector: how much red, how much green, how much blue, each from 0 to 1. <code>vec(1, 0, 0)</code> is red. <code>vec(1, 1, 0)</code> is red and green mixed, which is yellow. <code>vec(0, 0, 0)</code> is black and <code>vec(1, 1, 1)</code> is white.</p><p>Because a colour is a vector, you can do arithmetic on it. Multiplying by 0.5 halves all three numbers, which makes the same colour darker.</p><p><b>opacity</b> says how solid a shape looks: 1 is solid and 0 is invisible. 0.3 is glass you can see through.",
   "code": code('''
from vpython import *

print("red is", color.red)
print("yellow is", color.yellow)
print("orange is", color.orange)

purple = vec(0.6, 0, 0.8)
ball = sphere(pos=vec(-2, 0, 0), color=purple)
glass = box(pos=vec(2, 0, 0), size=vec(2, 2, 2), color=color.cyan, opacity=0.3)
print("the ball's colour is", ball.color)
print("the glass box has opacity", glass.opacity)

ball.color = ball.color * 0.5
print("half as bright:", ball.color)
'''),
   "run": "vpython",
   "predict": "Yellow is red and green mixed. What three numbers does <code>color.yellow</code> print? And what does multiplying the purple by 0.5 do to each of its three numbers?",
   "reveal": "Yellow prints as <code>&lt;1, 1, 0&gt;</code>: full red, full green, no blue. Orange is <code>&lt;1, 0.6, 0&gt;</code>, full red with some green.</p><p>Multiplying by 0.5 halves each number: <code>&lt;0.6, 0, 0.8&gt;</code> becomes <code>&lt;0.3, 0, 0.4&gt;</code>. The mix is the same, so it is still purple, and every number is smaller, so it is darker. In the tab, look through the glass box at the ball behind it."},

  {"title": "A function that makes a tree",
   "teach": "A function can make objects. <code>make_tree(x, z)</code> makes a trunk and a top at the place you give it. It has no return line, because its job is what it leaves behind in the world: two new objects every time it is called.</p><p>The two parameters are the only things that change from tree to tree. Everything else, the trunk's radius, the colours, the height, is written once inside the function.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)

def make_tree(x, z):
    trunk = cylinder(pos=vec(x, 0, z), axis=vec(0, 1, 0), radius=0.2, color=vec(0.5, 0.3, 0.1))
    top = cone(pos=vec(x, 1, z), axis=vec(0, 2, 0), radius=0.8, color=color.green)
    print("tree at x =", x, " z =", z, "  the top's point is at", top.pos + top.axis)

make_tree(-4, 0)
make_tree(3, -2)
make_tree(5, 4)
'''),
   "run": "vpython",
   "predict": "The function is called three times. How many objects are in the world after the third call, counting the ground? And how high is the point of every tree?",
   "reveal": "Seven objects: the ground, and two for each of the three trees. Every tree's point is at y = 3: the trunk is 1 tall and the top's axis adds 2, and neither number depends on x or z. The output box shows y = 3 on all three lines, with x and z matching each call."},

  {"title": "One number sets every size",
   "teach": "A rocket is a cylinder body, a cone nose, and a fin. If every part's size is worked out from one number, <code>height</code>, then changing that number changes the whole rocket and the parts still fit. The body's radius is <code>height / 6</code>. The nose is <code>height / 3</code> long. Expressions with a letter in them, like these, are what let one number drive a model.</p><p>A <b>pyramid</b> is the fin. Its pos is the middle of its base, like a cylinder, and its <code>size</code> is length along the axis, then height, then width.",
   "code": code('''
from vpython import *

def make_rocket(x, height):
    body = cylinder(pos=vec(x, 0, 0), axis=vec(0, height, 0), radius=height / 6, color=color.white)
    nose = cone(pos=vec(x, height, 0), axis=vec(0, height / 3, 0), radius=height / 6, color=color.red)
    fin = pyramid(pos=vec(x, height / 4, 0), size=vec(height / 4, height / 2, 0.2), axis=vec(1, 0, 0), color=color.red)
    print("rocket", height, "tall:  body radius", body.radius, "  nose tip at y =", nose.pos.y + nose.axis.y)

make_rocket(-3, 3)
make_rocket(3, 6)
'''),
   "run": "vpython",
   "predict": "The second rocket's height is twice the first. Is its body radius twice as big? Is its nose tip twice as high?",
   "reveal": "Both double. The body radius goes from 0.5 to 1.0, because <code>height / 6</code> doubles when height doubles. The nose tip goes from y = 4 to y = 8: the body's height plus a third of it, and both parts double.</p><p>The point of writing <code>height / 6</code> instead of <code>0.5</code> is that the 0.5 would still be 0.5 on the bigger rocket, and the body would be a thin stick."},

  {"title": "A model kept in a list moves as one thing",
   "teach": "Three objects make a car. Put them in a list and a loop can do the same thing to every part. Adding the same vector to every part's pos moves the whole car without changing the distances between its parts.",
   "code": code('''
from vpython import *

parts = []
parts.append(box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.blue))
parts.append(sphere(pos=vec(0, 1.3, 0), radius=0.4, color=color.yellow))
parts.append(cone(pos=vec(1, 0.5, 0), axis=vec(1, 0, 0), radius=0.5, color=color.red))
print(len(parts), "parts")

for part in parts:
    part.pos = part.pos + vec(0, 0, -3)

for part in parts:
    print("part now at", part.pos)
'''),
   "run": "vpython",
   "predict": "Before the loop, the sphere is 0.8 above the box's middle. After the loop, how far above the box's middle is it, and which of the three pos numbers changed for every part?",
   "reveal": "Still 0.8 above: the box's middle is at y = 0.5 and the sphere at y = 1.3, both unchanged. Only z changed, from 0 to -3, on all three parts, because the vector added had zeros for x and y.</p><p>That is the reason for the list. One loop, one vector, and the car is somewhere else in one piece."},

  {"title": "The arrow keys move the whole model",
   "teach": "This is session 1's held-key loop with the list from chunk 5 inside it. The four gates do not move anything themselves. They set <code>move</code>, and the loop over the parts adds <code>move</code> to every part. When no key is held, <code>move</code> stays <code>vec(0, 0, 0)</code>.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene, then hold an arrow key."
ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)
parts = []
parts.append(box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.blue))
parts.append(sphere(pos=vec(0, 1.3, 0), radius=0.4, color=color.yellow))
parts.append(cone(pos=vec(1, 0.5, 0), axis=vec(1, 0, 0), radius=0.5, color=color.red))
speed = 0.2

while True:
    rate(30)
    keys = keysdown()

    move = vec(0, 0, 0)
    if "right" in keys:
        move = vec(speed, 0, 0)
    if "left" in keys:
        move = vec(-speed, 0, 0)
    if "up" in keys:
        move = vec(0, 0, -speed)
    if "down" in keys:
        move = vec(0, 0, speed)

    for part in parts:
        part.pos = part.pos + move

    if len(keys) > 0:
        print(keys, " nose is at", parts[2].pos + parts[2].axis)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[2, "HOLD", "right"], [3, "HOLD", "right"], [4, "HOLD", "right"], [6, "HOLD", "down"]],
   "predict": "On a pass where no key is held, what does <code>move</code> hold, and what does the loop over the parts do? Then: the right arrow is held for three passes. Where is the nose of the cone afterwards?",
   "reveal": "With no key held, <code>move</code> is <code>vec(0, 0, 0)</code>, and the loop adds nothing to each part, so the car stays where it is. The loop runs every pass whether a key is held or not.</p><p>After three passes of the right arrow the nose is at <code>&lt;2.6, 0.5, 0&gt;</code>: it started at x = 2 (the cone's pos at 1 plus its axis of 1) and moved 0.2 three times. The down arrow then adds 0.2 to z."},
 ],
 "hinge": {"q": "Two students each built a village of five houses. One wrote <code>make_house(x, z)</code> and called it five times. The other copied the house code five times and changed the numbers in each copy. Now every roof has to turn red. How many lines does each student change? Then: one house has to be twice as big. What does each student do?",
           "a": "Roofs: the first student changes one line, the colour inside <code>make_house</code>, and all five roofs change. The second student changes five lines, one in each copy, and has to find them all.</p><p>Bigger house: the first student adds a parameter, <code>make_house(x, z, size)</code>, and writes each part's size from it, the way chunk 4's rocket does, then passes 2 for that one house. The second student has to work out every new number for the big house by hand."},
 "brief": {
   "title": "Build: a village with a rocket",
   "minutes": 20,
   "intro": "You are making a village on a green ground 20 wide and 20 deep: trees, houses, and one rocket on a launch pad. The trees come from <code>make_tree</code>. The houses come from a function of your own that takes a size. The rocket comes from <code>make_rocket</code>, and its parts live in a list so that holding the up arrow lifts the whole rocket.",
   "steps": [
     "Start with the ground and <code>make_tree</code> from chunk 3. Call it at least four times at different places.",
     "Write <code>make_house(x, z, size)</code>: a box body <code>size</code> wide and <code>size</code> tall, with its pos lifted by half its height so it stands on the ground, and a pyramid roof on top whose base is the same width. Start from the card below. Call it three times with different sizes.",
     "Change <code>make_rocket</code> so that it appends its three parts to a list called <code>rocket</code> instead of printing, and call it once.",
     "Add the loop from chunk 6 at the bottom. Holding the up arrow adds <code>vec(0, 0.2, 0)</code> to every part of the rocket. Holding down subtracts it.",
     "Add a caption above the scene that says what the up arrow does.",
   ],
   "cards": [
     {"title": "A house whose size is one number",
      "teach": "The body is a box, so its pos is its middle, and it has to be lifted by half its height to stand on the ground. The roof is a pyramid pointing up: its pos is the middle of its base, which is the top face of the body, and its axis points along y.",
      "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)

def make_house(x, z, size):
    body = box(pos=vec(x, size / 2, z), size=vec(size, size, size), color=color.white)
    roof = pyramid(pos=vec(x, size, z), size=vec(size / 2, size, size), axis=vec(0, 1, 0), color=color.red)
    print("house of size", size, " body bottom at y =", body.pos.y - body.size.y / 2, " roof point at y =", roof.pos.y + roof.size.x)

make_house(-5, 0, 1)
make_house(0, 0, 2)
make_house(6, 0, 3)
'''),
      "run": "vpython",
      "predict": "Three houses of size 1, 2 and 3. Where is the bottom of each body? And how high is the point of the size 3 roof compared with the size 1 roof?",
      "reveal": "Every body's bottom is at y = 0.0, because each pos is lifted by exactly half its own height. The size 3 roof's point is at y = 4.5 and the size 1 roof's at y = 1.5: three times as high, because every number comes from <code>size</code>.</p><p>The roof's <code>size.x</code> is its length along the axis, which points up here, so <code>roof.pos.y + roof.size.x</code> is where the point is."},
   ],
   "expected_got": [
     ["Every tree's point is at the same height", ""],
     ["The size 2 house is twice as tall as the size 1 house, roof included", ""],
     ["Holding up lifts all three rocket parts together", ""],
     ["Letting go of up leaves the rocket where it is", ""],
     ["No part of any house or rocket is under the ground", ""],
   ],
 },
 "exits": {
   "floor": "A snowman: three spheres of different radius stacked by typing each pos, and a cone nose pointing along x. No part sunk into the ground.",
   "middle": "The village: <code>make_tree</code> called four times, <code>make_house</code> with a size called three times, and a rocket whose parts lift together with the up arrow.",
   "stretch": "A second rocket twice as tall from the same function, kept in its own list. Up lifts the first rocket and w lifts the second. Then make the ground a list of nine grass boxes in a 3 by 3 pattern, built by two loops.",
 },
 "ledger": "Stamp 2: a cylinder or cone starts at <code>pos</code> and points along <code>axis</code>, the far end is <code>pos + axis</code>, <code>mag</code> is a vector's length, a colour is <code>vec(r, g, b)</code> from 0 to 1, <code>opacity</code>, a function can make objects, one <code>height</code> that every size is worked out from, a model is a list of parts.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 and 2, cylinders and colours, 15 min",
     "0:25 chunk 3, the tree function, 12 min (say what a function with no return is for)",
     "0:37 chunk 4, the rocket, 13 min (the core of the session)",
     "0:50 chunks 5 and 6, the list, 15 min",
     "1:05 hinge question, 5 min",
     "1:10 build brief, 15 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Puts a cylinder's pos in the middle of where the tube should be, so the tube pokes out one end.", "pos is the bottom face for a cylinder, cone and arrow. Have them print <code>pos + axis</code> and say where that point is in the tab."],
     ["Writes <code>make_tree(-4, 0)</code> inside the function body, indented, and nothing appears.", "The call is inside the definition, so it never runs. The call goes at the left edge, after the function, the way chunk 3 shows."],
     ["Writes the rocket's radius as 0.5 and the big rocket is a thin stick.", "Ask which numbers in the function depend on height. Every size must be worked out from height or the parts stop fitting."],
     ["Appends the parts to the list but moves only <code>parts[0]</code>.", "Print each part's pos after a move. The loop over the list is what moves all of them."],
     ["Expects <code>color.red * 2</code> to be a brighter red.", "Each number is already at its top value of 1. Print it: <code>&lt;2, 0, 0&gt;</code> is drawn the same as <code>&lt;1, 0, 0&gt;</code>. Darker is possible, brighter than 1 is not."],
   ],
   "standards": ["NY-6.EE.2", "NY-5.G.1", "MP7"],
   "routing": "Chunk 2 (colours) can be cut to five minutes: show the three prints and move on. Chunk 4 cannot be cut; it is the reason for the session. If the room is slow, the build stops at step 2 and the rocket becomes the stretch.",
 },
},

# =====================================================================
{
 "num": 3,
 "slug": "session03_velocity_gravity_and_bouncing",
 "title": "Motion: velocity, gravity, and bouncing",
 "subtitle": "A ball that moves because it has a velocity, falls because gravity changes that velocity, and bounces because one gate flips a sign",
 "new": ["velocity as a vector", "dt", "gravity changes velocity", "the floor gate", "flipping a sign to bounce", "losing speed on each bounce", "keys that push instead of move", "round(x, 2)"],
 "reuse": "Session 1: the loop with rate(30), keysdown, and pos.y on its own. Session 2: vector arithmetic",
 "env_note": True,
 "reuse_note": "The whole session is two lines, <code>vel = vel + gravity * dt</code> and <code>ball.pos = ball.pos + vel * dt</code>, and a gate. Keep saying which line changes the velocity and which line changes the position. Students who mix them up write gravity into pos and get a ball that falls at one speed.",
 "opener": {
   "title": "Retrieval: the loop, the middle, and vectors",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "What does <code>rate(30)</code> do, and what goes wrong without it?",
      "a": "It pauses the loop so that it runs 30 passes a second and no more. Without it the loop runs as fast as the computer can and the tab has no time to draw."},
     {"q": "The loop adds 0.1 to <code>ball.pos.x</code> on every pass. How far does the ball move in one second, and what is the one number to change to make it move twice as fast?",
      "a": "3 units: 30 passes, 0.1 each. Change the 0.1 to 0.2. Today that number gets a name, velocity, and its own vector."},
     {"q": "What is <code>vec(2, 0, 0) + vec(0, 3, 0)</code>? And why does a cone's pos plus its axis give the point of the cone?",
      "a": "<code>&lt;2, 3, 0&gt;</code>: each number adds to its partner. The cone's pos is its flat end and its axis is the vector from there to the point, so adding them gives where the point is."},
   ],
 },
 "chunks": [
  {"title": "Velocity is a vector, and dt is a slice of a second",
   "teach": "<b>Velocity</b> is how far something moves in one second, and in which direction. <code>vel = vec(2, 0, 0)</code> means 2 units to the right every second.</p><p>The loop runs 30 passes a second, so each pass is one thirtieth of a second. That slice is called <code>dt</code>. On each pass the ball moves <code>vel * dt</code>: the velocity, scaled down to one pass. After 30 passes the ball has moved exactly <code>vel</code>.",
   "code": code('''
from vpython import *

ball = sphere(pos=vec(-5, 0, 0), radius=0.5, color=color.yellow)
vel = vec(2, 0, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + vel * dt
    if passes == 30:
        print("after 1 second the ball is at", ball.pos)
    if passes == 60:
        print("after 2 seconds the ball is at", ball.pos)
'''),
   "run": "vpython",
   "frames": 60,
   "predict": "The ball starts at x = -5 and its velocity is 2 to the right. Where is it after one second, and after two?",
   "reveal": "After one second it is at <code>&lt;-3, 0, 0&gt;</code>, and after two at <code>&lt;-1, 0, 0&gt;</code>. Two units per second, so two seconds moves it four.</p><p>Session 1 wrote <code>ball.pos.x + 0.1</code>. This does the same thing with the speed written as a whole number per second, so you can read the speed straight off the program."},

  {"title": "Gravity changes the velocity, and the velocity changes the position",
   "teach": "Gravity is not a push on the position. It is a change to the velocity: on every pass, the downward speed grows by a little. Then the velocity, which is now bigger, moves the ball. Two lines, in that order.</p><p><code>gravity = vec(0, -9.8, 0)</code> is the real value: a falling thing gains 9.8 units of speed every second. After 30 passes the ball falls at 9.8 per second.</p><p><code>round(x, 2)</code> keeps two decimal places, so the printed numbers are readable.",
   "code": code('''
from vpython import *

ball = sphere(pos=vec(0, 5, 0), radius=0.5, color=color.yellow)
vel = vec(0, 0, 0)
gravity = vec(0, -9.8, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1

    vel = vel + gravity * dt
    ball.pos = ball.pos + vel * dt

    if passes in [10, 20, 30]:
        print("pass", passes, "  falling at", round(-vel.y, 2), "per second   height", round(ball.pos.y, 2))
'''),
   "run": "vpython",
   "frames": 30,
   "predict": "Gravity adds the same amount to the speed on every pass. How fast is the ball falling after 30 passes? And does the height drop by more between passes 20 and 30 than between passes 10 and 20?",
   "reveal": "After 30 passes it falls at 9.8 per second, the gravity number, because one second of passes has gone by. It falls at 3.27 after 10 passes and 6.53 after 20, so the speed grows by the same 3.27 each ten passes.</p><p>The height drops by 1.69 between passes 10 and 20, and by 2.77 between 20 and 30. More, because the ball is going faster by then. The speed changes evenly; the height does not."},

  {"title": "The floor gate flips the sign",
   "teach": "A bounce is one gate. When the ball is below the floor, put it back on the floor and turn its downward velocity into an upward one. <code>vel.y = -vel.y</code> does that: a speed of -9.47 becomes +9.47, the same size in the opposite direction.</p><p>The gate compares <code>ball.pos.y</code> with <code>ball.radius</code>, not with 0, because pos is the middle of the ball and the bottom of the ball touches the floor when the middle is one radius up.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
ball = sphere(pos=vec(0, 5, 0), radius=0.5, color=color.yellow)
vel = vec(0, 0, 0)
gravity = vec(0, -9.8, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1

    vel = vel + gravity * dt
    ball.pos = ball.pos + vel * dt

    if ball.pos.y < ball.radius:
        ball.pos.y = ball.radius
        vel.y = -vel.y
        print("bounce on pass", passes, "  going up at", round(vel.y, 2), "per second")
'''),
   "run": "vpython",
   "frames": 100,
   "predict": "The ball reaches the floor at about 9.5 per second. What is <code>vel.y</code> right after the first bounce? And on the second bounce, is the ball going faster, slower, or the same?",
   "reveal": "Right after the first bounce <code>vel.y</code> is 9.47: the same number with the sign flipped, so the ball goes up as fast as it came down. The second bounce, on pass 86, is at 9.15, a little slower. No line in the program takes speed away on purpose. The small loss comes from the line <code>ball.pos.y = ball.radius</code>: the ball had gone a little under the floor, that bit of the move is thrown away when the ball is put back on the floor, and the speed that bit would have cost is lost with it.</p><p>That line still has to be there. Without it the ball can still be under the floor on the next pass, the gate opens again, the sign flips back, and the ball is stuck in the floor."},

  {"title": "Walls are the same gate, on x",
   "teach": "A wall on the right is at x = 5. The ball's edge reaches it when its middle is at <code>5 - ball.radius</code>. Flip <code>vel.x</code> there, and flip it again at the left wall. The pattern is the floor gate with x in place of y.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
wall_left = box(pos=vec(-5, 1, 0), size=vec(0.2, 2, 10), color=color.gray(0.7))
wall_right = box(pos=vec(5, 1, 0), size=vec(0.2, 2, 10), color=color.gray(0.7))
ball = sphere(pos=vec(0, 0.5, 0), radius=0.5, color=color.yellow)
vel = vec(6, 0, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + vel * dt

    if ball.pos.x > 5 - ball.radius:
        vel.x = -vel.x
        print("hit the right wall on pass", passes, "  vel is now", vel)
    if ball.pos.x < -5 + ball.radius:
        vel.x = -vel.x
        print("hit the left wall on pass", passes, "  vel is now", vel)
'''),
   "run": "vpython",
   "frames": 100,
   "predict": "The ball starts in the middle, moving right at 6 per second. The wall is 5 away, so the ball's edge touches it 4.5 from the start. Which wall does it hit first, and on about which pass?",
   "reveal": "The right wall, on pass 23. At 6 per second, 4.5 units take three quarters of a second, which is 22.5 passes, so pass 23 is the first pass where the ball is past the line. The velocity becomes <code>&lt;-6, 0, 0&gt;</code>.</p><p>The left wall comes 46 passes later, on pass 69, because the ball has to cross the whole room, 9 units, at 6 per second."},

  {"title": "Losing a little speed on every bounce",
   "teach": "A real ball does not bounce back to the same height. Multiply the flipped velocity by a number less than 1 and each bounce is a bit lower than the one before. <code>vel.y = -vel.y * 0.7</code> keeps 7 tenths of the speed.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
ball = sphere(pos=vec(0, 5, 0), radius=0.5, color=color.yellow)
vel = vec(0, 0, 0)
gravity = vec(0, -9.8, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1

    vel = vel + gravity * dt
    ball.pos = ball.pos + vel * dt

    if ball.pos.y < ball.radius:
        ball.pos.y = ball.radius
        vel.y = -vel.y * 0.7
        print("bounce on pass", passes, "  going up at", round(vel.y, 2))
'''),
   "run": "vpython",
   "frames": 130,
   "predict": "The first bounce sends the ball up at about 6.6 per second instead of 9.5. Will the gap between bounces get longer or shorter each time? Will the ball ever stop bouncing?",
   "reveal": "Shorter. A slower ball does not go as high, so it comes back sooner: the bounces are 40 passes apart, then 27, then 18, then 12. The speeds shrink each time: 6.63, 4.5, 3.02, 2.0, 1.34.</p><p>The bounces get smaller and closer together until, after about five seconds, they are too small to see and the ball looks like it is resting on the floor. The program is still bouncing it a tiny amount on every pass. Seven tenths of a small number is a smaller number, not zero."},

  {"title": "Keys that push",
   "teach": "In session 1 the arrow keys changed the position. Here they change the velocity. Holding right adds <code>push</code> to <code>vel.x</code> on every pass, so the longer you hold, the faster the ball rolls. Letting go does not stop it, because nothing takes the velocity away.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene, then tap the right arrow."
ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
ball = sphere(pos=vec(0, 0.5, 0), radius=0.5, color=color.yellow)
vel = vec(0, 0, 0)
push = 0.3
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if "right" in keys:
        vel.x = vel.x + push
    if "left" in keys:
        vel.x = vel.x - push

    ball.pos = ball.pos + vel * dt

    if passes in [3, 5, 8]:
        print("pass", passes, "  vel.x =", round(vel.x, 2), "  x =", round(ball.pos.x, 2))
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[2, "HOLD", "right"], [3, "HOLD", "right"], [4, "HOLD", "right"]],
   "predict": "The right arrow is held on passes 2, 3 and 4 and then let go. What is <code>vel.x</code> on pass 5, and on pass 8? Does the ball stop when the key is let go?",
   "reveal": "On pass 5 <code>vel.x</code> is 0.9: three passes of 0.3. On pass 8 it is still 0.9, because no gate opened after pass 4 and nothing subtracts from the velocity. The ball does not stop; x keeps growing, 0.09 at pass 5 and 0.18 at pass 8.</p><p>To make it slow down on its own, multiply <code>vel.x</code> by 0.98 on every pass. That is friction, and it is the stretch exit."},
 ],
 "hinge": {"q": "Program A adds <code>vec(0.1, 0, 0)</code> to the ball's pos on every pass. Program B adds <code>vel * dt</code> with <code>vel = vec(3, 0, 0)</code> and <code>dt = 1 / 30</code>. Both run at <code>rate(30)</code>. Which ball is faster? Now both programs change to <code>rate(60)</code>, and B changes dt to <code>1 / 60</code>. Which ball changes speed?",
           "a": "At rate(30) they are the same speed: A moves 0.1 thirty times a second, which is 3 per second, and B moves 3 per second by definition.</p><p>At rate(60), A doubles to 6 per second, because it still moves 0.1 on each of 60 passes. B stays at 3 per second, because each pass now moves half as much. Writing motion as <code>vel * dt</code> is what keeps the speed you wrote, whatever the rate."},
 "brief": {
   "title": "Build: the bouncy room",
   "minutes": 20,
   "intro": "A ball in a room 10 by 10 with four walls 2 tall. Gravity pulls it down and the floor bounces it with 8 tenths of its speed. The arrow keys push it along x and z. Pressing r puts the ball back at the top with no velocity. The camera is tilted so you can see the floor, and the ball cannot leave the room.",
   "steps": [
     "Start from chunk 5: the ground, gravity, and the floor gate with 0.8 in place of 0.7.",
     "Add the two walls and the two x gates from chunk 4. Then add two walls at z = 5 and z = -5 and the two z gates from the card below.",
     "Add the key gates from chunk 6 for left and right on <code>vel.x</code>, and for up and down on <code>vel.z</code>. Remember that up is negative z.",
     "Add a gate inside the loop: if <code>\"r\"</code> is in the held keys, put the ball at <code>vec(0, 5, 0)</code> and set <code>vel</code> to <code>vec(0, 0, 0)</code>.",
     "Put <code>scene.forward = vec(0, -0.5, -1)</code> above the loop so the camera looks down into the room, and write a caption that names the keys.",
   ],
   "cards": [
     {"title": "The two gates for the z walls",
      "teach": "The far wall is at z = -5 and the near wall at z = 5. They are the x gates with z in place of x and the signs the other way round for the far wall.",
      "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
wall_far = box(pos=vec(0, 1, -5), size=vec(10, 2, 0.2), color=color.gray(0.7))
wall_near = box(pos=vec(0, 1, 5), size=vec(10, 2, 0.2), color=color.gray(0.7), opacity=0.3)
ball = sphere(pos=vec(0, 0.5, 0), radius=0.5, color=color.yellow)
vel = vec(0, 0, -6)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + vel * dt

    if ball.pos.z < -5 + ball.radius:
        vel.z = -vel.z
        print("hit the far wall on pass", passes, "  vel is now", vel)
    if ball.pos.z > 5 - ball.radius:
        vel.z = -vel.z
        print("hit the near wall on pass", passes, "  vel is now", vel)
'''),
      "run": "vpython",
      "frames": 100,
      "predict": "The ball starts moving away from you at 6 per second. Which wall does it hit first, and what is <code>vel</code> after that hit?",
      "reveal": "The far wall, on pass 23, because away from you is negative z and the far wall is at z = -5. After the hit <code>vel</code> is <code>&lt;0, 0, 6&gt;</code>, so the ball comes back toward you. The near wall is see-through, opacity 0.3, so the ball stays visible when it is close to the camera."},
   ],
   "expected_got": [
     ["The ball never sinks below the floor, even after many bounces", ""],
     ["Each bounce is lower than the one before", ""],
     ["The ball cannot leave the room through any of the four walls", ""],
     ["Pushing while the ball is in the air changes where it lands", ""],
     ["r puts the ball back at the top, not moving", ""],
   ],
 },
 "exits": {
   "floor": "A ball that falls with gravity and bounces on the floor, printing its speed at each bounce.",
   "middle": "The bouncy room: four walls, bounces that lose speed, arrow keys that push, r to reset.",
   "stretch": "Friction: multiply <code>vel.x</code> and <code>vel.z</code> by 0.98 on every pass so the ball rolls to a stop. Then a second ball with its own <code>vel2</code>, and a gate that swaps the two velocities when <code>mag(ball.pos - ball2.pos)</code> is less than the two radii added together.",
 },
 "ledger": "Stamp 3: <code>vel</code> is a vector of units per second, <code>dt = 1 / 30</code>, <code>pos = pos + vel * dt</code> moves, <code>vel = vel + gravity * dt</code> changes the speed, the floor gate compares with the radius and flips the sign, <code>* 0.7</code> loses speed, keys that push add to vel, <code>round(x, 2)</code>.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunk 1, velocity and dt, 10 min",
     "0:20 chunk 2, gravity, 12 min (the order of the two lines is the teaching point)",
     "0:32 chunk 3, the floor gate, 13 min",
     "0:45 chunks 4 and 5, walls and losing speed, 15 min",
     "1:00 chunk 6, pushing, 8 min",
     "1:08 hinge question, 7 min",
     "1:15 build brief, 10 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Writes <code>ball.pos = ball.pos + gravity * dt</code> and gets a ball that falls at one steady speed.", "Gravity changes the velocity, not the position. Print <code>vel.y</code> on each pass: in their version it never changes."],
     ["Compares with 0 in the floor gate and half the ball goes under the floor before it bounces.", "pos is the middle. The bottom of the ball is one radius below pos, which is why the gate uses <code>ball.radius</code>."],
     ["Leaves out <code>ball.pos.y = ball.radius</code> and the ball jitters on the floor or sinks through.", "The gate can open twice in a row if the ball is still under the floor on the next pass, and the second flip sends it down again. Putting the ball on the floor makes the gate close."],
     ["Flips <code>vel</code> instead of <code>vel.y</code> at the floor.", "<code>-vel</code> flips all three numbers, so a ball rolling right starts rolling left at every bounce. Only the number for the direction of the wall flips."],
     ["Expects the ball to stop when the arrow key is let go.", "Nothing subtracts from the velocity, so it keeps the speed it has. That is what velocity means. Friction, <code>vel.x * 0.98</code>, is the stretch."],
   ],
   "standards": ["NY-6.EE.9", "NY-6.NS.5", "MP8"],
   "routing": "Chunk 5 can be folded into chunk 3 by changing the 0.7 live on the projector. Keep the hinge's seven minutes; it is the one idea that separates this session from session 1. If the room is behind, the build is chunks 3 and 4 combined and the z walls become the stretch.",
 },
},
]
