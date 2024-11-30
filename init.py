import macro
import random
import pygame.draw as pyd


def draw_grid_of_squares(board: list, square_size: float, win):
    for row in board:
        for el in row:
            pyd.rect(win, "white", (el.x, el.y, square_size, square_size), 1)


def place_food(board: list, item: int):
    size = len(board) - 1
    while True:
        x = random.randint(0, size)
        y = random.randint(0, size)
        if board[x][y].id == 0:
            board[x][y].id = item
            break


def add_tail(board: list, x: int, y: int,
             tail: bool = True) -> tuple[int, int]:
    if board[x][y + 1].id == 0:
        board[x][y + 1].id = macro.TAIL if tail else macro.BODY
        board[x][y + 1].dir = macro.LEFT
        return x, y + 1
    elif board[x][y - 1].id == 0:
        board[x][y - 1].id = macro.TAIL if tail else macro.BODY
        board[x][y - 1].dir = macro.RIGHT
        return x, y - 1
    elif board[x + 1][y].id == 0:
        board[x + 1][y].id = macro.TAIL if tail else macro.BODY
        board[x + 1][y].dir = macro.UP
        return x + 1, y
    elif board[x - 1][y].id == 0:
        board[x - 1][y].id = macro.TAIL if tail else macro.BODY
        board[x - 1][y].dir = macro.DOWN
        return x - 1, y


def init_snake(board: list):
    size = len(board) - 1
    while True:
        x = random.randint(0, size)
        y = random.randint(0, size)
        if board[x][y].id == 0:
            board[x][y].id = macro.HEAD
            break
    x, y = add_tail(board, x, y, False)
    add_tail(board, x, y)


def init_board(size: int, square_size: float) -> list:
    board = [
        [
            macro.square(x * square_size, y * square_size, 0, -1)
            for x in range(size)
        ]
        for y in range(size)
        ]
    macro.length = 3
    init_walls(board)
    init_snake(board)
    place_food(board, macro.RED_APPLE)
    place_food(board, macro.GREEN_APPLE)
    place_food(board, macro.GREEN_APPLE)

    return board


def init_walls(board: list):
    end = len(board[0]) - 1
    for i, a in enumerate(board):
        if i == 0 or i == end:
            for el in board[i]:
                el.id = 1
        else:
            a[0].id = 1
            a[end].id = 1
