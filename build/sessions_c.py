"""Sessions 7 to 10 of the VPython course: every word and every snippet.

Same shape as sessions_a.py. render.py runs each snippet through
vpython_harness.py and pastes the real terminal output into the page.
"""


def code(text):
    return text.lstrip("\n").rstrip() + "\n"


SESSIONS_C = [

# =====================================================================
{
 "num": 7,
 "slug": "session07_a_grid_world_from_a_list_of_strings",
 "title": "A grid world: a level from a list of strings",
 "subtitle": "A maze drawn from text, row and column numbers that become places, a player that moves one tile per tap and cannot walk through walls, a goal, and coins",
 "new": ["a level as a list of strings", "indexing a string", "row then column", "nested loops", "row and col as attributes", "a place function", "is_open and !=", "a goal tile", "coins in a list"],
 "reuse": "Session 1: a bound keydown function. Session 5: attributes on an object, a list of objects",
 "env_note": True,
 "reuse_note": "Row first, then column, and row is z. Both will be swapped by someone in the first ten minutes. Chunk 1 has the room print <code>level[2][2]</code> and <code>level[3][5]</code> and find them with a finger on the projected level before anything is drawn.",
 "opener": {
   "title": "Retrieval: gates that fire once, and attributes",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "A catch gate adds 1 to the score and does nothing else. Why does the score climb 30 times a second, and what has to be in the gate's body?",
      "a": "The gate is True on every pass while the ball is over the paddle, so the body runs every pass. The body has to change what the gate checks, by sending the ball back to the top, so the gate closes."},
     {"q": "What does <code>abs(3 - 5)</code> give, and what is abs for in a game?",
      "a": "2. abs throws away the minus sign, so a gap is the same number whichever side the ball is on."},
     {"q": "<code>player.score = 0</code> is written above the loop. Can a bound function add to it? Could it add to a plain variable called <code>score</code>?",
      "a": "Yes to the first: the attribute lives on the player, and any function that can see the player can change it. No to the second: a function cannot assign to a plain variable that lives outside it. That is why the course puts shared numbers on objects."},
   ],
 },
 "chunks": [
  {"title": "A level is a list of strings",
   "teach": "Each string is one row of the level, read from the far edge to the near edge. <code>#</code> is a wall, <code>.</code> is floor, and <code>G</code> is the goal. A string can be indexed like a list: <code>level[2]</code> is the third row, and <code>level[2][2]</code> is the third character of it. Row first, then column, and both start at 0.",
   "code": code('''
from vpython import *

level = [
    "#######",
    "#.....#",
    "#.##..#",
    "#....G#",
    "#######",
]
print(len(level), "rows")
print(len(level[0]), "columns")
print("row 2 is", level[2])
print("row 2, column 2 is", level[2][2])
print("row 3, column 5 is", level[3][5])
'''),
   "run": "vpython",
   "predict": "Which pair of indexes finds the G? Say the row and the column, in that order. What is at row 2, column 2?",
   "reveal": "The G is at row 3, column 5: <code>level[3][5]</code>. Count rows from the top starting at 0, then characters from the left starting at 0.</p><p>Row 2, column 2 is <code>#</code>, the first of the two walls in the middle of the third row. Reading it as column 2, row 2 happens to give the same character on this level, because the level is nearly square; on a level that is 5 by 7 the swap gives a different answer, and the build brief's level is 9 by 9 so that the mistake shows."},

  {"title": "Two loops draw the walls",
   "teach": "A loop over the rows, and inside it a loop over the characters in that row. Every <code>#</code> becomes a box. The column number becomes x and the row number becomes z, each with 3 or 2 subtracted so the level is centred on the middle of the world.</p><p>Row 0 is the far edge, at negative z, the way the top line of a map is the far side when the map lies flat on a table.",
   "code": code('''
from vpython import *

level = [
    "#######",
    "#.....#",
    "#.##..#",
    "#....G#",
    "#######",
]
walls = 0

for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "#":
            box(pos=vec(col - 3, 0.5, row - 2), color=color.gray(0.6))
            walls = walls + 1

print(walls, "wall blocks")
print("the top-left wall, row 0 col 0, is at", vec(0 - 3, 0.5, 0 - 2))
print("the bottom-right wall, row 4 col 6, is at", vec(6 - 3, 0.5, 4 - 2))
'''),
   "run": "vpython",
   "predict": "How many wall blocks are drawn? The top-left wall is row 0, column 0. Is it near you or far away, on the left or the right?",
   "reveal": "22: seven on the top row, seven on the bottom, two on the second and fourth rows, and four on the middle row.</p><p>The top-left wall is at <code>&lt;-3, 0.5, -2&gt;</code>: on the left, because column 0 gives the smallest x, and far away, because row 0 gives the smallest z and negative z is away from you. The bottom-right wall is at <code>&lt;3, 0.5, 2&gt;</code>, on the right and near you."},

  {"title": "The player has a row and a column",
   "teach": "The player's place in the level is a row and a column, kept on the player as two attributes. A function called <code>place</code> turns them into a pos with the same arithmetic the walls used. Change the row or column, call <code>place</code>, and the player appears on the new tile.",
   "code": code('''
from vpython import *

player = sphere(radius=0.4, color=color.yellow)
player.row = 1
player.col = 1

def place(thing):
    thing.pos = vec(thing.col - 3, 0.5, thing.row - 2)

place(player)
print("player at row", player.row, "col", player.col, "  pos", player.pos)

player.col = 4
place(player)
print("after moving to col 4,  pos", player.pos)
'''),
   "run": "vpython",
   "predict": "After <code>player.col = 4</code> and <code>place(player)</code>, which of the three pos numbers changes, and to what?",
   "reveal": "Only x changes, from -2 to 1: column 4 minus 3. The row is still 1, so z is still -1, and y is always 0.5.</p><p><code>place</code> works on any object that has a row and a col, which is why its parameter is called <code>thing</code>. The coins in chunk 6 use the same function."},

  {"title": "One step per tap, and a wall says no",
   "teach": "Each arrow tap works out the row and column the player wants to go to, and a function called <code>is_open</code> says whether that tile is floor. <code>!=</code> means is not equal to, so <code>is_open</code> returns True for any character except a wall. If the tile is open, the player's row and column change and <code>place</code> moves it. If not, nothing changes.</p><p>The ring of <code>#</code> around the edge of the level is what keeps the row and column inside the list. Without it a step off the edge would ask for a row that does not exist.",
   "code": code('''
from vpython import *

scene.caption = "Click the scene, then tap the arrow keys."
level = [
    "#######",
    "#.....#",
    "#.##..#",
    "#....G#",
    "#######",
]
for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "#":
            box(pos=vec(col - 3, 0.5, row - 2), color=color.gray(0.6))

player = sphere(radius=0.4, color=color.yellow)
player.row = 1
player.col = 1

def place(thing):
    thing.pos = vec(thing.col - 3, 0.5, thing.row - 2)

def is_open(row, col):
    return level[row][col] != "#"

def step(evt):
    new_row = player.row
    new_col = player.col
    if evt.key == "up":
        new_row = player.row - 1
    if evt.key == "down":
        new_row = player.row + 1
    if evt.key == "left":
        new_col = player.col - 1
    if evt.key == "right":
        new_col = player.col + 1

    if is_open(new_row, new_col):
        player.row = new_row
        player.col = new_col
        place(player)
        print(evt.key, "-> row", player.row, "col", player.col)
    else:
        print(evt.key, "-> blocked by a wall")

place(player)
scene.bind("keydown", step)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 10,
   "inject": [[1, "KEYDOWN", "right"], [2, "KEYDOWN", "right"], [3, "KEYDOWN", "down"], [4, "KEYDOWN", "right"], [5, "KEYDOWN", "down"], [6, "KEYDOWN", "down"]],
   "predict": "The player starts at row 1, column 1. The taps are right, right, down, right, down, down. Which tap is blocked, and where is the player at the end?",
   "reveal": "The first down is blocked. After two rights the player is at row 1, column 3, and row 2, column 3 is a <code>#</code>, so <code>is_open</code> returns False and the player stays. The output box shows that line as blocked.</p><p>At the end the player is at row 3, column 4: the third right takes it to column 4, and the two downs take it to row 3, because rows 2 and 3 are open at column 4. The up arrow makes the row smaller, because row 0 is the far edge."},

  {"title": "A goal tile, and counting the steps",
   "teach": "After each move, look at the character under the player. If it is <code>G</code>, the player has won. A counter on the player, <code>player.steps</code>, goes up by one for each move that happened, and a label says how many it took. A blocked tap is not a step.",
   "code": code('''
from vpython import *

level = [
    "#######",
    "#.....#",
    "#.##..#",
    "#....G#",
    "#######",
]
for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "#":
            box(pos=vec(col - 3, 0.5, row - 2), color=color.gray(0.6))

player = sphere(radius=0.4, color=color.yellow)
player.row = 1
player.col = 1
player.steps = 0
sign = label(pos=vec(0, 2, 0), text="", height=20, box=False)

def place(thing):
    thing.pos = vec(thing.col - 3, 0.5, thing.row - 2)

def is_open(row, col):
    return level[row][col] != "#"

def step(evt):
    new_row = player.row
    new_col = player.col
    if evt.key == "up":
        new_row = player.row - 1
    if evt.key == "down":
        new_row = player.row + 1
    if evt.key == "left":
        new_col = player.col - 1
    if evt.key == "right":
        new_col = player.col + 1

    if is_open(new_row, new_col):
        player.row = new_row
        player.col = new_col
        player.steps = player.steps + 1
        place(player)

    if level[player.row][player.col] == "G":
        sign.text = "You reached the goal in " + str(player.steps) + " steps"
        print(sign.text)

place(player)
scene.bind("keydown", step)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 10,
   "inject": [[1, "KEYDOWN", "right"], [2, "KEYDOWN", "right"], [3, "KEYDOWN", "down"], [4, "KEYDOWN", "right"], [5, "KEYDOWN", "down"], [6, "KEYDOWN", "down"], [7, "KEYDOWN", "right"]],
   "predict": "The same taps as chunk 4, then one more right. Does the player reach the G? How many steps does the label say, and why is it not 7?",
   "reveal": "Yes. The last right takes the player from row 3, column 4 to row 3, column 5, which is the G. The label says 6 steps.</p><p>Seven taps were made, but one of them, the first down, was blocked, and <code>player.steps</code> only goes up inside the gate that moves the player. A tap that moved nothing is not counted."},

  {"title": "Coins are objects in a list, each with a row and a column",
   "teach": "A coin is a small sphere with its own row and col, placed by the same <code>place</code> function. The drawing loop makes one for every <code>o</code> in the level and appends it to a list. After each move, a loop over the coins asks whether any visible coin is on the player's tile. If one is, it is hidden and the score goes up.",
   "code": code('''
from vpython import *

level = [
    "#######",
    "#.o...#",
    "#.##o.#",
    "#..o.G#",
    "#######",
]
coins = []
for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "#":
            box(pos=vec(col - 3, 0.5, row - 2), color=color.gray(0.6))
        if level[row][col] == "o":
            c = sphere(radius=0.15, color=color.yellow)
            c.row = row
            c.col = col
            coins.append(c)

player = sphere(radius=0.4, color=color.cyan)
player.row = 1
player.col = 1
player.score = 0

def place(thing):
    thing.pos = vec(thing.col - 3, 0.5, thing.row - 2)

def is_open(row, col):
    return level[row][col] != "#"

def step(evt):
    new_row = player.row
    new_col = player.col
    if evt.key == "up":
        new_row = player.row - 1
    if evt.key == "down":
        new_row = player.row + 1
    if evt.key == "left":
        new_col = player.col - 1
    if evt.key == "right":
        new_col = player.col + 1

    if is_open(new_row, new_col):
        player.row = new_row
        player.col = new_col
        place(player)

    for c in coins:
        if c.visible and c.row == player.row and c.col == player.col:
            c.visible = False
            player.score = player.score + 1
            print("coin at row", c.row, "col", c.col, "  score", player.score)

for c in coins:
    place(c)
place(player)
scene.bind("keydown", step)
print(len(coins), "coins on the level")

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 10,
   "inject": [[1, "KEYDOWN", "right"], [2, "KEYDOWN", "right"], [3, "KEYDOWN", "right"], [4, "KEYDOWN", "down"], [5, "KEYDOWN", "down"], [6, "KEYDOWN", "right"], [7, "KEYDOWN", "left"]],
   "predict": "There are three coins. The taps are right, right, right, down, down, right, left. How many coins are collected, and why does the last left, which moves the player back onto a coin's tile, not score again?",
   "reveal": "Two coins: the one at row 1, column 2 on the first right, and the one at row 2, column 4 on the first down. The coin at row 3, column 3 is never stepped on.</p><p>The last left moves the player back to row 3, column 4, which never had a coin, so nothing scores. Even on a tile that did have one, the gate checks <code>c.visible</code> first, and a collected coin is hidden, so it cannot be collected twice. Hiding the coin is the change that closes the gate, the same idea as the catch gate sending the ball back to the top."},
 ],
 "hinge": {"q": "A level is 5 strings long and each string has 7 characters. Give <code>len(level)</code> and <code>len(level[0])</code>. Give the row and column of the bottom-right corner. Then say which of row and column becomes x in the drawing, and which becomes z.",
           "a": "<code>len(level)</code> is 5, the number of rows. <code>len(level[0])</code> is 7, the number of characters in a row.</p><p>The bottom-right corner is row 4, column 6: one less than each length, because both start at 0.</p><p>Column becomes x, because columns run across. Row becomes z, because rows run from far to near. Swapping them draws the level turned on its side."},
 "brief": {
   "title": "Build: the coin maze",
   "minutes": 20,
   "intro": "A maze 9 by 9 drawn from a list of strings, with walls, a start, coins, and a goal. The player moves one tile per arrow tap and cannot walk through walls. A line of text under the scene shows the score and the step count. Reaching the goal shows a label. Pressing r puts the player back at the start, the coins back, and the counts back to 0. The camera looks down at the maze from above.",
   "steps": [
     "Start from the card below: the 9 by 9 level, the drawing loop with the middle column and middle row as two named numbers, and <code>place</code> written from them.",
     "Add the player at row 1, column 1 with <code>row</code>, <code>col</code>, <code>steps</code> and <code>score</code> attributes, and the <code>step</code> function from chunk 6 with the step counter from chunk 5.",
     "Add a <code>wtext</code> under the scene and set its text after every move: <code>\"Coins: \" + str(player.score) + \"   Steps: \" + str(player.steps)</code>.",
     "Add the goal label from chunk 5.",
     "Add a restart: a key <code>r</code> inside the <code>step</code> function that puts the player's row and col back to 1, both counters back to 0, every coin's <code>visible</code> back to True, and the label's text back to empty.",
     "Put <code>scene.forward = vec(0, -1, -0.3)</code> and <code>scene.range = 6</code> above the loop so the whole maze is in view from above.",
   ],
   "cards": [
     {"title": "A bigger level, with the middle written once",
      "teach": "Nine columns and nine rows, so the middle is column 4 and row 4. Those two numbers are written once at the top, and both the drawing loop and <code>place</code> use them. Change the level's size and only those two numbers change.",
      "code": code('''
from vpython import *

level = [
    "#########",
    "#..o#...#",
    "#.#.#.#.#",
    "#.#...#o#",
    "#.#####.#",
    "#o..#...#",
    "#.#.#.#.#",
    "#...#..G#",
    "#########",
]
mid_col = 4
mid_row = 4
coins = []
walls = 0

for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "#":
            box(pos=vec(col - mid_col, 0.5, row - mid_row), color=color.gray(0.6))
            walls = walls + 1
        if level[row][col] == "o":
            c = sphere(radius=0.15, color=color.yellow)
            c.row = row
            c.col = col
            coins.append(c)

def place(thing):
    thing.pos = vec(thing.col - mid_col, 0.5, thing.row - mid_row)

for c in coins:
    place(c)

print(walls, "walls and", len(coins), "coins")
print("the middle tile, row 4 col 4, is at", vec(4 - mid_col, 0.5, 4 - mid_row))
print("the goal, row 7 col 7, is at", vec(7 - mid_col, 0.5, 7 - mid_row))
'''),
      "run": "vpython",
      "predict": "Where does the middle tile of the level land in the world? The goal is at row 7, column 7: is it near you or far away, left or right?",
      "reveal": "The middle tile lands at <code>&lt;0, 0.5, 0&gt;</code>, the middle of the world, because 4 minus 4 is 0 for both the column and the row. That is what the two <code>mid</code> numbers are for.</p><p>The goal is at <code>&lt;3, 0.5, 3&gt;</code>: on the right, because column 7 is past the middle, and near you, because row 7 is one of the last rows and the last rows are the near edge. The output box also counts 48 walls and 3 coins."},
   ],
   "expected_got": [
     ["A tap toward a wall leaves the player where it is and adds no step", ""],
     ["Each coin can be collected once", ""],
     ["The text under the scene changes on every move", ""],
     ["Reaching the G shows the label with the real step count", ""],
     ["r puts the player, the coins, and both counts back", ""],
   ],
 },
 "exits": {
   "floor": "The 9 by 9 level drawn from the card, with the player on the start tile and the arrow keys moving it one tile per tap, walls or no walls.",
   "middle": "The coin maze: walls that block, coins that score once, the text under the scene, the goal label, r to restart.",
   "stretch": "A second level as another list of strings. Reaching the G hides every wall of the first level, draws the second, and puts the player at its start. Then a timer: a counter in the loop that counts passes, shown as seconds under the scene.",
 },
 "ledger": "Stamp 7: a level is a list of strings, <code>level[row][col]</code> with row first, a string is indexed like a list, column becomes x and row becomes z, two loops with <code>range(len(...))</code>, <code>!=</code>, <code>is_open(row, col)</code> checked before the move, <code>place(thing)</code> from row and col attributes, a wall ring keeps the indexes inside the list, coins in a list hidden once.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunks 1 and 2, the level and the drawing loops, 18 min (fingers on the projected level)",
     "0:28 chunk 3, row and col as attributes, 7 min",
     "0:35 chunk 4, the step function, 15 min (the core of the session)",
     "0:50 chunks 5 and 6, the goal and the coins, 15 min",
     "1:05 hinge question, 5 min",
     "1:10 build brief, 15 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Writes <code>level[col][row]</code> and the maze is drawn turned on its side.", "Row first. Have them print <code>level[1][2]</code> and <code>level[2][1]</code> on the 9 by 9 level, where the two are different characters."],
     ["Expects the up arrow to make the row bigger.", "Row 0 is the far edge, so up is toward the far edge, which is a smaller row. Walk it on the projected level."],
     ["Leaves a gap in the wall ring and gets <code>IndexError: string index out of range</code> when the player walks off the edge.", "A row or column past the edge asks the list or the string for something it does not have. The ring of walls is the gate that keeps the numbers inside. Close the ring."],
     ["Moves the player by changing <code>player.pos</code> directly and the wall check stops working.", "The row and col are what the level knows about. Change those and call <code>place</code>, never pos on its own."],
     ["Collects the same coin again after walking back over it.", "The coin has to be hidden, and the gate has to check <code>c.visible</code> first. Both lines are in chunk 6."],
   ],
   "standards": ["NY-5.G.2", "NY-6.NS.8", "MP7"],
   "routing": "Chunk 6 can become the build brief's step 2 if time is short; the coin loop is the same shape as the catch gate. Chunk 3 can be shown on the projector in three minutes. The hinge is quick and should stay; the swap is the bug the build will hit.",
 },
},

# =====================================================================
{
 "num": 8,
 "slug": "session08_a_scene_editor_dragging_with_the_mouse",
 "title": "A scene editor: dragging with the mouse",
 "subtitle": "mousedown, mousemove and mouseup, a grabbed object that follows the mouse across the floor, a menu that picks the shape, and a checkbox that turns a click into a delete",
 "new": ["mousedown, mousemove, mouseup", "evt.press", "an attribute that holds what is held", "project onto the floor at a height", "snap with round on drop", "menu and m.selected", "checkbox and c.checked"],
 "reuse": "Session 1: click, scene.mouse.pick, the gate on None, project. Session 5: attributes that share a number between functions",
 "env_note": True,
 "reuse_note": "The shared thing here is an object, not a number: <code>floor.held</code> is the shape being dragged, or None. It is the same move as <code>sun.factor</code> in session 5. Say so when chunk 2 arrives, because three functions have to agree on what is held and students will reach for a plain variable.",
 "opener": {
   "title": "Retrieval: picks, None, and project",
   "minutes": 10,
   "body": "Paper first.",
   "questions": [
     {"q": "Inside a click function, what does <code>scene.mouse.pick</code> hold when the click was on empty space, and what happens if the next line is <code>thing.color = color.red</code>?",
      "a": "None. The next line asks None for a colour and the program stops with an AttributeError. The gate <code>if thing is None:</code> has to come first."},
     {"q": "What does <code>scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0, 0))</code> give?",
      "a": "The point where the mouse's line of sight meets a flat plane that faces up and passes through the middle of the world: the place on the floor that the mouse is over."},
     {"q": "Three functions need to know the same thing. Where does the course keep it, and why not in a plain variable?",
      "a": "On an object, as an attribute, the way <code>sun.factor</code> was kept on the sun. A function cannot assign to a plain variable outside itself, but it can assign to an attribute of any object it can see."},
   ],
 },
 "chunks": [
  {"title": "Three events make a drag",
   "teach": "A click is a press and a release in one place. A drag is a press, some moves, and a release somewhere else, and VPython reports each part as its own event: <code>mousedown</code>, <code>mousemove</code>, <code>mouseup</code>. Bind one function to each.</p><p><code>mousemove</code> happens every time the mouse moves, button or no button. <code>evt.press</code> is True on a move while the button is held, which is how a function can tell a drag from a wander.",
   "code": code('''
from vpython import *

scene.caption = "Press on the box, move, and let go."
crate = box(pos=vec(0, 0.5, 0), color=color.orange)

def down(evt):
    print("mousedown   press is", evt.press)

def move(evt):
    print("mousemove   press is", evt.press)

def up(evt):
    print("mouseup     press is", evt.press)

scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[1, "MOUSEDOWN", [0, 0.5, 0]], [2, "MOUSEMOVE", [1, 0.5, 0]], [3, "MOUSEUP", [1, 0.5, 0]], [5, "MOUSEMOVE", [2, 0.5, 0]]],
   "predict": "The mouse presses on the box, moves once, lets go, and then moves once more with no button down. Four events. For which of them is <code>evt.press</code> True?",
   "reveal": "Only the first two. <code>mousedown</code> is a press, and the move right after it happens with the button still down, so both print True. <code>mouseup</code> is the release, and the last move happens with no button down, so both print False.</p><p>In a real run there would be many more <code>mousemove</code> lines, one for every small movement, which is why the next chunks only act on a move when something is held."},

  {"title": "Grab: remember what was pressed on",
   "teach": "On <code>mousedown</code>, look at the pick. If it is a shape and not the floor, remember it in <code>floor.held</code>. The floor is the one object every function can see, so an attribute on it is where the three drag functions keep what they share. When nothing is held, <code>floor.held</code> is None.",
   "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.held = None
crate = box(pos=vec(2, 0.5, 0), color=color.orange)
ball = sphere(pos=vec(-2, 0.5, 0), radius=0.5, color=color.cyan)

def grab(evt):
    thing = scene.mouse.pick
    if thing is None or thing is floor:
        floor.held = None
        print("pressed on nothing to grab")
    else:
        floor.held = thing
        print("grabbed the thing at", floor.held.pos)

scene.bind("mousedown", grab)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[1, "MOUSEDOWN", [2, 0.5, 0]], [3, "MOUSEDOWN", [0, 0, 3]], [5, "MOUSEDOWN", [-2, 0.5, 0]]],
   "predict": "Three presses: on the crate, on an empty patch of floor, and on the ball. What does <code>floor.held</code> hold after each one?",
   "reveal": "After the first press it holds the crate, and the print shows the crate's pos. After the second it holds None: the pick was the floor, and the gate treats the floor like empty space. After the third it holds the ball.</p><p>The gate uses <code>or</code>: either reason, None or the floor, means there is nothing to grab. Without the floor check, a press on the floor would grab the floor, and the next chunk would drag the whole ground around."},

  {"title": "Drag: move what is held to where the mouse is",
   "teach": "On <code>mousemove</code>, if something is held, put it where the mouse is on the floor. <code>project</code> from session 1 finds that point, with one change: the plane is at height 0.5, <code>point=vec(0, 0.5, 0)</code>, so the dragged shape's middle stays half a unit up and the shape slides along the floor instead of sinking into it.",
   "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.held = None
crate = box(pos=vec(2, 0.5, 0), color=color.orange)
scene.forward = vec(0, -0.6, -1)

def grab(evt):
    thing = scene.mouse.pick
    if thing is None or thing is floor:
        floor.held = None
    else:
        floor.held = thing

def drag(evt):
    if floor.held is not None:
        spot = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0.5, 0))
        floor.held.pos = spot
        print("dragged to", spot)

