"""Sessions 4 to 7 of the VPython course: every word and every snippet.

Same shape as sessions_a.py. render.py runs each snippet through
vpython_harness.py and pastes the real terminal output into the page.
"""


def code(text):
    return text.lstrip("\n").rstrip() + "\n"


SESSIONS_B = [

# =====================================================================
{
 "num": 4,
 "slug": "session04_turning_things_and_the_camera",
 "title": "Turning things, and turning the camera",
 "subtitle": "rotate by an angle, a blade that spins because it turns a little on every pass, a moon that goes around a planet, and a car that drives the way it is facing",
 "new": ["rotate with angle and axis", "degrees and radians", "a counter that measures turning", "rotate with origin", "norm for a direction", "scene.center, scene.range, scene.forward", "scene.camera.follow"],
 "reuse": "Session 1: a bound keydown function and keysdown. Session 2: axis, mag, a model in a list. Session 3: a counter inside the loop",
 "env_note": True,
 "reuse_note": "Radians will confuse the room if they are explained. Do not explain them. <code>radians(30)</code> is how you write 30 degrees to VPython, and the page says nothing more than that. The counter in chunk 2 is the way to check that a turn is the size you meant.",
 "opener": {
   "title": "Retrieval: velocity, the floor gate, and axis",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "Which line changes the velocity and which line changes the position? Say what goes wrong if gravity is added to the position instead.",
      "code": 'vel = vel + gravity * dt\nball.pos = ball.pos + vel * dt',
      "a": "The first line changes the velocity: gravity adds a little downward speed every pass. The second changes the position by the velocity. Added to the position instead, gravity moves the ball down by the same amount every pass, so it falls at one steady speed and never speeds up."},
     {"q": "The bounce line is <code>vel.y = -vel.y</code>. What happens to a ball that was falling at 9 per second?",
      "a": "It goes up at 9 per second. The minus flips the sign and keeps the size, so the direction changes and the speed does not."},
     {"q": "A cylinder has <code>pos=vec(0, 0, 0)</code> and <code>axis=vec(0, 3, 0)</code>. Where is its top, and how tall is it?",
      "a": "The top is at <code>&lt;0, 3, 0&gt;</code>, pos plus axis. It is 3 tall, which is <code>mag(axis)</code>."},
   ],
 },
 "chunks": [
  {"title": "rotate turns a thing around a line through its pos",
   "teach": "<code>blade.rotate(angle=radians(60), axis=vec(0, 0, 1))</code> turns the blade by 60 degrees around a line that points along z and passes through the blade's pos. <code>radians(60)</code> is how you write 60 degrees to VPython. Always write the angle that way; a bare number means something else, and the hinge question is about what.</p><p>A box's <code>axis</code> is a vector along its length. Turning the box turns its axis with it. The length does not change, only the direction.",
   "code": code('''
from vpython import *

blade = box(pos=vec(0, 0, 0), size=vec(4, 0.4, 0.2), color=color.red)
print("blade axis before:", blade.axis, "  length", mag(blade.axis))

blade.rotate(angle=radians(60), axis=vec(0, 0, 1))
print("blade axis after 60 degrees:", blade.axis, "  length", mag(blade.axis))
'''),
   "run": "vpython",
   "predict": "The blade is 4 long, so its axis is <code>&lt;4, 0, 0&gt;</code>. After turning 60 degrees, is the axis longer, shorter, or the same length? Does its x number get bigger or smaller?",
   "reveal": "The same length: 4.0 before and 4.0 after. Turning does not stretch anything.</p><p>The x number gets smaller, from 4 to 2, and the y number grows from 0 to 3.4641. The blade now points up and to the right instead of straight right, so less of its length is along x and some of it is along y. In the tab the blade is tilted like a clock hand at two o'clock."},

  {"title": "A little turn on every pass is a spin",
   "teach": "Turn the blade by 3 degrees on every pass and it spins. A counter called <code>turned</code> adds up the degrees, and a gate on 360 says when one full turn is done. That is how you check that the turn is the size you meant.</p><p>Thirty passes a second at 3 degrees each is 90 degrees a second, so a full turn takes 4 seconds.",
   "code": code('''
from vpython import *

hub = cylinder(pos=vec(0, 0, -0.5), axis=vec(0, 0, 1), radius=0.3, color=color.gray(0.5))
blade = box(pos=vec(0, 0, 0), size=vec(4, 0.4, 0.2), color=color.red)
step = 3
turned = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1

    blade.rotate(angle=radians(step), axis=vec(0, 0, 1))
    turned = turned + step

    if turned == 360:
        print("one full turn after", passes, "passes, which is", passes / 30, "seconds")
        turned = 0
'''),
   "run": "vpython",
   "frames": 240,
   "predict": "3 degrees per pass, 30 passes a second. On which pass is the first full turn finished, and how many seconds is that? What single number change makes the blade spin twice as fast?",
   "reveal": "The first full turn finishes on pass 120, which is 4.0 seconds: 360 divided by 3 is 120 passes. The second finishes on pass 240.</p><p>Change <code>step</code> to 6. Then each pass turns twice as far, the counter reaches 360 on pass 60, and a full turn takes 2 seconds. Nothing else in the program needs to change, because every line uses <code>step</code>."},

  {"title": "rotate with an origin goes around another point",
   "teach": "Add <code>origin=planet.pos</code> and the moon turns around the planet instead of around its own middle. Its pos changes on every pass, and its distance from the planet does not.</p><p>The prints use <code>round(x, 2)</code> from session 3, because a turned position has many decimal places and two are enough to read.",
   "code": code('''
from vpython import *

planet = sphere(pos=vec(0, 0, 0), radius=1, color=color.blue)
moon = sphere(pos=vec(3, 0, 0), radius=0.3, color=color.white)
passes = 0

while True:
    rate(30)
    passes = passes + 1
    moon.rotate(angle=radians(10), axis=vec(0, 1, 0), origin=planet.pos)

    if passes in [3, 6, 9]:
        print("pass", passes, "  moon x =", round(moon.pos.x, 2), "  z =", round(moon.pos.z, 2),
              "  distance from planet", round(mag(moon.pos - planet.pos), 2))
'''),
   "run": "vpython",
   "frames": 9,
   "predict": "The moon starts 3 to the right of the planet and turns 10 degrees per pass around the planet. After 9 passes it has turned 90 degrees. Where is it then, and how far is it from the planet?",
   "reveal": "After 9 passes the moon is at x = 0.0 and z = -3.0: straight behind the planet, away from you, still 3.0 away. The distance is 3.0 on every line, because turning around a point keeps you the same distance from it.</p><p>Without <code>origin=</code>, the moon would turn around its own middle, which for a sphere changes nothing you can see."},

  {"title": "Turn the car with a key, then drive the way it faces",
   "teach": "Left and right are single taps, so they go in a bound function: each tap turns the car 30 degrees around the up direction. Up is held, so it goes in the loop.</p><p>Driving forward means moving along the car's own axis, whichever way that points now. <code>norm(car.axis)</code> is the axis shrunk to length 1, the direction only. Multiply it by 0.2 and you have a move of 0.2 in the direction the car is facing.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene. Left and right turn the car. Up drives it."
ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)
car = box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.red)
start = vec(0, 0.5, 0)

def steer(evt):
    if evt.key == "left":
        car.rotate(angle=radians(30), axis=vec(0, 1, 0))
    if evt.key == "right":
        car.rotate(angle=radians(-30), axis=vec(0, 1, 0))
    print("car now points along", car.axis)

scene.bind("keydown", steer)

while True:
    rate(30)
    keys = keysdown()
    if "up" in keys:
        car.pos = car.pos + norm(car.axis) * 0.2
        print("car at", car.pos, "  distance from start", round(mag(car.pos - start), 2))
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[2, "KEYDOWN", "left"], [4, "HOLD", "up"], [5, "HOLD", "up"]],
   "predict": "Left is tapped once, then up is held for two passes. Is the car 0.4 from where it started? Did it move along x only, or along x and z?",
   "reveal": "It is 0.4 from the start: 0.2 per pass for two passes, whatever direction it faces. The line that moves it uses <code>norm</code>, so the move is always exactly 0.2 long.</p><p>It moved along x and z both. After the left tap the axis is <code>&lt;1.73205, 0, -1&gt;</code>: mostly along x, partly away from you. So each pass moves the car 0.17 along x and 0.1 along negative z, and the output box shows x growing and z going negative together."},

  {"title": "The camera: where it looks and how much it shows",
   "teach": "<code>scene.center</code> is the point the camera looks at, and <code>scene.range</code> is how many units it shows from the middle to the edge. By default the camera zooms out on its own to keep everything in view; <code>scene.autoscale = False</code> stops that, so a car can drive out of sight.</p><p><code>scene.forward</code> is the direction the camera looks. <code>vec(0, -0.5, -1)</code> looks away from you and a bit down, so the ground is seen from above.</p><p>Assigning the car's pos to <code>scene.center</code> moves the camera to look at the car. Doing that on every pass is what <code>scene.camera.follow(car)</code> does in one line.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(40, 0.2, 40), color=color.green)
car = box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.red)
scene.autoscale = False
scene.range = 8
scene.forward = vec(0, -0.5, -1)
print("the camera looks at", scene.center, " and shows", scene.range, "units each way")
passes = 0

while True:
    rate(30)
    passes = passes + 1
    car.pos = car.pos + vec(0.2, 0, 0)

    if passes == 60:
        print("car is at", car.pos, "  camera still looks at", scene.center)
        scene.center = car.pos
        print("after scene.center = car.pos, the camera looks at", scene.center)
'''),
   "run": "vpython",
   "frames": 60,
   "predict": "The view shows 8 units each way and the car drives right at 0.2 per pass. On about which pass does the car leave the view? And where is the camera looking on pass 60, before the center line runs?",
   "reveal": "About pass 40: 8 units at 0.2 per pass is 40 passes, and after that the car is past the right edge. The view does not move to follow it, because autoscale is off.</p><p>On pass 60 the camera still looks at <code>&lt;0, 0, 0&gt;</code> while the car is at x = 12. After <code>scene.center = car.pos</code> the camera looks at <code>&lt;12, 0.5, 0&gt;</code> and the car is back in the middle of the view. Put that line inside the loop, or write <code>scene.camera.follow(car)</code> once above it, and the view stays on the car."},

  {"title": "Turning a whole model",
   "teach": "A model is a list of parts, from session 2. To turn the whole model, rotate every part around the same point: the body's pos. Parts that are not at that point move around it, the way the moon did, and parts at that point turn in place.",
   "code": code('''
