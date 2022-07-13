# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE=(0,0,255)

# game settings

TILESIZE = 30
DIM = 20
GWIDTH = DIM
GHEIGHT = DIM

WIDTH = GWIDTH * TILESIZE # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = GHEIGHT * TILESIZE  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

BLANK = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

RULES = {
    BLANK : [[BLANK, UP],
             [BLANK, RIGHT],
             [BLANK, DOWN],
             [BLANK, LEFT]
             ],
    UP : [
        [LEFT, DOWN, RIGHT],
        [LEFT, DOWN, UP],
        [BLANK, DOWN],
        [RIGHT, DOWN, UP]
    ],
    RIGHT : [
        [DOWN, LEFT, RIGHT],
        [DOWN, LEFT, UP],
        [LEFT, UP, RIGHT],
        [BLANK, LEFT]
    ],
    LEFT :  [
        [RIGHT, DOWN, LEFT],
        [BLANK, RIGHT],
        [UP, RIGHT, LEFT],
        [RIGHT, DOWN, UP]
    ],
    DOWN : [
        [BLANK, UP],
        [LEFT, UP, DOWN],
        [UP, LEFT, RIGHT],
        [RIGHT, UP, DOWN]
    ],
}

MAPPED_EDGES = {
    BLANK : [0, 0, 0, 0],
    UP : [1, 1, 0, 1],
    RIGHT : [1, 1, 1, 0],
    LEFT : [1, 0, 1, 1],
    DOWN : [0, 1, 1, 1]
}


NORTH=0
SOUTH=1
EAST=2
WEST=3