scene.bind("mousedown", grab)
scene.bind("mousemove", drag)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[1, "MOUSEDOWN", [2, 0.5, 0]], [2, "MOUSEMOVE", [2.8, 0.5, 1.1]], [3, "MOUSEMOVE", [3.6, 0.5, 2.3]]],
   "predict": "The mouse presses on the crate and moves twice. After the second move, what is the crate's y, and why is it not 0?",
   "reveal": "The crate's y is 0.5 after every move. The plane that <code>project</code> uses passes through <code>vec(0, 0.5, 0)</code>, so every point it gives has y = 0.5, and the crate's middle stays half a unit above the floor.</p><p>With <code>point=vec(0, 0, 0)</code> the crate's middle would be put on the floor itself, and half of it would be under the ground, the session 1 mistake made by the mouse instead of by a typed number."},

  {"title": "Drop: let go, and snap to the grid",
   "teach": "On <code>mouseup</code>, if something is held, round its x and z to whole numbers so it lands on a grid, then set <code>floor.held</code> to None so moves stop dragging it. The crate's y does not need rounding, because the drag kept it at 0.5.",
   "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.held = None
crate = box(pos=vec(2, 0.5, 0), color=color.orange)
scene.forward = vec(0, -0.6, -1)

def grab(evt):
    thing = scene.mouse.pick
    if thing is None or thing is floor:
        floor.held = None
    else:
        floor.held = thing

def drag(evt):
    if floor.held is not None:
        floor.held.pos = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0.5, 0))