from vpython import *

body = box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.red)
parts = [body]
parts.append(sphere(pos=vec(1, 0.5, 0), radius=0.3, color=color.yellow))
parts.append(sphere(pos=vec(-1, 0.5, 0), radius=0.3, color=color.yellow))

for part in parts:
    part.rotate(angle=radians(60), axis=vec(0, 1, 0), origin=body.pos)

for part in parts:
    print("part at x =", round(part.pos.x, 2), " z =", round(part.pos.z, 2))
'''),
   "run": "vpython",
   "predict": "The two lights sit 1 to the right and 1 to the left of the body. After the whole model turns 60 degrees, is the body's pos different? Are the lights still 1 away from the body?",
   "reveal": "The body's pos is the same, x = 0.0 and z = 0.0, because it is at the origin of the turn and a point does not move when you turn around it.</p><p>The lights are still 1 away. The right light is at x = 0.5, z = -0.87 and the left light at x = -0.5, z = 0.87, and each of those is 1 from the middle. They have swung around the body the way the moon swung around the planet. If the loop rotated each part with no origin, every part would turn in place and the lights would stay where they were, beside a body that now points the other way."},
 ],
 "hinge": {"q": "A student writes <code>wheel.rotate(angle=5, axis=vec(0, 0, 1))</code> inside the loop and says the wheel spins far too fast and looks like it is jumping about. What is wrong with the angle, and what is the fix?",
           "a": "The angle has no <code>radians</code> around it, so 5 means 5 radians, which is 286 degrees, rounded to the nearest degree. The wheel turns almost all the way round on every pass, which looks like jumping.</p><p>The fix is <code>angle=radians(5)</code>: 5 degrees per pass, 150 degrees a second. Every angle in a VPython program is written with <code>radians</code> around it."},
 "brief": {
   "title": "Build: drive the car",
   "minutes": 20,
   "intro": "A car on a big green ground. The car is a red body and two yellow lights kept in a list. Left and right turn the whole car. Up drives it the way it faces. The camera follows the car so it never leaves the view. Off to one side there is a windmill whose blade spins on its own.",
   "steps": [
     "Start from the card below: the car as a list of parts, and the <code>turn</code> function that rotates every part around the body.",
     "Bind <code>turn</code> to <code>\"keydown\"</code>. Then put the loop from chunk 4 at the bottom with the up gate changed so that it adds <code>norm(body.axis) * 0.2</code> to every part, not just the body.",
     "Add <code>scene.camera.follow(body)</code> and <code>scene.range = 10</code> above the loop.",
     "Add a windmill at <code>vec(8, 0, -8)</code>: a post from chunk 1 of session 2, and a blade from chunk 2 of this session that turns 3 degrees on every pass.",
     "Write a caption that says what the three keys do.",
   ],
   "cards": [
     {"title": "The turn function for a model in a list",
      "teach": "This is chunk 6's loop inside a bound function, with the angle chosen by the key. The function turns every part around the body's pos, so the lights swing with the body.",
      "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(40, 0.2, 40), color=color.green)
body = box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.red)
parts = [body]
parts.append(sphere(pos=vec(1, 0.5, 0.3), radius=0.2, color=color.yellow))
parts.append(sphere(pos=vec(1, 0.5, -0.3), radius=0.2, color=color.yellow))

def turn(evt):
    angle = 0
    if evt.key == "left":
        angle = radians(30)
    if evt.key == "right":
        angle = radians(-30)
    for part in parts:
        part.rotate(angle=angle, axis=vec(0, 1, 0), origin=body.pos)
    print(evt.key, "  body points along x =", round(body.axis.x, 2), " z =", round(body.axis.z, 2),
          "  first light at x =", round(parts[1].pos.x, 2), " z =", round(parts[1].pos.z, 2))

scene.bind("keydown", turn)

while True:
    rate(30)
'''),
      "run": "vpython",
      "frames": 6,
      "inject": [[2, "KEYDOWN", "left"], [3, "KEYDOWN", "left"], [5, "KEYDOWN", "right"]],
      "predict": "Left is tapped twice, then right once. After the three taps, how far round has the car turned in total? Do the lights stay at the front of the car?",
      "reveal": "30 degrees to the left in total: two left taps make 60, and one right tap takes 30 back. The output box shows the body's axis going to 60 degrees and then back to 30.</p><p>The lights stay at the front. Each tap rotates every part around the body's pos, so a light that was 1 ahead of the body is still 1 ahead of it in the new direction. The last line shows the first light at x = 1.02, z = -0.24, which is in front of a body whose axis is x = 1.73, z = -1.0.</p><p>A tap of any other key sets no angle, so <code>angle</code> stays 0 and <code>rotate</code> does nothing. That is why the function can be bound to every key without a gate around the loop."},
   ],
   "expected_got": [
     ["Left turns the lights with the body, so they stay at the front", ""],
     ["Up moves the car the way it faces, not always along x", ""],
     ["The car never leaves the view", ""],
     ["The windmill blade makes one full turn every 4 seconds", ""],
     ["Up without any turn drives the car straight along x", ""],
   ],
 },
 "exits": {
   "floor": "A windmill: a post and a blade that spins 3 degrees per pass, with the counter that prints when each full turn is done.",
   "middle": "The car: turned by left and right, driven by up, followed by the camera, next to the windmill.",
   "stretch": "Make the lights come on: the space key sets both lights' <code>emissive</code> to True and their colour to white. Then add a wheel sphere on each side that rotates around its own axis while up is held, by an angle that depends on how fast the car is going.",
 },
 "ledger": "Stamp 4: <code>obj.rotate(angle=radians(d), axis=vec(0, 1, 0))</code> turns around a line through pos, add <code>origin=p</code> to go around another point, a counter of degrees checks a spin, <code>norm(v)</code> is a direction of length 1, drive with <code>pos + norm(axis) * speed</code>, <code>scene.center</code>, <code>scene.range</code>, <code>scene.forward</code>, <code>scene.autoscale = False</code>, <code>scene.camera.follow(obj)</code>.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 and 2, rotate and the spin counter, 15 min",
     "0:25 chunk 3, origin, 10 min",
     "0:35 chunk 4, turn and drive, 15 min (norm is the teaching point)",
     "0:50 chunk 5, the camera, 10 min",
     "1:00 chunk 6, turning a model, 8 min",
     "1:08 hinge question, 7 min",
     "1:15 build brief, 10 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Writes <code>angle=30</code> and the thing spins wildly.", "That is the hinge. 30 radians is nearly five full turns. Wrap it: <code>radians(30)</code>."],
     ["Rotates the moon with no origin and sees nothing happen.", "A sphere turning around its own middle looks the same. <code>origin=planet.pos</code> is what makes it go around the planet. Print the moon's pos with and without."],
     ["Drives the car with <code>car.pos.x + 0.2</code> after turning it, so it slides sideways.", "The car's facing is its axis. <code>norm(car.axis) * 0.2</code> is a move in that direction. Print <code>car.axis</code> after a turn and ask which way that vector points."],
     ["Turns only the body in the car build, and the lights are left behind.", "Every part has to rotate around the same origin. The card's loop does that; a rotate on the body alone turns one part."],
     ["Sets <code>scene.range</code> and expects the camera to move.", "range is how much is shown, center is where it looks. Two different numbers. Print both."],
   ],
   "standards": ["NY-4.MD.5", "NY-6.NS.6", "MP6"],
   "routing": "Chunk 6 can be cut, since the card in the build brief teaches the same loop in use. Chunk 5 can be cut to the two lines <code>scene.autoscale = False</code> and <code>scene.camera.follow(car)</code> shown on the projector. The hinge is not cuttable; the radians mistake will appear in the build either way.",
 },
},

