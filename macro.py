from dataclasses import dataclass

WIDTH, HEIGHT = 900, 900
EMPTY = 0
WALL = 1
HEAD = 2
BODY = 3
TAIL = 4
RED_APPLE = 5
GREEN_APPLE = 6
SQUARE_SIZE = HEIGHT / 11
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

opposite = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

@dataclass
class square:
    x: float
    y: float
    id: int
    dir: int