def drop(evt):
    if floor.held is not None:
        floor.held.pos = vec(round(floor.held.pos.x), 0.5, round(floor.held.pos.z))
        print("dropped at", floor.held.pos)
        floor.held = None

scene.bind("mousedown", grab)
scene.bind("mousemove", drag)
scene.bind("mouseup", drop)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[1, "MOUSEDOWN", [2, 0.5, 0]], [2, "MOUSEMOVE", [3.6, 0.5, 2.3]], [3, "MOUSEUP", [3.6, 0.5, 2.3]], [5, "MOUSEMOVE", [-4, 0.5, -4]]],
   "predict": "The crate is dragged to x = 3.6, z = 2.3 and dropped there. Where does it land? After the drop, the mouse moves again. Does the crate follow it?",
   "reveal": "It lands at <code>&lt;4, 0.5, 2&gt;</code>: 3.6 rounds to 4 and 2.3 rounds to 2.</p><p>The crate does not follow the later move. <code>drop</code> set <code>floor.held</code> to None, so the gate in <code>drag</code> is False and the move does nothing. That line is what ends a drag; without it, every move for the rest of the program would carry the crate along."},

  {"title": "A menu picks the shape, and a click on the floor makes one",
   "teach": "A <b>menu</b> is a drop-down list under the scene. Its function gets the menu, and <code>m.selected</code> is the word that was chosen. The chosen shape is kept on the floor, as <code>floor.tool</code>, so the click function can read it.</p><p>A click on the floor makes the chosen shape at the clicked spot. A box's pos is its middle, so it goes at y = 0.5. A cone's pos is its flat end, so it goes at y = 0 and points up.",
   "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.tool = "box"
scene.forward = vec(0, -0.6, -1)

def pick_tool(m):
    floor.tool = m.selected
    print("tool is now", floor.tool)

menu(choices=["box", "ball", "cone"], bind=pick_tool)

def make(evt):
    if scene.mouse.pick is floor:
        spot = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0, 0))
        x = round(spot.x)
        z = round(spot.z)
        if floor.tool == "box":
            thing = box(pos=vec(x, 0.5, z), color=color.orange)
        if floor.tool == "ball":
            thing = sphere(pos=vec(x, 0.5, z), radius=0.5, color=color.cyan)
        if floor.tool == "cone":
            thing = cone(pos=vec(x, 0, z), axis=vec(0, 1, 0), radius=0.5, color=color.red)
        print("made a", floor.tool, "at", thing.pos)