# =====================================================================
{
 "num": 5,
 "slug": "session05_a_car_with_wheels_that_roll",
 "title": "A car with wheels that roll along a road",
 "subtitle": "A wheel is a cylinder on its side, one speed moves every part, and the wheels turn by exactly as far as the car travels",
 "new": ["a wheel sits on its radius", "two lists for one model: parts and rolling", "a road built by a loop", "speed in units per second with dt", "rolling: 360 degrees per circumference", "a negative angle rolls backwards", "a loop-back gate that shifts every part"],
 "reuse": "A function that makes objects, a model kept in a list, a cylinder and its axis, dt and a speed, rotate with radians, and the camera lines. Each one is shown again on this page where it is used",
 "env_note": True,
 "reuse_note": "The one new idea is in chunk 5: how far a wheel should turn is worked out from how far the car moved, not picked. Everything before chunk 5 sets that up, and the hinge question checks it. The opener shows the three older ideas the page leans on, turning a shape, the two ends of a cylinder, and a model kept in a list, each with its own code, so the page can be followed on its own.",
 "opener": {
   "title": "Retrieval: turning, the axis, and the loop",
   "minutes": 10,
   "body": "Paper first. Three questions about three ideas today's car is built from: turning a shape, where the two ends of a cylinder are, and moving a model that is kept in a list. Each question shows all the code it asks about.",
   "questions": [
     {"q": "The first line makes a red box and gives it the name <code>car</code>. The second line turns it. Which object turns? What does <code>radians(30)</code> mean, and what goes wrong if the <code>radians</code> is left off?",
      "code": 'car = box(pos=vec(0, 0.5, 0), size=vec(2, 1, 1), color=color.red)\ncar.rotate(angle=radians(30), axis=vec(0, 1, 0))',
      "a": "The red box turns. <code>car</code> is the name the first line gave it, and <code>car.rotate</code> means turn that box: the part before the dot says which object, the part after says what to do. It turns around a line that points up, <code>vec(0, 1, 0)</code>, through the box's middle, so it turns like a car steering on flat ground.</p><p><code>radians(30)</code> is how you write 30 degrees to VPython. Without it the 30 means something much bigger, nearly five full turns, and the box spins far too far."},
     {"q": "A cylinder is made with <code>pos=vec(2, 0, 0)</code> and <code>axis=vec(0, 0, 3)</code>. Where is its other end? Is its pos in the middle of it?",
      "a": "The other end is at <code>&lt;2, 0, 3&gt;</code>, pos plus axis. No: for a cylinder, pos is one flat end, not the middle. A box and a sphere have their pos in the middle, a cylinder does not."},
     {"q": "A model made of a box and a sphere is kept in a list called <code>parts</code>. What does the loop do to each part? After it, is the sphere still 1 to the right of the box?",
      "code": 'parts = [box(pos=vec(0, 0.5, 0)), sphere(pos=vec(1, 0.5, 0), radius=0.3)]\n\nfor part in parts:\n    part.pos = part.pos + vec(2, 0, 0)',
      "a": "It adds <code>vec(2, 0, 0)</code> to each part's pos, so the box and the sphere both move 2 to the right. The sphere is still 1 to the right of the box, because both got the same vector.</p><p>That is why a model is kept in a list. One loop moves every part, however many there are, and the parts stay together. Today's car has nine parts, and every move it makes is a loop like this one."},
   ],
 },
 "chunks": [
  {"title": "A wheel is a cylinder lying on its side",
   "teach": "A wheel is a cylinder whose axis points along z, so its flat faces look left and right and its round side touches the ground. <code>pos</code> is one flat face, not the middle, and <code>pos + axis</code> is the other. The wheel here is 0.3 thick, from z = 0.7 to z = 1.0, which is where the right side of a car 1.4 wide would be.</p><p>How high to put it needs care, because every shape in VPython is placed by its pos. A box 1 tall is lifted by 0.5, half its height. A wheel is lifted by its <b>radius</b>: the lowest point of the round side is the radius below the middle. Radius 0.4 means <code>pos.y = 0.4</code>, and then the wheel just touches a ground whose top is at y = 0.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)
wheel = cylinder(pos=vec(1, 0.4, 0.7), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
print("one face is at", wheel.pos)
print("the other face is at", wheel.pos + wheel.axis)
print("the lowest point of the wheel is at y =", wheel.pos.y - wheel.radius)
'''),
   "run": "vpython",
   "predict": "The wheel's pos is <code>&lt;1, 0.4, 0.7&gt;</code>. Where is its other flat face? And where is the lowest point of the wheel: on the ground, under it, or floating above it?",
   "reveal": "The other face is at <code>&lt;1, 0.4, 1&gt;</code>: pos plus the axis, which adds 0.3 to z and nothing else.</p><p>The lowest point is at y = 0.0, exactly on the ground. The middle of the wheel is 0.4 up and the round side reaches 0.4 below it, the radius. Change the radius to 0.6 and leave pos alone, and the wheel sinks 0.2 into the ground. For a wheel, the lift is the radius."},

  {"title": "Four wheels from one function, into two lists",
   "teach": "<code>add_wheel(x, z)</code> is a function whose job is to make objects: a black cylinder and a white <b>spoke</b> at the place you give it. The spoke is a thin box across the middle of the wheel, so that you can see the wheel turn. A plain black cylinder looks the same whether it is turning or not.</p><p>The function has no return line. It puts what it makes into lists. Every part goes in <code>parts</code>, the list of everything that moves with the car. The spoke also goes in <code>rolling</code>, the list of everything that turns when the car rolls. One object can be in two lists at once.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)
body = box(pos=vec(0, 0.9, 0), size=vec(3, 0.8, 1.4), color=color.red)
parts = [body]
rolling = []

def add_wheel(x, z):
    wheel = cylinder(pos=vec(x, 0.4, z), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
    spoke = box(pos=vec(x, 0.4, z + 0.15), size=vec(0.7, 0.08, 0.32), color=color.white)
    parts.append(wheel)
    parts.append(spoke)
    rolling.append(spoke)

add_wheel(1, 0.7)
add_wheel(-1, 0.7)
add_wheel(1, -1)
add_wheel(-1, -1)
print(len(parts), "parts move with the car")
print(len(rolling), "of them turn when it rolls")
print("the first spoke is at", rolling[0].pos)
'''),
   "run": "vpython",
   "predict": "The function is called four times. How many objects end up in <code>parts</code>, counting the body? How many in <code>rolling</code>? And is the first spoke inside its wheel, or beside it?",
   "reveal": "Nine in <code>parts</code>: the body, plus a wheel and a spoke from each of the four calls. Four in <code>rolling</code>: only the spokes.</p><p>The first spoke is inside its wheel, at <code>&lt;1, 0.4, 0.85&gt;</code>. Its z is the wheel's z plus 0.15, which is halfway along the wheel's axis of 0.3, so the spoke's middle is the wheel's middle. Its size is 0.32 deep, a little more than the wheel is thick, so the white shows at both faces. The wheels on the left have z = -1, and their faces run from -1 to -0.7, against the left side of the body."},

  {"title": "A road made by a loop",
   "teach": "The road is one long, thin grey box with its top at y = 0, so the wheels from chunk 1 sit on it. The dashes down the middle are ten small yellow boxes, placed by a loop. Each one is 4 further along than the one before, starting at x = -18. A dash is 0.02 tall and sits at y = 0.01, so it lies on the road instead of inside it.</p><p>A counter in the loop checks that the loop ran the number of times you meant.",
   "code": code('''
from vpython import *

grass = box(pos=vec(0, -0.2, 0), size=vec(60, 0.2, 30), color=color.green)
road = box(pos=vec(0, -0.05, 0), size=vec(40, 0.1, 4), color=color.gray(0.4))
dashes = 0

for i in range(10):
    dash = box(pos=vec(-18 + i * 4, 0.01, 0), size=vec(1.5, 0.02, 0.2), color=color.yellow)
    dashes = dashes + 1

print(dashes, "dashes, the last one at x =", dash.pos.x)
print("the road runs from x =", road.pos.x - road.size.x / 2, "to x =", road.pos.x + road.size.x / 2)
'''),
   "run": "vpython",
   "predict": "The first dash is at x = -18 and each is 4 further on. Where is the tenth dash? Is it still on the road, which is 40 long with its middle at 0?",
   "reveal": "The tenth dash is at x = 18: the loop's <code>i</code> runs from 0 to 9, and -18 plus 9 times 4 is 18. The road runs from x = -20 to x = 20, so the last dash is 2 short of the end, with the same gap at the other end.</p><p>After the loop, <code>dash</code> holds the last box it made, which is why the print line can ask it for its pos. The other nine dashes are in the world but no name points at them, and that is fine, because nothing in this program moves a dash."},

  {"title": "One speed moves every part",
   "teach": "<code>dt</code> is the slice of a second that one pass of the loop takes: 1/30, because <code>rate(30)</code> runs 30 passes a second. Multiply a speed by <code>dt</code> and you get how far to move on one pass. <code>speed</code> is 3, in units per second, and <code>step</code> is how far one pass moves it: 3 times 1/30, which is 0.1.</p><p>The loop over <code>parts</code> adds the same <code>vec(step, 0, 0)</code> to every part, so the wheels stay where they are on the body. <code>parts[1]</code> is the first wheel, 1 ahead of the body, and the print lines check that it stays 1 ahead.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(60, 0.2, 20), color=color.green)
body = box(pos=vec(0, 0.9, 0), size=vec(3, 0.8, 1.4), color=color.red)
parts = [body]

def add_wheel(x, z):
    wheel = cylinder(pos=vec(x, 0.4, z), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
    parts.append(wheel)

add_wheel(1, 0.7)
add_wheel(-1, 0.7)
add_wheel(1, -1)
add_wheel(-1, -1)

speed = 3
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    step = speed * dt
    for part in parts:
        part.pos = part.pos + vec(step, 0, 0)

    if passes == 30:
        print("after 1 second the body is at x =", round(body.pos.x, 2), " front wheel at x =", round(parts[1].pos.x, 2))
    if passes == 60:
        print("after 2 seconds the body is at x =", round(body.pos.x, 2), " front wheel at x =", round(parts[1].pos.x, 2))
'''),
   "run": "vpython",
   "frames": 60,
   "predict": "The speed is 3 units per second. Where is the body after one second, and after two? Is the front wheel still exactly 1 ahead of the body on both lines?",
   "reveal": "After one second the body is at x = 3.0 and after two it is at x = 6.0: thirty passes of 0.1 each, then thirty more. The front wheel is at 4.0 and then 7.0, still 1 ahead on both lines, because every part got the same step on every pass.</p><p>Change <code>speed</code> to 6 and the body is at 6.0 after one second with nothing else touched. That is why the speed is a number of units per second and not a number per pass: you can read it, and <code>rate</code> can change without the car changing speed."},

  {"title": "The wheels roll: one circumference is one full turn",
   "teach": "A wheel that slides along without turning looks wrong at once. It should turn by exactly as much as it travels. A wheel that rolls one full turn, 360 degrees, has travelled once around its own rim: its <b>circumference</b>, which is <code>2 * pi * radius</code>. So the degrees for one pass are 360 times the step, divided by the circumference.</p><p>The car rolls to the right, and a wheel rolling to the right turns clockwise, which is a negative angle around z. A positive angle turns anticlockwise as you look at the screen, and a minus sign turns the other way. The spokes are in <code>rolling</code>, and each one rotates around a line along z through its own pos, which is the middle of its wheel. A <code>turned</code> counter adds up the degrees.</p><p>The wheel's radius is 0.4, so its circumference is 2.51. The car moves 0.1 per pass.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(60, 0.2, 20), color=color.green)
body = box(pos=vec(0, 0.9, 0), size=vec(3, 0.8, 1.4), color=color.red)
parts = [body]
rolling = []

def add_wheel(x, z):
    wheel = cylinder(pos=vec(x, 0.4, z), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
    spoke = box(pos=vec(x, 0.4, z + 0.15), size=vec(0.7, 0.08, 0.32), color=color.white)
    parts.append(wheel)
    parts.append(spoke)
    rolling.append(spoke)

add_wheel(1, 0.7)
add_wheel(-1, 0.7)
add_wheel(1, -1)
add_wheel(-1, -1)

radius = 0.4
speed = 3
dt = 1 / 30
moved = 0
turned = 0
passes = 0
print("circumference of a wheel:", round(2 * pi * radius, 2))

while True:
    rate(30)
    passes = passes + 1
    step = speed * dt
    for part in parts:
        part.pos = part.pos + vec(step, 0, 0)
    moved = moved + step

    turn = 360 * step / (2 * pi * radius)
    for spoke in rolling:
        spoke.rotate(angle=radians(-turn), axis=vec(0, 0, 1))
    turned = turned + turn

    if passes == 25:
        print("pass 25: moved", round(moved, 2), " turned", round(turned, 1), "degrees")
    if passes == 26:
        print("pass 26: moved", round(moved, 2), " turned", round(turned, 1), "degrees")
    if passes == 30:
        print("pass 30: moved", round(moved, 2), " turned", round(turned, 1), "degrees, which is",
              round(turned / 360, 2), "full turns")
'''),
   "run": "vpython",
   "frames": 30,
   "predict": "The circumference is 2.51 and the car moves 0.1 per pass. On which pass does <code>turned</code> go past 360? After one second the car has moved 3: is that more or less than one full turn of the wheel?",
   "reveal": "On pass 26. After 25 passes the car has moved 2.5, just short of one circumference, and <code>turned</code> is 358.1. One more pass takes it to 2.6 and 372.4 degrees. The spoke has gone once round and a little more.</p><p>More than one full turn: 3 is bigger than 2.51, and the output box shows 429.7 degrees, which is 1.19 turns. A bigger wheel would turn less for the same trip: with radius 0.8 the circumference doubles and the same 3 units is only 0.6 of a turn. The turn line works that out from <code>radius</code>, so changing the wheel changes the turn with it."},

  {"title": "Off the end of the road, and back to the start",
   "teach": "The road is 40 long, so the car reaches its end. A gate on the body's x sends the car back to the other end once the body is past x = 21, which is when the back wheel has left the road. The gate must not put the body back on its own, because the wheels would then be 42 units behind it. Every part gets the same move, as always: subtract <code>vec(42, 0, 0)</code> from all five, and the car is off the left end of the road in one piece, ready to drive on again.</p><p>The speed is 4 here so that the trip takes less time. Nothing else about the moving changes.</p><p>Four camera lines go above the loop. <code>scene.autoscale = False</code> stops the camera zooming out on its own, <code>scene.range = 8</code> shows 8 units from the middle of the view to its edge, and <code>scene.forward = vec(0, -0.5, -1)</code> points the camera away from you and a little down, so the road is seen from above. <code>scene.camera.follow(body)</code> keeps the car in view the whole way, and the road slides past under it.",
   "code": code('''
from vpython import *

grass = box(pos=vec(0, -0.2, 0), size=vec(60, 0.2, 30), color=color.green)
road = box(pos=vec(0, -0.05, 0), size=vec(40, 0.1, 4), color=color.gray(0.4))
body = box(pos=vec(0, 0.9, 0), size=vec(3, 0.8, 1.4), color=color.red)
parts = [body]

def add_wheel(x, z):
    wheel = cylinder(pos=vec(x, 0.4, z), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
    parts.append(wheel)

add_wheel(1, 0.7)
add_wheel(-1, 0.7)
add_wheel(1, -1)
add_wheel(-1, -1)

scene.autoscale = False
scene.range = 8
scene.forward = vec(0, -0.5, -1)
scene.camera.follow(body)

speed = 4
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    step = speed * dt
    for part in parts:
        part.pos = part.pos + vec(step, 0, 0)

    if passes == 157:
        print("pass 157: body at x =", round(body.pos.x, 2))
    if body.pos.x > 21:
        for part in parts:
            part.pos = part.pos - vec(42, 0, 0)
        print("back to the other end on pass", passes, " body at x =", round(body.pos.x, 2),
              " front wheel at x =", round(parts[1].pos.x, 2))
'''),
   "run": "vpython",
   "frames": 160,
   "predict": "The body starts at x = 0 and speed 4 moves it 0.13 per pass, a little more. About how many passes until the body is past 21? Right after the gate fires, is the front wheel still 1 ahead of the body?",
   "reveal": "About 158 passes: 21 divided by 0.13 is a little under 158. After 157 passes the body is at 20.93, not yet past 21, so the gate waits. On pass 158 it is at 21.07, the gate fires, and 42 is taken off, which puts the body at x = -20.93 and the front wheel at -19.93, still 1 ahead.</p><p>In the tab the car vanishes past the right end of the road and comes on at the left end, with the camera jumping to it. If the gate had done <code>body.pos = vec(0, 0.9, 0)</code> instead, the body would jump and the wheels would carry on without it, so the loop over the parts is the whole point of the gate."},
 ],
 "hinge": {"q": "Two students each write the wheel line as <code>spoke.rotate(angle=radians(5), axis=vec(0, 0, 1))</code>, 5 degrees on every pass. One car has <code>speed = 6</code>. The other has <code>speed = 1</code>. Describe what each car's wheels look like, and say what the one fix is for both.",
           "a": "The fast car's wheels turn far too slowly for how far it travels: they look like they are skidding along the road. The slow car's wheels turn far too fast for its crawl: they look like they are spinning on ice. A fixed 5 degrees cannot be right for both, because the right turn depends on the step.</p><p>The fix is the chunk 5 line: <code>turn = 360 * step / (2 * pi * radius)</code>, then <code>radians(-turn)</code>. At speed 6 that is 28.6 degrees per pass, and at speed 1 it is 4.8. Whatever the speed, the wheel turns by exactly as far as the car moves."},
 "brief": {
   "title": "Build: the road trip",
   "minutes": 15,
   "intro": "A red car with four black wheels and white spokes drives along a grey road with yellow dashes, through green grass with lamp posts beside it. The up arrow speeds it up and the down arrow slows it, right down past zero into reverse, and the spokes roll the right way in both directions. The camera follows the car, and when it runs off either end of the road it comes back on at the other end.",
   "steps": [
     "Start from the card below: the car, the two lists, the speed on the arrow keys, and the rolling spokes.",
     "Add the road and the ten dashes from chunk 3, and the grass under them, above the loop.",
     "Add the loop-back gate from chunk 6, and then a second gate the other way: when <code>body.pos.x</code> is less than -21, add <code>vec(42, 0, 0)</code> to every part. The car can now reverse off the left end too.",
     "Add the camera lines from chunk 6 above the loop, so the road slides past under the car.",
     "Lamp posts: a function like <code>add_wheel</code> from chunk 2, a thin grey cylinder 2 tall with a yellow sphere on top, called by a loop every 8 units along x at z = 3 and again at z = -3.",
     "Write a caption that says what the two keys do.",
   ],
   "cards": [
     {"title": "Speed on the keys, and wheels that roll backwards",
      "teach": "The speed starts at 0 and the keys change it a little on every pass they are held, so holding up is a smooth start and not a jump. Two gates keep it between -3 and 6. A negative speed makes a negative step, and a negative step makes a negative <code>turn</code>, so <code>radians(-turn)</code> comes out positive and the spokes turn the other way. Nothing in the rolling lines knows which way the car is going. The sign does the work.",
      "code": code('''
from vpython import *

scene.caption = "Click the scene. Up speeds the car up, down slows it and then reverses it."
ground = box(pos=vec(0, -0.1, 0), size=vec(60, 0.2, 20), color=color.green)
body = box(pos=vec(0, 0.9, 0), size=vec(3, 0.8, 1.4), color=color.red)
parts = [body]
rolling = []

def add_wheel(x, z):
    wheel = cylinder(pos=vec(x, 0.4, z), axis=vec(0, 0, 0.3), radius=0.4, color=color.black)
    spoke = box(pos=vec(x, 0.4, z + 0.15), size=vec(0.7, 0.08, 0.32), color=color.white)
    parts.append(wheel)
    parts.append(spoke)
    rolling.append(spoke)

add_wheel(1, 0.7)
add_wheel(-1, 0.7)
add_wheel(1, -1)
add_wheel(-1, -1)

radius = 0.4
speed = 0
dt = 1 / 30

while True:
    rate(30)
    keys = keysdown()
    if "up" in keys:
        speed = speed + 0.2
    if "down" in keys:
        speed = speed - 0.2
    if speed > 6:
        speed = 6
    if speed < -3:
        speed = -3

    step = speed * dt
    for part in parts:
        part.pos = part.pos + vec(step, 0, 0)

    turn = 360 * step / (2 * pi * radius)
    for spoke in rolling:
        spoke.rotate(angle=radians(-turn), axis=vec(0, 0, 1))

    if len(keys) > 0:
        print(keys, " speed", round(speed, 1), " turn this pass", round(turn, 2), "degrees")
'''),
      "run": "vpython",
      "frames": 10,
      "inject": [[2, "HOLD", "up"], [3, "HOLD", "up"], [4, "HOLD", "up"], [6, "HOLD", "down"], [7, "HOLD", "down"], [8, "HOLD", "down"], [9, "HOLD", "down"], [10, "HOLD", "down"]],
      "predict": "Up is held for three passes, then down for five. What is the speed after the three ups, and after the five downs? Does the sign of <code>turn</code> change, and what does that look like on the spokes?",
      "reveal": "After three ups the speed is 0.6: three steps of 0.2. Five downs take off 1.0, so it ends at -0.4 and the car is reversing. On the passes with no key held, the speed stays where it is and the car keeps going at that speed, because nothing in the loop slows it down.</p><p>The sign changes with the speed. While the car goes right the turn is positive, 2.86 degrees on the first pass of speed 0.6, and the spokes turn clockwise. At speed -0.4 the turn is -1.91, <code>radians(-turn)</code> is a positive angle, and the spokes turn the other way. Reverse rolls the wheels backwards without a single extra line."},
   ],
   "expected_got": [
     ["Every wheel touches the road and none sinks into it", ""],
     ["The spokes turn when the car moves and stop when it stops", ""],
     ["Holding down past zero reverses the car and the spokes turn the other way", ""],
     ["Running off either end of the road brings the whole car back on at the other end", ""],
     ["The car never leaves the view", ""],
   ],
 },
 "exits": {
   "floor": "The car with four wheels standing on the road, every wheel touching and none sunk, and the car driving right at one steady speed with the spokes rolling.",
   "middle": "The road trip: speed on the keys, reverse, the loop-back at both ends, the camera following, and the dashes.",
   "stretch": "Lamp posts both sides, then brake lights: two small red boxes on the back of the car, in <code>parts</code>, whose <code>emissive</code> is True only while the down arrow is held. Then a second car in its own two lists, driving the other way at its own speed.",
 },
 "ledger": "Stamp 5: a wheel is <code>cylinder(axis=vec(0, 0, w), radius=r)</code> lifted by its radius, two lists for one model (<code>parts</code> moves, <code>rolling</code> turns), a road placed by a loop with a counter, <code>step = speed * dt</code> moves every part, one circumference <code>2 * pi * radius</code> is one full turn, <code>turn = 360 * step / (2 * pi * radius)</code> then <code>radians(-turn)</code>, a negative step rolls backwards on its own, a loop-back gate shifts every part by the same vector.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 and 2, the wheel and the two lists, 15 min",
     "0:25 chunk 3, the road, 8 min",
     "0:33 chunk 4, one speed for every part, 10 min",
     "0:43 chunk 5, rolling, 15 min (the circumference line is the teaching point; do it on the projector with a real wheel or a lid)",
     "0:58 chunk 6, the loop-back and the camera, 7 min",
     "1:05 hinge question, 5 min",
     "1:10 build brief, 15 min (most rooms get speed on the keys and stop; the loop-back both ways is the middle exit)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Lifts the wheel by 0.5 like a box and it floats, or by nothing and it is half under the road.", "A wheel is lifted by its radius. Have them print <code>wheel.pos.y - wheel.radius</code>, as chunk 1 does, and read off where the bottom is."],
     ["Puts the spokes in <code>rolling</code> but not in <code>parts</code>, and they stay behind when the car drives off.", "Everything that moves goes in <code>parts</code>. The spokes are in both lists, and chunk 2's print shows nine in one and four in the other."],
     ["Writes a fixed <code>radians(5)</code> for the wheel turn.", "That is the hinge. The turn has to come from the step, or the wheels skid at one speed and spin at another."],
     ["Puts the body back at 0 in the loop-back gate and the wheels carry on without it.", "The gate moves every part by the same vector, the way every other move in the course does. Ask what happens to a wheel that was 1 ahead when only the body jumps."],
     ["Rotates the wheel cylinders as well as the spokes and sees no difference.", "A plain cylinder turning around its own axis looks the same. Only the spoke shows the turn, which is why the cylinders are not in <code>rolling</code>. Turning them too does no harm but does nothing either."],
     ["Spokes turn the wrong way: forward looks like reverse.", "The minus is missing from <code>radians(-turn)</code>. Rolling right is clockwise around z, which is a negative angle, as the right turn was in session 4."],
   ],
   "standards": ["NY-7.G.4", "NY-6.NS.5", "MP8"],
   "routing": "Chunk 3 can be cut to a single grey box for the road with no dashes; the dashes come back in the build. Chunk 6 can be cut to the camera lines shown on the projector, and the loop-back becomes a build step. Chunk 5 is not cuttable, and neither is the hinge; a room that skips the circumference line ships skidding wheels.",
   "setup": "The output boxes on this page come from running each snippet against the installed library with no browser open and the keys fed in by the build script. The picture is not checked, so run chunk 5 once on the projector machine before class and watch that the spokes turn clockwise while the car moves right.",
 },
},

