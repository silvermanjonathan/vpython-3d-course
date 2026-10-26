"""Standards registry for the VPython course: every code the site prints.

Each entry was resolved through the Learning Commons Knowledge Graph connector
(CASE Network) on RESOLVED_ON and is printed on the pages with its CASE identifier.
Nothing here was written from memory.
"""

RESOLVED_ON = '2026-10-05 (NY-7.G.4 added 2026-10-26)'
CONNECTOR = 'Learning Commons Knowledge Graph (CASE Network)'

NY_MATH = 'NY Next Generation Mathematics Learning Standards'
NY_ELA = 'NY Next Generation ELA Learning Standards'
MP = 'Standards for Mathematical Practice'

STANDARDS = {
    'NY-4.MD.5': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '4',
        'statement': (
            'Recognize angles as geometric shapes that are formed wherever two rays '
            'share a common endpoint, and understand concepts of angle measurement.'
        ),
        'lcs': [], 'uuid': '70d727aa-d7cc-11e8-824f-0242ac160002',
    },
    'NY-5.G.1': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '5',
        'statement': (
            'Use a pair of perpendicular number lines, called axes, to define a '
            'coordinate system, with the intersection of the lines (the origin) '
            'arranged to coincide with the 0 on each line and a given point in the '
            'plane located by using an ordered pair of numbers, called its '
            'coordinates. Understand that the first number indicates how far to '
            'travel from the origin in the direction of one axis, and the second '
            'number indicates how far to travel in the direction of the second '
            'axis, with the convention that the names of the two axes and the '
            'coordinates correspond.'
        ),
        'lcs': [], 'uuid': '70d7a534-d7cc-11e8-824f-0242ac160002',
    },
    'NY-5.G.2': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '5',
        'statement': (
            'Represent real world and mathematical problems by graphing points in '
            'the first quadrant of the coordinate plane, and interpret coordinate '
            'values of points in the context of the situation.'
        ),
        'lcs': [], 'uuid': '70d7a8cc-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.EE.2': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': 'Write, read, and evaluate expressions in which letters stand for numbers.',
        'lcs': [], 'uuid': '70d83bda-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.EE.5': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': (
            'Understand solving an equation or inequality as a process of answering '
            'a question: which values from a specified set, if any, make the '
            'equation or inequality true? Use substitution to determine whether a '
            'given number in a specified set makes an equation or inequality true.'
        ),
        'lcs': [], 'uuid': '70d84845-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.EE.9': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': (
            'Use variables to represent two quantities in a real-world problem that '
            'change in relationship to one another. Given a verbal context and an '
            'equation, identify the dependent variable, in terms of the other '
            'quantity, thought of as the independent variable. Analyze the '
            'relationship between the dependent and independent variables using '
            'graphs and tables, and relate these to the equation.'
        ),
        'lcs': [], 'uuid': '70d853df-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.NS.5': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': (
            'Understand that positive and negative numbers are used together to '
            'describe quantities having opposite directions or values. Use positive '
            'and negative numbers to represent quantities in real-world contexts, '
            'explaining the meaning of 0 in each situation.'
        ),
        'lcs': [], 'uuid': '70d817ee-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.NS.6': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': (
            'Understand a rational number as a point on the number line. Use '
            'number lines and coordinate axes to represent points on a number line '
            'and in the coordinate plane with negative number coordinates.'
        ),
        'lcs': [], 'uuid': '70d81cfb-d7cc-11e8-824f-0242ac160002',
    },
    'NY-6.NS.8': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '6',
        'statement': (
            'Solve real-world and mathematical problems by graphing points on a '
            'coordinate plane. Include use of coordinates and absolute value to find '
            'distances between points with the same first coordinate or the same '
            'second coordinate.'
        ),
        'lcs': [], 'uuid': '70d83247-d7cc-11e8-824f-0242ac160002',
    },
    'NY-7.G.4': {
        'jurisdiction': 'New York', 'framework': NY_MATH, 'subject': 'Mathematics',
        'grades': '7',
        'statement': (
            'Apply the formulas for the area and circumference of a circle to '
            'solve problems.'
        ),
        'lcs': ['Find the circumference of a circle to solve problems, including by '
                'using the formula for circumference of a circle'],
        'uuid': '70d89048-d7cc-11e8-824f-0242ac160002',
    },
    'MP1': {
        'jurisdiction': 'Multi-State', 'framework': MP, 'subject': 'Mathematics',
        'grades': 'K-12',
        'statement': 'Make sense of problems and persevere in solving them.',
        'lcs': [], 'uuid': '6b9ca36a-d7cc-11e8-824f-0242ac160002',
    },
    'MP6': {
        'jurisdiction': 'Multi-State', 'framework': MP, 'subject': 'Mathematics',
        'grades': 'K-12',
        'statement': 'Attend to precision.',
        'lcs': [], 'uuid': '6ba033ff-d7cc-11e8-824f-0242ac160002',
    },
    'MP7': {
        'jurisdiction': 'Multi-State', 'framework': MP, 'subject': 'Mathematics',
        'grades': 'K-12',
        'statement': 'Look for and make use of structure.',
        'lcs': [], 'uuid': '6ba09141-d7cc-11e8-824f-0242ac160002',
    },
    'MP8': {
        'jurisdiction': 'Multi-State', 'framework': MP, 'subject': 'Mathematics',
        'grades': 'K-12',
        'statement': 'Look for and express regularity in repeated reasoning.',
        'lcs': [], 'uuid': '6ba0d653-d7cc-11e8-824f-0242ac160002',
    },
    '5SL4': {
        'jurisdiction': 'New York', 'framework': NY_ELA, 'subject': 'English Language Arts',
        'grades': '5',
        'statement': (
            'Report on a topic or text, sequencing ideas logically and using '
            'appropriate facts and relevant, descriptive details to support central '
            'ideas or themes; speak clearly at an understandable pace and volume '
            'appropriate for audience.'
        ),
        'lcs': [], 'uuid': '70df5a51-d7cc-11e8-824f-0242ac160002',
    },
    '5W2': {
        'jurisdiction': 'New York', 'framework': NY_ELA, 'subject': 'English Language Arts',
        'grades': '5',
        'statement': (
            'Write informative/explanatory texts to explore a topic and convey '
            'ideas and information relevant to the subject.'
        ),
        'lcs': [], 'uuid': '70ded018-d7cc-11e8-824f-0242ac160002',
    },
}