scene.bind("click", make)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[1, "CLICK", [1.2, 0, 1.8]], [3, "WIDGET", "pick_tool", 2], [4, "CLICK", [-3.4, 0, 0.6]], [6, "CLICK", [-3.4, 0, 0.6]]],
   "predict": "A click on the floor, then the menu is set to cone, then two clicks at the same spot. What is made by each click, and why does the third click make nothing?",
   "reveal": "The first click makes a box at <code>&lt;1, 0.5, 2&gt;</code>, because the tool starts as box. The second makes a cone at <code>&lt;-3, 0, 1&gt;</code>: y is 0 for a cone, because its pos is its flat end.</p><p>The third click is on the same spot, where the cone now stands, so the pick is the cone and not the floor. The gate <code>scene.mouse.pick is floor</code> is False and nothing is made. A click on a shape is the next chunk's job."},

  {"title": "A checkbox turns a press into a delete",
   "teach": "A <b>checkbox</b> is a tick box under the scene. Its function gets the checkbox, and <code>c.checked</code> is True while it is ticked. Keep it on the floor as <code>floor.delete</code>. In <code>grab</code>, a press on a shape while delete mode is on hides the shape instead of holding it.",
   "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.held = None
floor.delete = False
crate = box(pos=vec(2, 0.5, 0), color=color.orange)
ball = sphere(pos=vec(-2, 0.5, 0), radius=0.5, color=color.cyan)

def set_delete(c):
    floor.delete = c.checked
    print("delete mode is", floor.delete)

checkbox(text="Delete mode", bind=set_delete)

def grab(evt):
    thing = scene.mouse.pick
    if thing is None or thing is floor:
        floor.held = None
    elif floor.delete:
        thing.visible = False
        print("deleted the thing at", thing.pos)
    else:
        floor.held = thing
        print("grabbed the thing at", thing.pos)

scene.bind("mousedown", grab)

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[1, "MOUSEDOWN", [2, 0.5, 0]], [3, "WIDGET", "set_delete", True], [4, "MOUSEDOWN", [-2, 0.5, 0]], [6, "MOUSEDOWN", [-2, 0.5, 0]]],
   "predict": "A press on the crate, then the box is ticked, then two presses on the ball. What happens on each press? Why does the last press not delete anything?",
   "reveal": "The first press grabs the crate, because delete mode is off. The second press, after the tick, deletes the ball: it is hidden. The third press is on the same spot, but a hidden shape cannot be picked, so the pick is the floor and the first gate catches it. Nothing is deleted and nothing is grabbed.</p><p><code>elif</code> is a second gate that is only checked when the first was False. Here it means: not nothing, and delete mode is on."},
 ],
 "hinge": {"q": "From session 1: a student's dragged shape sinks half into the floor while it is being dragged, then pops up to the right height when it is dropped. Which line has the mistake, which argument in it, and what is the right value?",
           "a": "The <code>project</code> line inside <code>drag</code>. Its <code>point</code> argument is <code>vec(0, 0, 0)</code>, so the plane the mouse is projected onto is the floor itself, and a box's middle is put on the floor. The right value is <code>vec(0, 0.5, 0)</code>, half the box's height up.</p><p>The drop looks right because <code>drop</code> builds a new pos with 0.5 written in. The drag has to use the same height."},
 "brief": {
   "title": "Build: the scene editor",
   "minutes": 15,
   "intro": "An editor for building a scene with the mouse. A menu picks the shape and a second menu picks the colour. A click on the floor makes the chosen shape there. A press on a shape grabs it, moving the mouse drags it across the floor, and letting go drops it on the grid. A Delete mode checkbox turns a press into a delete. A line of text under the scene counts the shapes that are standing, and a Reset button hides them all.",
   "steps": [
     "Start from the card below: the shape menu, the colour menu, and the click that makes a shape and appends it to a list.",
     "Add <code>grab</code>, <code>drag</code> and <code>drop</code> from chunks 2 to 4, with the delete gate from chunk 6 in <code>grab</code>.",
     "Add a <code>wtext</code> under the scene. After every make and every delete, count the shapes in the list whose <code>visible</code> is True, with a loop and a counter, and set the text to <code>\"Shapes: \" + str(count)</code>.",
     "Add a Reset button whose function hides every shape in the list and sets the text to Shapes: 0.",
     "Write a caption that says what a click, a drag, and the tick box do.",
   ],
   "cards": [
     {"title": "Two menus, and a shape with the right height for its kind",
      "teach": "The colour menu works like the shape menu: its function puts the chosen colour on the floor as <code>floor.paint</code>. Every shape made goes into a list so that the count and the Reset can reach it. A cone's pos is its flat end, so it sits at y = 0; a box and a ball have their middle at y = 0.5.",
      "code": code('''
from vpython import *

floor = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
floor.tool = "box"
floor.paint = color.orange
shapes = []
scene.forward = vec(0, -0.6, -1)

def pick_tool(m):
    floor.tool = m.selected

def pick_paint(m):
    if m.selected == "orange":
        floor.paint = color.orange
    if m.selected == "cyan":
        floor.paint = color.cyan
    if m.selected == "white":
        floor.paint = color.white
    print("paint is now", floor.paint)

menu(choices=["box", "ball", "cone"], bind=pick_tool)
scene.append_to_caption("  ")
menu(choices=["orange", "cyan", "white"], bind=pick_paint)

def make(evt):
    if scene.mouse.pick is floor:
        spot = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 0, 0))
        x = round(spot.x)
        z = round(spot.z)
        if floor.tool == "box":
            thing = box(pos=vec(x, 0.5, z), color=floor.paint)
        if floor.tool == "ball":
            thing = sphere(pos=vec(x, 0.5, z), radius=0.5, color=floor.paint)
        if floor.tool == "cone":
            thing = cone(pos=vec(x, 0, z), axis=vec(0, 1, 0), radius=0.5, color=floor.paint)
        shapes.append(thing)
        print("shape", len(shapes), "is a", floor.tool, "at", thing.pos, "coloured", thing.color)

scene.bind("click", make)

while True:
    rate(30)
'''),
      "run": "vpython",
      "frames": 8,
      "inject": [[1, "CLICK", [2, 0, 2]], [2, "WIDGET", "pick_paint", 1], [3, "WIDGET", "pick_tool", 1], [4, "CLICK", [-2, 0, 2]], [6, "CLICK", [0, 0, -3]]],
      "predict": "A click, then the paint is set to cyan and the tool to ball, then two more clicks. What colour and kind is each of the three shapes, and how long is the list at the end?",
      "reveal": "The first shape is an orange box, made before either menu changed. The second and third are cyan balls, at <code>&lt;-2, 0.5, 2&gt;</code> and <code>&lt;0, 0.5, -3&gt;</code>. The list holds 3 at the end, and the output box numbers them.</p><p>The colour prints as a vector, <code>&lt;0, 1, 1&gt;</code> for cyan, because a colour is three numbers."},
   ],
   "expected_got": [
     ["A click on the floor makes the shape and colour the menus show", ""],
     ["A dragged shape stays on the floor and lands on whole-number x and z", ""],
     ["A press on a shape with the tick on hides it and adds nothing", ""],
     ["The count under the scene matches the shapes you can see", ""],
     ["Reset hides everything and shows Shapes: 0", ""],
   ],
 },
 "exits": {
   "floor": "The three drag functions on one crate: press, drag along the floor, drop on the grid.",
   "middle": "The scene editor: two menus, make on click, drag, delete mode, the count, Reset.",
   "stretch": "A height slider: a dragged shape's y follows the slider, so shapes can be stacked. Then a Save key that prints every visible shape's kind and pos in the terminal, one line each, so a scene can be typed back in later.",
 },
 "ledger": "Stamp 8: <code>mousedown</code>, <code>mousemove</code>, <code>mouseup</code>, <code>evt.press</code>, what is held lives on an object (<code>floor.held</code>, or None), <code>project</code> onto a plane at the shape's height, <code>round</code> on drop, <code>menu(choices, bind)</code> and <code>m.selected</code>, <code>checkbox(text, bind)</code> and <code>c.checked</code>, <code>elif</code>, a hidden shape cannot be picked.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 10 min",
     "0:10 chunk 1, three events, 8 min",
     "0:18 chunks 2 to 4, grab, drag, drop, 25 min (the core of the session; build it up live)",
     "0:43 chunk 5, the menu, 10 min",
     "0:53 chunk 6, delete mode, 10 min",
     "1:03 hinge question, 7 min",
     "1:10 build brief, 15 min",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Keeps the held shape in a plain variable and the drag function never sees it.", "A function cannot assign to a plain variable outside itself. <code>floor.held</code> is where all three functions can reach it. This is session 5's idea again."],
     ["Drags with <code>point=vec(0, 0, 0)</code> and the shape sinks.", "That is the hinge. The plane has to be at the height the shape's middle should have."],
     ["Forgets to set <code>floor.held</code> to None on mouseup and the shape follows the mouse forever.", "The drop has to end the drag. Print <code>floor.held</code> in <code>drag</code> and watch it never go back to None."],
     ["Grabs the floor and drags the whole ground away.", "The grab gate needs <code>or thing is floor</code>. Chunk 2's reveal says why."],
     ["Expects a hidden shape to be clickable, or to still count.", "Hidden shapes are not picked, which is why delete works, but they are still in the list. Counting has to check <code>visible</code>, and so does the stretch's Save."],
   ],
   "standards": ["NY-5.G.1", "NY-6.NS.6", "MP6"],
   "routing": "Chunk 1 can be cut to its reveal on the projector. Chunks 5 and 6 can be folded into the build, since the card has the menus. If time is short the build stops at step 2, which is the floor exit plus the card.",
 },
},