# =====================================================================
{
 "num": 6,
 "slug": "session06_a_solar_system_objects_carry_their_numbers",
 "title": "A solar system: objects that carry their own numbers",
 "subtitle": "A function that returns a planet, a speed that lives on the planet itself, a list of planets turned by one loop, a moon with two motions, and a slider that runs time",
 "new": ["a function that returns an object", "an attribute you give an object", "planet.speed and planet.turned", "a moon with two rotates", "a slider that sets a number on an object", "label", "scene.camera.follow from a key"],
 "reuse": "Session 2: a function that makes objects, a list of parts. Session 4: rotate with origin, the degrees counter",
 "env_note": True,
 "reuse_note": "Chunk 2 is the idea the rest of the course leans on: <code>earth.speed = 2</code> makes a new attribute, and any function that can see the earth can read or change it. This is how the course shares a number between a bound function and the loop without a global. Spend the time on it.",
 "opener": {
   "title": "Retrieval: rotate, origin, and lists",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "What is the difference between <code>moon.rotate(angle=radians(10), axis=vec(0, 1, 0))</code> and the same line with <code>origin=planet.pos</code> added?",
      "a": "Without origin, the moon turns around its own middle, which for a sphere changes nothing you can see. With origin, it moves in a circle around the planet, staying the same distance from it."},
     {"q": "A loop adds 3 to a counter on every pass and a gate checks for 360. What does the gate detect, and why does the body of the gate set the counter back to 0?",
      "a": "It detects one full turn. Setting the counter back to 0 starts counting the next turn, so the gate opens again 120 passes later. Without the reset the counter passes 360 and never equals it again."},
     {"q": "Three parts are in a list and a loop adds <code>vec(0, 0, -3)</code> to each one's pos. What happens to the distances between the parts?",
      "a": "Nothing. Every part moves by the same vector, so the model moves in one piece."},
   ],
 },
 "chunks": [
  {"title": "A function that returns the planet it made",
   "teach": "Session 2's functions made objects and kept no name for them. This one returns the sphere it makes, so the caller can keep it: <code>earth = make_planet(5, 0.4, color.blue)</code>. After that line, <code>earth</code> is the sphere and can be moved, recoloured, or rotated like any other.</p><p>Without the return line, <code>earth</code> would be <code>None</code>, and <code>earth.pos</code> would stop the program with an error.",
   "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)

def make_planet(distance, size, colour):
    p = sphere(pos=vec(distance, 0, 0), radius=size, color=colour)
    return p

earth = make_planet(5, 0.4, color.blue)
mars = make_planet(7, 0.3, color.red)
print("earth is at", earth.pos, "with radius", earth.radius)
print("mars is at", mars.pos, "with radius", mars.radius)
'''),
   "run": "vpython",
   "predict": "What does <code>earth</code> hold after its line runs? And if the <code>return p</code> line were deleted, what would <code>earth</code> hold, and what would happen on the first print line?",
   "reveal": "<code>earth</code> holds the sphere that the function made, 5 from the sun with radius 0.4, and the print line reads its pos and radius.</p><p>Without the return line the function still makes the sphere, and it still appears in the tab, but the function gives nothing back, so <code>earth</code> holds <code>None</code>. The print line then asks None for its pos and the program stops with <code>AttributeError: 'NoneType' object has no attribute 'pos'</code>, the same error as a click on empty space in session 1."},

  {"title": "An object can carry a number you give it",
   "teach": "<code>pos</code>, <code>radius</code> and <code>color</code> are attributes VPython gave the sphere. You can give it more. <code>earth.speed = 2</code> makes an attribute called <code>speed</code> on the earth and puts 2 in it. From then on <code>earth.speed</code> reads it, and any line that can see <code>earth</code> can change it.</p><p>The number belongs to the object. Mars has its own <code>speed</code>, which can be different, and a loop over planets can ask each one for its own.</p><p>Reading an attribute you have not given yet is an error, and the last line shows which one.",
   "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)
earth = sphere(pos=vec(5, 0, 0), radius=0.4, color=color.blue)
earth.speed = 3
earth.name = "Earth"
mars = sphere(pos=vec(7, 0, 0), radius=0.3, color=color.red)
mars.speed = 2
mars.name = "Mars"

print(earth.name, "turns", earth.speed, "degrees per pass")
print(mars.name, "turns", mars.speed, "degrees per pass")
print("the earth's radius is", earth.radius, "and its speed is", earth.speed)
print("mars has a year counter:", mars.year)
'''),
   "run": "vpython",
   "expect_error": True,
   "predict": "Which of the earth's attributes in this program came from VPython, and which did the program give it? The last line reads <code>mars.year</code>, which nothing has set. What happens?",
   "reveal": "<code>radius</code>, <code>pos</code> and <code>color</code> came from VPython. <code>speed</code> and <code>name</code> were given by the program, with an assignment each.</p><p>The last line stops the program: <code>AttributeError: 'sphere' object has no attribute 'year'</code>. An attribute exists from the moment something is assigned to it, and not before. The three lines above it printed first, so the output box shows them and then the error."},

  {"title": "One loop turns every planet by its own speed",
   "teach": "The function now takes a name and a speed and puts both on the planet, plus a <code>turned</code> counter starting at 0. The planets go in a list. One loop rotates each planet around the sun by its own speed and adds that speed to its own counter, and a gate on 360 says when each planet finishes a year.",
   "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)

def make_planet(name, distance, size, colour, speed):
    p = sphere(pos=vec(distance, 0, 0), radius=size, color=colour)
    p.name = name
    p.speed = speed
    p.turned = 0
    return p

planets = []
planets.append(make_planet("Mercury", 3, 0.2, color.gray(0.6), 6))
planets.append(make_planet("Earth", 5, 0.4, color.blue, 3))
planets.append(make_planet("Mars", 7, 0.3, color.red, 2))
passes = 0

while True:
    rate(30)
    passes = passes + 1

    for p in planets:
        p.rotate(angle=radians(p.speed), axis=vec(0, 1, 0), origin=sun.pos)
        p.turned = p.turned + p.speed
        if p.turned == 360:
            print(p.name, "finished a year on pass", passes)
            p.turned = 0
'''),
   "run": "vpython",
   "frames": 180,
   "predict": "Mercury turns 6 degrees per pass, Earth 3, and Mars 2. Which planet finishes a year first, and on which pass? How many Mercury years fit in one Mars year?",
   "reveal": "Mercury first, on pass 60: 360 divided by 6. Earth finishes on pass 120 and Mars on pass 180.</p><p>Three Mercury years fit in one Mars year: Mercury finishes on passes 60, 120 and 180, and Mars finishes once, on 180. The output box shows that order. Each planet keeps its own count in its own <code>turned</code>, which is why one loop can serve all three."},

  {"title": "A moon has two motions",
   "teach": "A moon goes around the earth, and the earth goes around the sun, so the moon has to do both. Two rotate lines: one around the sun by the earth's speed, so the moon keeps up with the earth, and one around the earth by its own speed.",
   "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)
earth = sphere(pos=vec(5, 0, 0), radius=0.4, color=color.blue)
moon = sphere(pos=vec(5.8, 0, 0), radius=0.1, color=color.white)
passes = 0

while True:
    rate(30)
    passes = passes + 1

    earth.rotate(angle=radians(3), axis=vec(0, 1, 0), origin=sun.pos)
    moon.rotate(angle=radians(3), axis=vec(0, 1, 0), origin=sun.pos)
    moon.rotate(angle=radians(12), axis=vec(0, 1, 0), origin=earth.pos)

    if passes in [10, 60, 120]:
        print("pass", passes, "  moon to earth", round(mag(moon.pos - earth.pos), 2),
              "  earth to sun", round(mag(earth.pos - sun.pos), 2))
'''),
   "run": "vpython",
   "frames": 120,
   "predict": "The moon starts 0.8 from the earth. After 120 passes, is it still 0.8 from the earth? What would happen to that distance if the first <code>moon.rotate</code> line, the one around the sun, were deleted?",
   "reveal": "Still 0.8, on every line, and the earth is still 5.0 from the sun. The first moon line moves the moon along with the earth, and the second swings it around the earth, so the moon stays with the earth and circles it.</p><p>Without the first moon line, the moon would only turn around wherever the earth is on that pass, by 12 degrees, while the earth moves on without it. The distance would drift, growing and shrinking, and the moon would wander off its circle. Delete the line and watch; then put it back."},

  {"title": "A slider sets a number on the sun, and the loop reads it",
   "teach": "The slider's function and the loop need to share one number: how fast time runs. Put it on the sun: <code>sun.factor</code>. The slider's function assigns it, and the loop multiplies every speed by it. Anything that can see the sun can see the number.</p><p>At 0 everything stops, but the loop keeps running, so moving the slider again starts things up.",
   "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)
sun.factor = 1

def set_time(s):
    sun.factor = s.value
    print("time now runs", sun.factor, "times as fast")

scene.append_to_caption("Time: ")
slider(min=0, max=4, value=1, step=0.5, bind=set_time)

mercury = sphere(pos=vec(3, 0, 0), radius=0.2, color=color.gray(0.6))
mercury.turned = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1

    mercury.rotate(angle=radians(6 * sun.factor), axis=vec(0, 1, 0), origin=sun.pos)
    mercury.turned = mercury.turned + 6 * sun.factor

    if mercury.turned >= 360:
        print("Mercury finished a year on pass", passes)
        mercury.turned = mercury.turned - 360
'''),
   "run": "vpython",
   "frames": 120,
   "inject": [[30, "WIDGET", "set_time", 2], [80, "WIDGET", "set_time", 0]],
   "predict": "The slider is moved to 2 on pass 30, and to 0 on pass 80. Without the slider, Mercury's first year would end on pass 60. When does it end now? And what does Mercury do after pass 80?",
   "reveal": "The first year ends on pass 45. By pass 30 Mercury has turned 180 degrees at 6 per pass. From then on it turns 12 per pass, so the remaining 180 take 15 passes. The second year ends on pass 75, 30 passes later.</p><p>After pass 80 Mercury stops: 6 times 0 is 0, so the rotate turns it by nothing and the counter stops growing. The loop is still running, and the output box shows no more years, because the slider was never moved again."},

  {"title": "A label that follows, and a key that picks what the camera follows",
   "teach": "A <b>label</b> is flat text that floats in the scene at a pos. Give the earth its label as an attribute, <code>earth.tag</code>, and move the label to the earth's pos on every pass, because rotate moves the earth and nothing else moves the label.</p><p>A keydown function can choose what the camera follows: e for the earth, s for the sun.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene, then press e to follow the Earth or s for the Sun."
sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)
earth = sphere(pos=vec(5, 0, 0), radius=0.4, color=color.blue)
earth.tag = label(pos=earth.pos, text="Earth", height=14, box=False, yoffset=20)

def pick_view(evt):
    if evt.key == "e":
        scene.camera.follow(earth)
        print("the camera follows the Earth")
    if evt.key == "s":
        scene.camera.follow(sun)
        print("the camera follows the Sun")

scene.bind("keydown", pick_view)
passes = 0

while True:
    rate(30)
    passes = passes + 1
    earth.rotate(angle=radians(3), axis=vec(0, 1, 0), origin=sun.pos)
    earth.tag.pos = earth.pos

    if passes in [20, 40]:
        print("pass", passes, "  label at x =", round(earth.tag.pos.x, 2), " z =", round(earth.tag.pos.z, 2),
              "  earth at x =", round(earth.pos.x, 2), " z =", round(earth.pos.z, 2))
'''),
   "run": "vpython",
   "frames": 40,
   "inject": [[10, "KEYDOWN", "e"], [30, "KEYDOWN", "s"]],
   "predict": "The label is a separate object from the earth. Why does the loop need the line <code>earth.tag.pos = earth.pos</code>? What would you see without it?",
   "reveal": "Because <code>rotate</code> moves the earth and nothing moves the label. The line copies the earth's new pos to the label on every pass, so the output box shows the label and the earth at the same x and z on passes 20 and 40.</p><p>Without it the label would stay where the earth started, at x = 5, and the word Earth would float over empty space while the planet went round without it. The e and s keys only change what the camera follows; they do not move anything."},
 ],
 "hinge": {"q": "From session 1: a student makes the sun with <code>radius=2</code> and Mercury with <code>distance=1</code>. What do they see in the tab, and which one number do they change?",
           "a": "Nothing, or a grey bump on the sun. Mercury's pos is 1 from the sun's middle and the sun's radius is 2, so Mercury is inside the sun. pos is the middle of a sphere, and a sphere reaches one radius out from it in every direction.</p><p>Change Mercury's distance to something bigger than the sun's radius plus Mercury's own radius, 3 or more, so the two spheres do not overlap."},
 "brief": {
   "title": "Build: the solar system",
   "minutes": 20,
   "intro": "A sun in the middle and at least four planets going around it, each with its own name, distance, size, colour and speed, made by one function and turned by one loop. One planet has a moon. Every planet wears its name on a label that follows it. A slider under the scene runs time faster or slower, and the number keys choose which planet the camera follows. A line of text under the scene counts the Earth's years.",
   "steps": [
     "Start from the card below: <code>make_planet</code> with the label as an attribute, and the loop that turns every planet and moves every label.",
     "Make four planets with different distances and speeds. Keep the distances at least 1 apart so no two overlap.",
     "Add the moon from chunk 4 to the second planet, with both rotate lines inside the loop.",
     "Add the time slider from chunk 5, with <code>sun.factor</code> multiplied into every rotate angle and every counter.",
     "Add a keydown function: the keys 1 to 4 call <code>scene.camera.follow</code> on <code>planets[0]</code> to <code>planets[3]</code>, and 0 follows the sun.",
     "Add a line of text under the scene that counts the Earth's years: <code>years_text = wtext(text=\"Earth years: 0\")</code> puts it there, and assigning to <code>years_text.text</code> changes it. Give the Earth a <code>years</code> attribute, add 1 to it when its counter reaches 360, and then set <code>years_text.text = \"Earth years: \" + str(earth.years)</code>. <code>str</code> changes a number into a string so that <code>+</code> can join it to words.",
   ],
   "cards": [
     {"title": "A planet that carries its own label",
      "teach": "The function makes the planet, puts the name, speed and counter on it, and makes a label that it also puts on the planet, as <code>p.tag</code>. The loop then has everything it needs from the planet itself.",
      "code": code('''
from vpython import *

sun = sphere(pos=vec(0, 0, 0), radius=1.2, color=color.yellow)

def make_planet(name, distance, size, colour, speed):
    p = sphere(pos=vec(distance, 0, 0), radius=size, color=colour)
    p.name = name
    p.speed = speed
    p.turned = 0
    p.tag = label(pos=p.pos, text=name, height=12, box=False, yoffset=16)
    return p

planets = []
planets.append(make_planet("Mercury", 3, 0.2, color.gray(0.6), 6))
planets.append(make_planet("Venus", 4, 0.35, color.orange, 4))
passes = 0

while True:
    rate(30)
    passes = passes + 1

    for p in planets:
        p.rotate(angle=radians(p.speed), axis=vec(0, 1, 0), origin=sun.pos)
        p.tag.pos = p.pos
        p.turned = p.turned + p.speed
        if p.turned == 360:
            print(p.name, "finished a year on pass", passes, "  its label is at x =", round(p.tag.pos.x, 2))
            p.turned = 0
'''),
      "run": "vpython",
      "frames": 90,
      "predict": "Venus turns 4 degrees per pass. On which pass does it finish a year? Where is its label on that pass?",
      "reveal": "Pass 90: 360 divided by 4. On that pass Venus is back where it started, at x = 4, and its label is at x = 4.0 as well, because the loop moved the label to the planet on every pass.</p><p>Mercury finishes on pass 60, with its label at x = 3.0, back at its start too."},
   ],
   "expected_got": [
     ["Each planet finishes its year on the pass you worked out from its speed", ""],
     ["The moon stays with its planet all the way round", ""],
     ["Sliding time to 0 freezes everything, and sliding it back starts everything again", ""],
     ["Every label stays on its planet", ""],
     ["The year count under the scene goes up by 1 each time the Earth comes round", ""],
   ],
 },
 "exits": {
   "floor": "A sun and two planets from <code>make_planet</code>, each with its own speed, turned by one loop, printing when each finishes a year.",
   "middle": "The solar system: four planets with labels, a moon, the time slider, and the number keys choosing what the camera follows.",
   "stretch": "Give each planet a <code>make_trail=True</code> in the sphere call so it draws its orbit. Then a second moon on another planet, and a key that reverses time by setting <code>sun.factor</code> to its negative.",
 },
 "ledger": "Stamp 6: <code>return p</code> gives the object back, <code>earth.speed = 3</code> makes an attribute the object carries, a loop over a list reads each object's own attributes, a moon rotates around the sun and around its planet, a shared number lives on an object (<code>sun.factor</code>), <code>label(pos, text)</code> and moving it every pass, <code>scene.camera.follow</code> from a key, <code>str(n)</code> to join a number to words.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunk 1, return, 8 min",
     "0:18 chunk 2, attributes you give, 15 min (the core of the session)",
     "0:33 chunk 3, the list and the years, 12 min",
     "0:45 chunk 4, the moon, 10 min",
     "0:55 chunks 5 and 6, the slider and labels, 15 min",
     "1:10 hinge question, 5 min",
     "1:15 build brief, 10 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Forgets <code>return p</code> and gets <code>AttributeError: 'NoneType' object has no attribute 'pos'</code>.", "The function made the planet and gave nothing back. Ask what the line <code>earth = make_planet(...)</code> stored. Chunk 1's reveal has the error."],
     ["Reads <code>p.turned</code> before the function sets it.", "An attribute exists after the first assignment. Chunk 2's last line is this error on purpose; point at it."],
     ["Rotates the moon around the sun by the moon's own speed instead of the earth's.", "The moon has to keep up with the earth, so the first rotate uses the earth's speed. Print the moon-to-earth distance; it drifts when the speeds differ."],
     ["Keeps the slider's number in a plain variable and the loop never sees it change.", "The slider's function cannot change a plain variable outside itself. Put the number on the sun, where both can reach it. That is what chunk 5 is for."],
     ["Checks <code>p.turned == 360</code> with a speed that does not divide 360, like 7, and no year is ever printed.", "The counter steps over 360 without landing on it. Use <code>&gt;=</code> and subtract 360, the way chunk 5 does."],
   ],
   "standards": ["NY-5.G.2", "NY-6.EE.2", "MP7"],
   "routing": "Chunk 6 can be cut; the card covers labels. Chunk 4 can become the stretch. Chunk 2 cannot be cut or shortened, because sessions 7, 8 and 9 all use attributes to share state between a bound function and the loop.",
 },
},

# =====================================================================
{
 "num": 7,
 "slug": "session07_a_game_catch_the_falling_balls",
 "title": "A game: catch the falling balls",
 "subtitle": "A paddle on keys, a ball that falls, one gate that decides a catch, a score on screen, lives, game over, and a key that starts again",
 "new": ["abs for a distance", "randint", "a catch gate with and", "str to put a number in text", "wtext for a score", "lives", "a state name", "restart from inside the loop", "harder each catch"],
 "reuse": "Session 3: velocity on the ball, keysdown in the loop. Session 6: attributes on an object",
 "env_note": True,
 "reuse_note": "Every piece of state in this game is a plain variable inside the loop, because there are no bound functions: the restart is a key read with keysdown. Say that at the start. Students who try to add a Reset button will hit the shared-state problem and should use the r key instead, or put the numbers on the paddle as attributes.",
 "opener": {
   "title": "Retrieval: attributes, the floor gate, and two kinds of key",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "<code>ball.vel = vec(0, -4, 0)</code> is written once above the loop. What kind of thing is <code>vel</code> here, and who gave it to the ball?",
      "a": "An attribute that the program gave the ball by assigning to it. VPython did not give the ball a vel. From then on the ball carries its own velocity, and a loop over several balls can read each one's."},
     {"q": "Why does the floor gate compare <code>ball.pos.y</code> with the ball's radius and not with 0?",
      "a": "pos is the middle of the ball. The bottom of the ball is one radius below, so the ball touches the floor when its middle is one radius up."},
     {"q": "One box moves one step per tap. Another glides while the key is held. Which used a bound keydown function and which used <code>keysdown()</code> in the loop?",
      "a": "One step per tap is the bound function: VPython calls it once per press. Gliding is <code>keysdown()</code>: the gate runs on every pass and the key is in the list for as long as it is held."},
   ],
 },
 "chunks": [
  {"title": "A paddle on the keys and a ball that falls",
   "teach": "The paddle is a flat box that slides along x while an arrow key is held. The ball falls at a steady speed: its velocity is <code>vec(0, -4, 0)</code>, 4 per second downward, and there is no gravity line, so the speed never changes. The ball's velocity is an attribute on the ball, <code>ball.vel</code>, the way session 6 put a speed on a planet.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene, then hold left or right."
ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(0, 0.25, 0), size=vec(3, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(0, 8.5, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if "right" in keys:
        paddle.pos.x = paddle.pos.x + 0.3
    if "left" in keys:
        paddle.pos.x = paddle.pos.x - 0.3

    ball.pos = ball.pos + ball.vel * dt

    if passes in [30, 60]:
        print("pass", passes, "  ball height", round(ball.pos.y, 2), "  paddle x", round(paddle.pos.x, 2))
'''),
   "run": "vpython",
   "frames": 60,
   "inject": [[5, "HOLD", "right"], [6, "HOLD", "right"], [7, "HOLD", "right"], [8, "HOLD", "right"], [9, "HOLD", "right"], [10, "HOLD", "right"]],
   "predict": "The ball starts 8.5 up and falls 4 per second. On which pass does its middle reach the paddle's height, 0.5? The right arrow is held for six passes: where is the paddle after that?",
   "reveal": "Pass 60. In two seconds the ball falls 8, so on pass 60 its height is 0.5, and on pass 30 it was 4.5. The output box shows both.</p><p>The paddle is at x = 1.8 after six passes of 0.3 each, and it stays there once the key is let go, because the key gates change the position, not a velocity. Nothing stops the ball at the paddle yet. That is the next chunk."},

  {"title": "The catch gate: close enough, and low enough",
   "teach": "A catch is two things true at once: the ball is down at the paddle's height, and it is near the paddle along x. <code>and</code> joins the two checks into one gate.</p><p><code>abs(ball.pos.x - paddle.pos.x)</code> is the gap between them along x, always as a positive number. abs throws away the minus sign, so a ball 1 to the left and a ball 1 to the right both give a gap of 1. The paddle is 3 wide, so a gap under 1.5 means the ball is over the paddle.</p><p>When the ball is caught, the gate's body sends it back to the top at a random x. <code>randint(-4, 4)</code> picks a whole number from -4 to 4. It comes from Python's <code>random</code> module, so the program imports it.",
   "code": code('''
from vpython import *
from random import randint

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(0, 0.25, 0), size=vec(3, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(1, 8, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
score = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + ball.vel * dt

    gap = abs(ball.pos.x - paddle.pos.x)
    if ball.pos.y < 0.9 and gap < 1.5:
        score = score + 1
        print("caught on pass", passes, "  the gap was", round(gap, 2), "  score", score)
        ball.pos = vec(randint(-4, 4), 8, 0)
        print("a new ball is at the top, height", ball.pos.y)
'''),
   "run": "vpython",
   "frames": 60,
   "predict": "The ball starts at x = 1 and the paddle is at x = 0. Is the gap small enough for a catch? On about which pass does the catch happen, and where does the new ball start?",
   "reveal": "Yes: the gap is 1.0, under 1.5. The catch happens on pass 54, the first pass where the ball's height is under 0.9. 7.1 units at 4 per second is 1.775 seconds, which is a little more than 53 passes.</p><p>The new ball starts at height 8 and at an x chosen by <code>randint</code>. The output box shows the x of one run; on your run it will probably be a different whole number from -4 to 4, because that is what random means."},

  {"title": "Missing the ball costs a life",
   "teach": "If the whole ball is under the ground, lower than -0.5, it was missed. That is a second gate, after the catch gate: lives go down by one and the ball goes back to the top. The paddle in this program is far away at x = -8 so that no catch can happen and every ball is missed.",
   "code": code('''
from vpython import *
from random import randint

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(-8, 0.25, 0), size=vec(3, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(1, 8, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
lives = 3
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + ball.vel * dt

    if ball.pos.y < -0.5:
        lives = lives - 1
        print("missed on pass", passes, "  lives left", lives)
        ball.pos = vec(randint(-4, 4), 8, 0)
'''),
   "run": "vpython",
   "frames": 200,
   "predict": "Every ball is missed. The first miss is on the first pass where the ball's height is below -0.5. On about which pass is that, and on which pass do the lives reach 0?",
   "reveal": "The first miss is on pass 64: the ball falls 8.5 units, from 8 to -0.5, at 4 per second, which takes 2.125 seconds, and pass 64 is the first pass past that. Each new ball starts at 8 again, so the misses come every 64 passes: 64, 128, 192. Lives reach 0 on pass 192.</p><p>The program keeps dropping balls after that, and lives would go to -1. Chunk 5 stops the game instead."},

  {"title": "The score on the screen",
   "teach": "<code>wtext</code> puts a line of text under the scene, and assigning to its <code>text</code> changes it. The text has to be a string. <code>str(score)</code> changes the number 3 into the string <code>\"3\"</code>, and <code>+</code> joins two strings. Without <code>str</code>, joining a string to a number is an error.</p><p>The paddle here is wide enough to catch everything, so the score climbs on every ball.",
   "code": code('''
from vpython import *
from random import randint

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(0, 0.25, 0), size=vec(12, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(1, 8, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
score = 0
score_text = wtext(text="Score: 0")
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + ball.vel * dt

    gap = abs(ball.pos.x - paddle.pos.x)
    if ball.pos.y < 0.9 and gap < 6:
        score = score + 1
        score_text.text = "Score: " + str(score)
        print("pass", passes, "  the text under the scene now says:", score_text.text)
        ball.pos = vec(randint(-4, 4), 8, 0)
'''),
   "run": "vpython",
   "frames": 120,
   "predict": "What does the line under the scene say after the second catch? What would go wrong if the line were <code>\"Score: \" + score</code> with no <code>str</code>?",
   "reveal": "It says <code>Score: 2</code>, and the output box shows the text after each catch, on passes 54 and 108.</p><p>Without <code>str</code>, Python is asked to join a string to a number, and it stops with <code>TypeError: can only concatenate str (not \"int\") to str</code>. <code>str(score)</code> changes the type of the number to a string first, and then the join works."},

  {"title": "A state name: playing, or over",
   "teach": "A game is not always being played. Keep a variable called <code>state</code> that holds <code>\"play\"</code> or <code>\"over\"</code>, and gate the ball's movement on it. When lives reach 0, the state becomes over, the ball stops, and a label says so. Pressing r puts everything back and the state becomes play.</p><p>The restart is a key read with <code>keysdown</code> inside the loop, so every number it resets is a plain variable the loop already owns.",
   "code": code('''
from vpython import *
from random import randint

scene.caption = "Click the scene. When the game is over, press r to play again."
ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(-8, 0.25, 0), size=vec(3, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(1, 8, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
sign = label(pos=vec(0, 4, 0), text="", height=24, box=False)
dt = 1 / 30
lives = 3
state = "play"
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if state == "play":
        ball.pos = ball.pos + ball.vel * dt

    if state == "play" and ball.pos.y < -0.5:
        lives = lives - 1
        ball.pos = vec(randint(-4, 4), 8, 0)
        print("missed on pass", passes, "  lives left", lives)

    if state == "play" and lives == 0:
        state = "over"
        sign.text = "Game over. Press r."
        print("pass", passes, "  state is now", state)

    if state == "over" and "r" in keys:
        state = "play"
        lives = 3
        sign.text = ""
        ball.pos = vec(randint(-4, 4), 8, 0)
        print("pass", passes, "  restarted, state is", state, " lives", lives)
'''),
   "run": "vpython",
   "frames": 210,
   "inject": [[100, "HOLD", "r"], [200, "HOLD", "r"]],
   "predict": "r is pressed on pass 100 and again on pass 200. The game is over on pass 192. Which of the two presses restarts it, and why does the other one do nothing?",
   "reveal": "The press on pass 200 restarts it: the state is over by then, so the gate <code>state == \"over\" and \"r\" in keys</code> is True, and the output box shows the restart with lives back at 3.</p><p>The press on pass 100 does nothing, because the state is still play, and the restart gate needs both halves to be True. Pressing r in the middle of a game should not throw the game away, and that one <code>and</code> is what makes sure it does not."},

  {"title": "Harder with every catch",
   "teach": "Each catch makes the next ball fall faster: subtract 1 from <code>ball.vel.y</code>, which is already negative, so the ball falls 1 unit per second faster. The paddle here is wide enough to catch everything, so you can watch the speed climb.",
   "code": code('''
from vpython import *
from random import randint

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
paddle = box(pos=vec(0, 0.25, 0), size=vec(12, 0.5, 1), color=color.blue)
ball = sphere(pos=vec(1, 8, 0), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
score = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1
    ball.pos = ball.pos + ball.vel * dt

    gap = abs(ball.pos.x - paddle.pos.x)
    if ball.pos.y < 0.9 and gap < 6:
        score = score + 1
        ball.vel.y = ball.vel.y - 1
        ball.pos = vec(randint(-4, 4), 8, 0)
        print("catch", score, "on pass", passes, "  the next ball falls at", -ball.vel.y, "per second")
'''),
   "run": "vpython",
   "frames": 140,
   "predict": "The first ball takes 54 passes to reach the paddle at 4 per second. The second ball falls at 5 per second. Does it take more passes or fewer? About how many?",
   "reveal": "Fewer: 43 passes, so the second catch is on pass 97. The ball has 7.1 units to fall at 5 per second, which is 1.42 seconds. The third ball, at 6 per second, takes 36 passes and is caught on pass 133.</p><p>Every catch takes a bigger bite out of the time the player has. That one line is what makes the game get harder."},
 ],
 "hinge": {"q": "A student's score climbs by about 30 a second after the first catch, and keeps climbing. The catch gate is <code>if ball.pos.y &lt; 0.9 and gap &lt; 1.5:</code> and its body adds 1 to the score. What is missing from the body, and why does the score climb by about 30 a second?",
           "a": "The body never moves the ball back to the top. The ball keeps falling through the paddle, the gate is still True on the next pass, and the next, so the score goes up once per pass, which is 30 times a second.</p><p>The fix is the line <code>ball.pos = vec(randint(-4, 4), 8, 0)</code> inside the body. Once the ball is at the top, the gate is False until the ball comes down again. A gate that should fire once has to change the thing it checks."},
 "brief": {
   "title": "Build: the catch game in 3D",
   "minutes": 15,
   "intro": "The game from the chunks, with one change that makes it a 3D game: the paddle moves along x and z, and each new ball drops from a random x and a random z. The catch gate checks both gaps. The score and the lives show under the scene. Three misses end the game, r starts it again, and every catch makes the next ball faster. The camera is tilted down so the player can see where the ball will land.",
   "steps": [
     "Start from the card below: the paddle on four keys, the ball at a random x and z, and the catch gate with two gaps.",
     "Add lives and the miss gate from chunk 3, and the score text from chunk 4. Add a second <code>wtext</code> for lives.",
     "Add the state name, the game-over label, and the r restart from chunk 5. The restart also puts the score back to 0 and the ball's speed back to 4.",
     "Add the speed-up line from chunk 6 to the catch gate.",
     "Put <code>scene.forward = vec(0, -0.7, -1)</code> above the loop and write a caption that names the keys.",
   ],
   "cards": [
     {"title": "The catch gate in two directions",
      "teach": "The paddle is 3 wide along x and 3 deep along z, so a catch needs the x gap under 1.5 and the z gap under 1.5. Three checks joined by <code>and</code>. The ball drops from a random x and a random z.",
      "code": code('''
from vpython import *
from random import randint

scene.caption = "Click the scene. Arrow keys move the paddle along x and z."
ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
paddle = box(pos=vec(0, 0.25, 0), size=vec(3, 0.5, 3), color=color.blue)
ball = sphere(pos=vec(1, 8, -1), radius=0.4, color=color.yellow)
ball.vel = vec(0, -4, 0)
dt = 1 / 30
score = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if "right" in keys:
        paddle.pos.x = paddle.pos.x + 0.3
    if "left" in keys:
        paddle.pos.x = paddle.pos.x - 0.3
    if "up" in keys:
        paddle.pos.z = paddle.pos.z - 0.3
    if "down" in keys:
        paddle.pos.z = paddle.pos.z + 0.3

    ball.pos = ball.pos + ball.vel * dt

    gap_x = abs(ball.pos.x - paddle.pos.x)
    gap_z = abs(ball.pos.z - paddle.pos.z)
    if ball.pos.y < 0.9 and gap_x < 1.5 and gap_z < 1.5:
        score = score + 1
        print("caught on pass", passes, "  gaps were", round(gap_x, 2), "and", round(gap_z, 2), "  score", score)
        ball.pos = vec(randint(-4, 4), 8, randint(-4, 4))
'''),
      "run": "vpython",
      "frames": 60,
      "inject": [[10, "HOLD", "up"], [11, "HOLD", "up"], [12, "HOLD", "up"]],
      "predict": "The ball will land at x = 1, z = -1. The paddle starts at the middle and up is held for three passes. Where is the paddle then, and is the ball caught?",
      "reveal": "The paddle is at z = -0.9 after three passes of 0.3 toward negative z, and still at x = 0. The x gap is 1.0 and the z gap is 0.1, both under 1.5, so the ball is caught on pass 54. The output box shows both gaps.</p><p>Had up not been pressed, the z gap would be 1.0, which is also under 1.5, so the ball would be caught anyway. A ball at z = -2 would need the move."},
   ],
   "expected_got": [
     ["A ball that lands beside the paddle is missed, not caught", ""],
     ["Each catch raises the score by exactly 1", ""],
     ["The third miss ends the game and the ball stops", ""],
     ["r during a game does nothing; r after game over starts a new game with 3 lives and score 0", ""],
     ["Every ball after a catch falls faster than the one before", ""],
   ],
 },
 "exits": {
   "floor": "A paddle on the left and right keys and a ball that falls, with the catch gate printing each catch and sending the ball back to the top.",
   "middle": "The 3D catch game: two gaps, score and lives under the scene, game over, r to restart, faster each catch.",
   "stretch": "Two balls in a list, each with its own <code>vel</code>, both falling, with the catch and miss gates inside a loop over the list. Then a bonus ball in a different colour that is worth 3.",
 },
 "ledger": "Stamp 7: <code>abs(a - b)</code> is a gap, <code>randint(lo, hi)</code> from <code>random</code>, a catch is two checks joined by <code>and</code>, a gate that should fire once must change what it checks, <code>wtext</code> and <code>text = \"Score: \" + str(score)</code>, lives, a <code>state</code> name gated on everywhere, restart with a key in the loop, <code>ball.vel.y - 1</code> to speed up.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunk 1, paddle and ball, 8 min",
     "0:18 chunk 2, the catch gate, 15 min (abs and the random restart are the teaching points)",
     "0:33 chunks 3 and 4, lives and the score text, 15 min",
     "0:48 chunk 5, state and restart, 15 min",
     "1:03 chunk 6, speeding up, 5 min",
     "1:08 hinge question, 7 min",
     "1:15 build brief, 10 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Catches the same ball on every pass and the score runs away.", "That is the hinge. The gate's body has to send the ball back to the top so the gate closes."],
     ["Writes the x gap without <code>abs</code> and only catches balls on one side of the paddle.", "A ball 1 to the left gives a gap of -1, which is less than 1.5, but a ball 1 to the right gives 1. Without abs, the check is about which side, not how far. Print the gap for a ball on each side."],
     ["Joins the score to the text with <code>+ score</code> and gets a TypeError.", "A number and a string cannot be joined. <code>str(score)</code> first. Chunk 4's reveal has the exact error."],
     ["Puts the restart in a Reset button and finds that score and lives do not change.", "The button's function cannot assign to the loop's variables. Use the r key inside the loop, as chunk 5 does, or put the numbers on the paddle as attributes, as session 6 did with the sun."],
     ["Lets the game keep dropping balls after lives hit 0, and lives go negative.", "The ball's movement has to be gated on <code>state == \"play\"</code>. Every line that belongs to playing gets that gate."],
   ],
   "standards": ["NY-6.NS.8", "NY-6.EE.5", "MP1"],
   "routing": "Chunk 6 is one line and can be folded into the build brief. Chunk 3 and chunk 4 can be shown together on the projector. If the room is behind, the build is the card plus lives, and state and restart become the stretch.",
 },
},
]