# =====================================================================
{
 "num": 9,
 "slug": "session09_your_project",
 "title": "Your project",
 "subtitle": "Pick one of three briefs, write the plan on one sheet, start from a skeleton that runs, and add one feature at a time",
 "new": ["a knob block of named numbers at the top", "a skeleton that runs before it does anything", "one feature, then run, then the next", "a plan sheet"],
 "reuse": "Everything: this session uses no new VPython and no new Python",
 "env_note": True,
 "reuse_note": "The three briefs are deliberately the three kinds of program the course has built: a model with a camera, a game, and an animation with a control. A student who cannot choose should take the one closest to the session they liked most. The plan sheet is not optional; a project with no plan sheet is a build with no expected column.",
 "opener": {
   "title": "Retrieval: pick any stamp",
   "minutes": 5,
   "body": "Talk this one out with a neighbour.",
   "questions": [
     {"q": "Pick any stamp on your ledger card and say, in one sentence each: what it lets a program do, and which session's build used it.",
      "a": "Any stamp works. Two examples: <code>keysdown()</code> lets a program move something for as long as a key is held, and the car in session 4 used it to drive. <code>scene.mouse.pick</code> lets a click find the object under the mouse, and the editor in session 8 used it to grab."},
     {"q": "Three functions in a program need to share one number. Where does it live?",
      "a": "On an object, as an attribute: <code>sun.factor</code>, <code>floor.held</code>, <code>player.score</code>. Any function that can see the object can read it and change it."},
   ],
 },
 "chunks": [
  {"title": "A knob block: the numbers you will want to change, named, at the top",
   "teach": "Every program has numbers that get tuned: how fast, how big, how strong. Give each one a name in capitals at the top of the file, and use the name everywhere below. Then tuning the program is changing one line, and the lines below say what they mean.</p><p>This program is session 3's bouncing ball with its three numbers lifted into a knob block. Nothing below the block has a bare number in it that you might want to change.",
   "code": code('''
from vpython import *

GRAVITY = 9.8
BOUNCE = 0.8
START_HEIGHT = 6

ground = box(pos=vec(0, -0.1, 0), size=vec(10, 0.2, 10), color=color.green)
ball = sphere(pos=vec(0, START_HEIGHT, 0), radius=0.5, color=color.yellow)
ball.vel = vec(0, 0, 0)
dt = 1 / 30
passes = 0
print("knobs: gravity", GRAVITY, " bounce", BOUNCE, " start height", START_HEIGHT)

while True:
    rate(30)
    passes = passes + 1

    ball.vel.y = ball.vel.y - GRAVITY * dt
    ball.pos = ball.pos + ball.vel * dt

    if ball.pos.y < ball.radius:
        ball.pos.y = ball.radius
        ball.vel.y = -ball.vel.y * BOUNCE
        print("bounce on pass", passes, "  going up at", round(ball.vel.y, 2))
'''),
   "run": "vpython",
   "frames": 100,
   "predict": "Which one line would you change to make the ball bounce higher each time, and which to make it fall faster? Would either change need a second line changed anywhere below?",
   "reveal": "Bounce higher: <code>BOUNCE = 0.8</code>, to a number closer to 1. Fall faster: <code>GRAVITY = 9.8</code>, to a bigger number. Neither needs any other line changed, because every line below uses the name, not the number.</p><p>The output box shows the first bounce on pass 32 at 8.36 per second and the second on pass 83. On a bigger START_HEIGHT the first bounce would come later and faster, and again nothing else would change."},

  {"title": "A skeleton that runs before it does anything",
   "teach": "The first version of a project has every object it will need, the knob block, the empty functions it will need, the bind lines, and the loop with nothing in it but <code>rate(30)</code>. It runs, it shows the scene, and it does nothing else. That is the first thing to make, because every mistake in it is a mistake you can see before any gate is written.</p><p>The objects go in a list called <code>things</code>, so that later a Reset and a count can reach all of them.",
   "code": code('''
from vpython import *

SPEED = 0.2

scene.caption = "Nothing works yet. That is on purpose."
ground = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 16), color=color.green)
things = []
things.append(box(pos=vec(0, 0.5, 0), color=color.orange))
things.append(sphere(pos=vec(3, 0.5, -2), radius=0.5, color=color.cyan))
things.append(cone(pos=vec(-3, 0, 2), axis=vec(0, 1.5, 0), radius=0.5, color=color.red))

def tapped(evt):
    print("a key was tapped:", evt.key, " (nothing wired to it yet)")

scene.bind("keydown", tapped)
print("skeleton is up:", len(things), "things on the ground, and the loop is running")

while True:
    rate(30)
'''),
   "run": "vpython",
   "frames": 4,
   "inject": [[2, "KEYDOWN", "left"]],
   "predict": "The loop body is only <code>rate(30)</code>. What does the program do when it runs, and what happens when a key is tapped?",
   "reveal": "It draws the ground and the three things, prints that the skeleton is up, and then runs the loop 30 times a second doing nothing, so the scene stays on screen and can be turned with the mouse.</p><p>A tap calls <code>tapped</code>, which prints the key and nothing else. The output box shows the left arrow arriving. The function is already bound, so wiring the key is a matter of adding gates to a function that already runs."},

  {"title": "One feature, then run, then the next",
   "teach": "Add one thing to the skeleton. Run it. Check it against what you expected. Only then add the next thing. A program with three new features and a bug has three places the bug could be; a program with one new feature and a bug has one.</p><p>This is the skeleton with its first feature: the left and right keys move the first thing. The second and third things are still waiting.",
   "code": code('''
from vpython import *

SPEED = 0.2

ground = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 16), color=color.green)
things = []
things.append(box(pos=vec(0, 0.5, 0), color=color.orange))
things.append(sphere(pos=vec(3, 0.5, -2), radius=0.5, color=color.cyan))
things.append(cone(pos=vec(-3, 0, 2), axis=vec(0, 1.5, 0), radius=0.5, color=color.red))
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if "right" in keys:
        things[0].pos.x = things[0].pos.x + SPEED
    if "left" in keys:
        things[0].pos.x = things[0].pos.x - SPEED

    if passes == 5:
        print("feature 1 check: box at", things[0].pos, "  ball still at", things[1].pos)
'''),
   "run": "vpython",
   "frames": 5,
   "inject": [[2, "HOLD", "right"], [3, "HOLD", "right"], [4, "HOLD", "right"]],
   "predict": "Before running: write down where the box should be after right is held for three passes, and where the ball should be. Then run and compare.",
   "reveal": "The box should be at x = 0.6, three passes of 0.2, and the ball should not have moved from <code>&lt;3, 0.5, -2&gt;</code>. The output box shows both. If the ball had moved, the gate would be touching the wrong thing, and with only one feature added, that is the only place to look.</p><p>Write the expected value down first, every time. A check you make up after seeing the output is not a check."},

  {"title": "The caption tells the player what to do",
   "teach": "The caption is the first thing someone else sees. It says what the keys and the mouse do, in the order they will want them. <code>\\n</code> inside a string starts a new line. Write the caption at the top of the file, before anything is built, because writing it is the fastest way to find out what the program is for.",
   "code": code('''
from vpython import *

scene.caption = "Arrow keys move the box.\\nClick a shape to change its colour.\\nPress r to put everything back.\\n"
ground = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 16), color=color.green)
print(scene.caption)
'''),
   "run": "vpython",
   "predict": "How many lines does the caption have under the scene, and what does <code>\\n</code> do inside the string?",
   "reveal": "Three lines. <code>\\n</code> is the new-line character: wherever it appears, the text goes on to the next line. The output box shows the same three lines in the terminal, because the print shows the string the way the caption shows it.</p><p>A caption that says three things is a plan for three features. If you cannot write the caption, the plan is not finished."},
 ],
 "sections": [
  {"title": "Three briefs. Pick one.",
   "html": '<div class="grid2">'
           '<div class="card"><h3>A. A model with a camera tour</h3><p>A scene with at least six shapes made by at least two functions of your own, from session 2. The keys 1, 2 and 3 move the camera to three views of it, using <code>scene.center</code> and <code>scene.forward</code> from session 4. One thing in the scene moves on its own: a spinning blade, a moon, a bouncing ball. A slider changes the speed of that thing.</p><p><b>Starter: card A below.</b></p></div>'
           '<div class="card"><h3>B. A game</h3><p>A player moved by keys. Things that fall, or chase, or have to be collected, from sessions 6 and 7. A score and lives under the scene, a game-over state, and r to restart. One number that makes it harder as the score goes up.</p><p><b>Starter: card B below.</b></p></div>'
           '<div class="card"><h3>C. An animation with controls</h3><p>Something that moves by itself, built from a list of objects turned or moved by one loop, from sessions 4 and 5. A slider for its speed, a checkbox that pauses it, and a button that puts it back to the start. A label on at least one moving thing.</p><p><b>Starter: card C below.</b></p></div>'
           '<div class="card"><h3>The plan sheet</h3><p>Four boxes on paper, filled in before the skeleton is typed:</p>'
           '<ol><li><b>What the viewer sees.</b> The objects, in a list, with their starting places.</li>'
           '<li><b>The controls.</b> Each key, click, slider or button, and what it does. This becomes the caption.</li>'
           '<li><b>What the program remembers.</b> Every number or thing that changes while it runs, and where it lives: a plain variable in the loop, or an attribute on which object.</li>'
           '<li><b>The knobs.</b> The numbers you will want to tune, with names.</li></ol></div>'
           '</div>'},
 ],
 "hinge": {"q": "A student's plan sheet says the controls are: arrows move the player, space fires, r restarts, a slider for speed, and a Delete mode tick box. The program has two bound functions, a slider function, a checkbox function, and a loop. Which of the five controls go in the loop with <code>keysdown</code>, which go in a bound function, and which numbers from the sheet have to live on an object rather than in a plain variable?",
           "a": "Arrows go in the loop with <code>keysdown</code>, because moving should continue while the key is held. Space and r go in a bound keydown function, because each should happen once per tap. The slider and the checkbox have their own bound functions.</p><p>Anything the slider or checkbox function changes has to live on an object: the speed and the delete flag. Anything that only the loop reads and changes can be a plain variable. The restart is the hard case: if r is in a bound function, every number it resets has to be on an object too; if r is read with <code>keysdown</code> in the loop instead, they can stay plain variables, which is what session 6 did."},
 "brief": {
   "title": "Build: the project, part one",
   "minutes": 40,
   "intro": "Fill in the plan sheet. Then type the skeleton from your sheet: the knob block, the caption, every object, the empty functions, the bind lines, and the loop with only <code>rate(30)</code>. Run it. Then add the features in the order they are on your sheet, running after each one and filling in the expected and got sheet as you go. Session 10 is for finishing, polishing, and showing it.",
   "steps": [
     "Plan sheet, on paper, all four boxes. Show it to the teacher before typing anything.",
     "Type the skeleton from the sheet. Run it. The scene should appear and nothing should happen.",
     "Add the first control from box 2. Write what you expect on the sheet below, run, write what you got.",
     "Add the next control. Same again. Stop when the session ends, wherever you are.",
     "At the end of the session, write on the plan sheet which features are done and which are next, so that session 10 starts from the sheet and not from memory.",
   ],
   "cards": [
     {"title": "Card A: three camera views on three keys",
      "teach": "Each number key sets where the camera looks and which way it faces. The views are written once at the top, as three pairs of vectors, so changing a view is changing one line.",
      "code": code('''
from vpython import *

VIEW_1 = [vec(0, 0, 0), vec(0, -0.5, -1)]
VIEW_2 = [vec(4, 0, 0), vec(-1, -0.3, 0)]
VIEW_3 = [vec(0, 2, 0), vec(0, -1, -0.2)]

scene.caption = "Press 1, 2 or 3 to change the view."
ground = box(pos=vec(0, -0.1, 0), size=vec(16, 0.2, 16), color=color.green)
tower = cylinder(pos=vec(4, 0, 0), axis=vec(0, 3, 0), radius=0.5, color=color.white)
scene.autoscale = False
scene.range = 8

def view(evt):
    if evt.key == "1":
        scene.center = VIEW_1[0]
        scene.forward = VIEW_1[1]
    if evt.key == "2":
        scene.center = VIEW_2[0]
        scene.forward = VIEW_2[1]
    if evt.key == "3":
        scene.center = VIEW_3[0]
        scene.forward = VIEW_3[1]
    print("key", evt.key, "  camera looks at", scene.center, "  facing", scene.forward)

scene.bind("keydown", view)

while True:
    rate(30)
'''),
      "run": "vpython",
      "frames": 6,
      "inject": [[1, "KEYDOWN", "2"], [3, "KEYDOWN", "3"], [5, "KEYDOWN", "x"]],
      "predict": "2 is pressed, then 3, then x. After the x, where does the camera look? Why does the print line run for x at all?",
      "reveal": "After x the camera still looks at <code>&lt;0, 2, 0&gt;</code>, facing <code>&lt;0, -1, -0.2&gt;</code>, the third view, because none of the three gates named x and nothing changed. The print line runs for every key, because it is after the gates and not inside any of them, so the output box has three lines.</p><p>View 2 looks at the tower from the side, and view 3 looks straight down at the middle of the ground. The number keys arrive as the strings <code>\"1\"</code>, <code>\"2\"</code> and <code>\"3\"</code>."},
     {"title": "Card B: blocks that fall, and a player that dodges",
      "teach": "A game that is the catch game turned around: the blocks are the danger and the player has to not be under them. The hit gate is the catch gate from session 6. A hit costs a life and sends the block back to the top. The blocks are a list, each with its own velocity, so one loop serves all of them. For this test run the player starts directly under the lowest block, so the first hit is certain; in the game the player starts in the middle and dodges.",
      "code": code('''
from vpython import *
from random import randint

FALL_SPEED = 4
REACH = 1.0

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 6), color=color.green)
player = box(pos=vec(0, 0.5, 0), size=vec(1, 1, 1), color=color.blue)
player.lives = 3
blocks = []
for i in range(3):
    b = box(pos=vec(randint(-5, 5), 8 + i * 4, 0), color=color.red)
    b.vel = vec(0, -FALL_SPEED, 0)
    blocks.append(b)
player.pos.x = blocks[0].pos.x
dt = 1 / 30
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if "right" in keys:
        player.pos.x = player.pos.x + 0.3
    if "left" in keys:
        player.pos.x = player.pos.x - 0.3

    for b in blocks:
        b.pos = b.pos + b.vel * dt
        gap = abs(b.pos.x - player.pos.x)
        if b.pos.y < 1 and gap < REACH:
            player.lives = player.lives - 1
            print("hit on pass", passes, "  lives left", player.lives)
            b.pos = vec(randint(-5, 5), 12, 0)
        if b.pos.y < -0.5:
            b.pos = vec(randint(-5, 5), 12, 0)
'''),
      "run": "vpython",
      "frames": 60,
      "predict": "Three blocks start at heights 8, 12 and 16, all falling at 4 per second, from random x positions, and the player is under the lowest one. On about which pass is the first hit? Will the second block hit too?",
      "reveal": "Pass 53. The lowest block reaches height 1 after falling 7 units, which at 4 per second is 1.75 seconds, and pass 53 is the first pass past that. Lives go from 3 to 2.</p><p>Whether the second block hits depends on where <code>randint</code> put it, and this run stops on pass 60 before it arrives. If its x is more than 1 from the player's x, the gap gate is False, the block falls past, and the second gate sends it back to the top with no print. A block that misses is not a bug; it is the game."},
     {"title": "Card C: a windmill farm with a wind slider and a pause box",
      "teach": "Every blade is in a list, and one loop turns them all by the wind speed, which lives on the ground as <code>ground.wind</code> so the slider can change it. The checkbox sets <code>ground.paused</code>, and the loop turns nothing while it is True.",
      "code": code('''
from vpython import *

WIND = 3

ground = box(pos=vec(0, -0.1, 0), size=vec(20, 0.2, 20), color=color.green)
ground.wind = WIND
ground.paused = False
blades = []
for x in [-6, 0, 6]:
    cylinder(pos=vec(x, 0, 0), axis=vec(0, 3, 0), radius=0.2, color=color.white)
    blade = box(pos=vec(x, 3, 0.3), size=vec(3, 0.3, 0.1), color=color.red)
    blades.append(blade)

def set_wind(s):
    ground.wind = s.value
    print("wind is now", ground.wind)

def set_pause(c):
    ground.paused = c.checked
    print("paused is now", ground.paused)

scene.append_to_caption("Wind: ")
slider(min=0, max=10, value=WIND, step=1, bind=set_wind)
scene.append_to_caption("   ")
checkbox(text="Pause", bind=set_pause)
turned = 0
passes = 0

while True:
    rate(30)
    passes = passes + 1

    if ground.paused == False:
        for blade in blades:
            blade.rotate(angle=radians(ground.wind), axis=vec(0, 0, 1))
        turned = turned + ground.wind

    if passes in [30, 60, 90]:
        print("pass", passes, "  each blade has turned", turned, "degrees in total")
'''),
      "run": "vpython",
      "frames": 90,
      "inject": [[31, "WIDGET", "set_wind", 6], [61, "WIDGET", "set_pause", True]],
      "predict": "The wind slider is set to 6 right after pass 30 and the pause box is ticked right after pass 60. How many degrees has each blade turned by pass 30, by 60, and by 90?",
      "reveal": "90 degrees by pass 30: 3 per pass. 270 by pass 60: 180 more, at 6 per pass. Still 270 by pass 90, because the blades were paused after pass 60 and the loop turned nothing after that.</p><p>The gate <code>ground.paused == False</code> is around both the rotate and the counter, so pausing stops both. Untick the box and the blades carry on from where they stopped."},
   ],
   "expected_got": [
     ["The skeleton runs and shows every object before any feature is added", ""],
     ["Feature 1 does what the plan sheet says, and nothing else moves", ""],
     ["Feature 2 does what the plan sheet says, and feature 1 still works", ""],
     ["The caption matches the controls that actually work", ""],
     ["The plan sheet says what is done and what is next", ""],
   ],
 },
 "exits": {
   "floor": "The plan sheet filled in, and the skeleton running with every object in place and a caption that names the planned controls.",
   "middle": "The skeleton plus two working controls, checked against the sheet.",
   "stretch": "Everything on the plan sheet working, so session 10 is polish and the demo only.",
 },
 "ledger": "Stamp 9: knobs in capitals at the top, the skeleton runs before any feature, one feature then run then the next, write the expected value before running, the caption is the plan, the plan sheet: what is seen, the controls, what is remembered and where, the knobs.",
 "teacher": {
   "timing": [
     "0:00 retrieval opener, 5 min",
     "0:05 chunks 1 and 2, knobs and the skeleton, 15 min",
     "0:20 chunks 3 and 4, one feature at a time and the caption, 10 min",
     "0:30 the three briefs and the plan sheet, 10 min",
     "0:40 hinge question, 5 min",
     "0:45 build brief, 40 min (plan sheets checked in the first ten)",
     "1:25 exits, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Starts typing the whole program from the brief, with no sheet and no skeleton.", "Stop them at the first error and ask which of the five things they typed caused it. The skeleton exists so that the answer is always one thing."],
     ["Picks brief B and plans six kinds of enemy.", "One kind of falling thing, in a list. Card B is brief B at the floor; everything else is a feature to add after it works."],
     ["Puts the speed in a plain variable and the slider never changes it.", "Session 5's chunk 5. The slider's function needs the number on an object."],
     ["Cannot write the caption and keeps changing the plan.", "That is the caption doing its job. Write the three sentences first; the sentences are the features."],
     ["Adds three features between runs and then has a bug.", "Comment out two of them, run, and find out which one. Then say why the course says one at a time."],
   ],
   "standards": ["MP1", "5W2", "MP6"],
   "routing": "Chunk 1 can be cut if the room already names its knobs. The plan sheet and the skeleton cannot. If a student is far behind, their project is card A, B or C as given, with one feature of their own added, and that is a finished project.",
 },
},

# =====================================================================
{
 "num": 10,
 "slug": "session10_finish_polish_and_show",
 "title": "Finish, polish, and show",
 "subtitle": "A start screen, a Reset that puts everything back, three lines of polish, a partner's test, and a two-minute demo",
 "new": ["a start state and a space key", "a home attribute for Reset", "scene.background and scene.title", "a partner test", "the demo script"],
 "reuse": "Everything",
 "env_note": True,
 "reuse_note": "The demo is a report on a topic, and the topic is the student's own program. Two minutes, four sentences, one key and one click shown. The partner test in the second section is what finds the bug the author cannot see, so it comes before the polish, not after.",
 "opener": {
   "title": "Retrieval: the plan sheet",
   "minutes": 5,
   "body": "Open your plan sheet from session 9.",
   "questions": [
     {"q": "Read box 3 of your sheet, what the program remembers. For each thing on it, say where it lives in your program now: a plain variable in the loop, or an attribute on which object. Is anything on the sheet that the program does not keep yet?",
      "a": "Any honest answer is right. Something on the sheet that the program does not keep yet is the first thing to add today, before any polish."},
     {"q": "Read box 2, the controls. Which of them work now, and which does the caption promise that do not work yet?",
      "a": "A control the caption promises and the program does not do is a bug a visitor will find in the first ten seconds. Either make it work or take it out of the caption, and do that first."},
   ],
 },
 "chunks": [
  {"title": "A start screen: a title, and a key that begins",
   "teach": "A program that starts moving the moment it opens gives the viewer no time to read the caption. Keep a <code>state</code> that starts as <code>\"start\"</code>, show a title label, and gate everything that moves on <code>state == \"play\"</code>. The space key, which arrives as the string <code>\" \"</code>, changes the state and hides the title. This is session 6's state name with one more value.",
   "code": code('''
from vpython import *

scene.caption = "Press space to start. Arrow keys move the ball."
ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
ball = sphere(pos=vec(0, 0.5, 0), radius=0.5, color=color.yellow)
title = label(pos=vec(0, 3, 0), text="BALL RUN", height=30, box=False)
ground.state = "start"

def begin(evt):
    if evt.key == " " and ground.state == "start":
        ground.state = "play"
        title.visible = False
        print("space pressed: state is now", ground.state)

scene.bind("keydown", begin)
passes = 0

while True:
    rate(30)
    passes = passes + 1
    keys = keysdown()

    if ground.state == "play" and "right" in keys:
        ball.pos.x = ball.pos.x + 0.2

    if passes in [3, 6]:
        print("pass", passes, "  state", ground.state, "  ball at", ball.pos)
'''),
   "run": "vpython",
   "frames": 6,
   "inject": [[2, "HOLD", "right"], [4, "KEYDOWN", " "], [5, "HOLD", "right"], [6, "HOLD", "right"]],
   "predict": "The right arrow is held on pass 2, before space is pressed, and again on passes 5 and 6, after it. Does the ball move on pass 2? Where is it on pass 6?",
   "reveal": "No. On pass 2 the state is still start, so the gate <code>ground.state == \"play\" and \"right\" in keys</code> is False and the ball stays at x = 0; the pass 3 line shows that. After space on pass 4, the state is play, and the two held passes move the ball to x = 0.4 by pass 6.</p><p>The state lives on the ground, because the bound function and the loop both need it. The space key's name is a single space character, which is easy to miss when reading the program."},

  {"title": "Reset puts everything back, because every thing knows its home",
   "teach": "A Reset that works has to know where everything started. Give each moving thing a <code>home</code> attribute holding a copy of its starting pos, made with <code>vec(thing.pos.x, thing.pos.y, thing.pos.z)</code>. The Reset function loops over the list and puts each thing back at its home. Copying matters: <code>thing.home = thing.pos</code> would make <code>home</code> the same vector as the pos, and it would move with the thing.",
   "code": code('''
from vpython import *

ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green)
things = []
things.append(box(pos=vec(0, 0.5, 0), color=color.orange))
things.append(sphere(pos=vec(3, 0.5, -2), radius=0.5, color=color.cyan))
for thing in things:
    thing.home = vec(thing.pos.x, thing.pos.y, thing.pos.z)

def reset(b):
    for thing in things:
        thing.pos = thing.home
        thing.visible = True
    print("reset: box at", things[0].pos, " ball at", things[1].pos)

button(text="Reset", bind=reset)
passes = 0

while True:
    rate(30)
    passes = passes + 1
    things[0].pos.x = things[0].pos.x + 0.5
    things[1].pos.z = things[1].pos.z + 0.5

    if passes == 4:
        print("pass 4: box at", things[0].pos, " ball at", things[1].pos, " box home is still", things[0].home)
'''),
   "run": "vpython",
   "frames": 8,
   "inject": [[6, "WIDGET", "reset"]],
   "predict": "The box and the ball move 0.5 on every pass. Reset is clicked on pass 6. Where are they after the click, and why is the box's <code>home</code> on pass 4 still <code>&lt;0, 0.5, 0&gt;</code> after four moves?",
   "reveal": "After the click the box is back at <code>&lt;0, 0.5, 0&gt;</code> and the ball at <code>&lt;3, 0.5, -2&gt;</code>, their starting places. The loop then moves them again from there.</p><p>The home is unchanged on pass 4 because it is a copy: a new vector built from the three numbers the pos had at the start. The moves change the pos and never touch the copy. Written as <code>thing.home = thing.pos</code> with no copy, the home would be the pos itself, and Reset would put each thing back exactly where it already was."},

  {"title": "Three lines of polish",
   "teach": "<code>scene.background</code> is the colour behind everything. <code>scene.title</code> is a heading above the scene. Opacity on the ground lets a viewer see a thing that is behind it from a low camera. None of these change what the program does; all of them change what the viewer sees first.",
   "code": code('''
from vpython import *

scene.title = "Ball Run, by Jonathan\\n"
scene.background = vec(0.1, 0.1, 0.25)
ground = box(pos=vec(0, -0.1, 0), size=vec(12, 0.2, 12), color=color.green, opacity=0.8)
ball = sphere(pos=vec(0, 0.5, 0), radius=0.5, color=color.yellow)
print("title:", scene.title)
print("background:", scene.background, "  ground opacity:", ground.opacity)
'''),
   "run": "vpython",
   "predict": "What colour is <code>vec(0.1, 0.1, 0.25)</code>: dark or light, and closer to blue or to red? Where does the title appear?",
   "reveal": "Dark, because all three numbers are small, and closer to blue, because the third number is the biggest of the three. A night sky. The title appears above the scene, in the tab, with its <code>\\n</code> putting a blank line between it and the scene.</p><p>Keep the polish to lines like these. A feature added in the last ten minutes is where the demo breaks."},
 ],
 "sections": [
  {"title": "The partner test, 10 minutes",
   "html": '<p>Swap seats with a neighbour. Do not explain your program. Your partner reads the caption, and only the caption, and tries every control it names. For each one they write a line on your expected-and-got sheet: what the caption said, what happened. Then swap back.</p>'
           '<p>Three things a partner finds that an author does not: a control the caption names that does nothing, a key that does something the caption does not say, and a thing that can go wrong when the controls are used in an order the author never tried. Fix the first kind first.</p>'},
  {"title": "The demo: two minutes, four sentences",
   "html": '<p>Each demo is two minutes. Say these four things, in this order, then show one key and one click:</p>'
           '<ol><li><b>What it is.</b> One sentence: a game where you dodge falling blocks; a solar system with a moon; an editor for building a village.</li>'
           '<li><b>What it does when you use it.</b> Name the controls as you show them: press space, hold right, click a block.</li>'
           '<li><b>One thing that was hard, and how you fixed it.</b> The bug, the line, the fix.</li>'
           '<li><b>What you would add next.</b> One feature, from your plan sheet.</li></ol>'
           '<p>Before your turn: the tab is open, the scene has been clicked so the keys work, and the program has been restarted so it is at its start screen. During your turn, if something breaks, say what you think it is and move on. A demo with a bug and a sentence about the bug is a complete demo.</p>'},
  {"title": "Demo order and what the room does",
   "html": '<p>The order is the order of the plan sheets on the desk, so nobody is first because of where they sit. While one person shows, everyone else writes one line on a slip: one thing the program did that they want to try in their own. The slips go to the author at the end.</p>'
           '<p>The teacher keeps the time and says nothing about the program until all demos are done.</p>'},
 ],
 "hinge": {"q": "From session 1: during a demo, a visitor presses the left arrow and nothing happens. Name the two things that could be true, and say how to check each one in five seconds.",
           "a": "One: the browser tab does not have the focus, so the key went to the editor or somewhere else. Check by clicking once inside the 3D scene and pressing the key again.</p><p>Two: the program has stopped. Check the terminal: if the prompt is back, the loop at the bottom is not running, because the program ended or an error stopped it, and the traceback above the prompt says which line. Run it again."},
 "brief": {
   "title": "Build: finish, test, polish, show",
   "minutes": 30,
   "intro": "Finish the features on your plan sheet, in the order the sheet says, one at a time. Then the start screen and the Reset from chunks 1 and 2, if your project needs them. Then the partner test. Then the three lines of polish. Then the demo.",
   "steps": [
     "Make every control the caption promises work, or take it out of the caption.",
     "Add the start state and the space key if anything moves on its own, so the viewer can read the caption first.",
     "Add the Reset button with a <code>home</code> on every moving thing, or an r key if your numbers live in the loop.",
     "Partner test. Fix what the partner found, first kind first.",
     "Title, background, opacity. Nothing else new.",
     "Restart the program, click the scene, and leave it at the start screen for the demo.",
   ],
   "expected_got": [
     ["Every control named in the caption does what the caption says", ""],
     ["Nothing moves before space is pressed", ""],
     ["Reset puts every moving thing back where it started", ""],
     ["A partner found the controls from the caption alone", ""],
     ["The program is at its start screen when the demo begins", ""],
   ],
 },
 "exits": {
   "floor": "The project as it was at the end of session 9, with a caption that only promises what works, and a two-minute demo of it.",
   "middle": "The project with a start screen, a Reset, a partner test done, and the demo.",
   "stretch": "The project with every feature on the plan sheet, a visitor's slip of ideas read, and one of those ideas added.",
 },
 "ledger": "Stamp 10: a <code>state</code> that starts as start, the space key is <code>\" \"</code>, a <code>home</code> copy on every moving thing (<code>vec(p.x, p.y, p.z)</code>), Reset loops over the list, <code>scene.title</code>, <code>scene.background</code>, the partner test from the caption alone, the demo: what it is, what it does, what was hard, what is next.",
 "teacher": {
   "timing": [
     "0:00 plan sheet opener, 5 min",
     "0:05 chunks 1 to 3, start screen, Reset, polish, 15 min",
     "0:20 hinge question, 5 min",
     "0:25 build brief, finishing and the partner test, 30 min",
     "0:55 demos, 30 min (two minutes each, the teacher keeps time)",
     "1:25 slips to authors, ledger stamp, 5 min",
   ],
   "misconceptions": [
     ["Adds a new feature during the polish step and the demo breaks.", "Polish is three lines that change nothing the program does. A feature is not polish. If it is not working ten minutes before demos, comment it out and take it out of the caption."],
     ["Writes <code>thing.home = thing.pos</code> and Reset does nothing.", "The home is the same vector as the pos, so it moves with the thing. Chunk 2's reveal. Build the copy from the three numbers."],
     ["Skips the partner test because the program works.", "It works for the author, who knows what not to press. The partner presses it."],
     ["Starts the demo with the tab unfocused and says the keys are broken.", "The hinge. Click the scene first. Make it the first thing every demo does."],
     ["Tells the room every line of the program.", "Four sentences, one key, one click. The slips are for the rest."],
   ],
   "standards": ["5SL4", "MP1", "MP6"],
   "routing": "If the room has more than twelve students, demos are ninety seconds and the build is 25 minutes. Chunk 3 can be cut to one line on the projector. The partner test cannot be cut; it is the only check that is not the author's own.",
 },
},
]
