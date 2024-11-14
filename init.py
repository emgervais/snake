import macro
import pygame as py
import random

def draw_grid_of_squares(board: list, win):
    for row in board:
        for el in row:
            py.draw.rect(win, "white", (el.x, el.y, macro.SQUARE_SIZE, macro.SQUARE_SIZE), 1)

def place_food(board: list, item: int):
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y].id == 0:
            board[x][y].id = item
            break

def add_tail(board: list, x: int, y: int, tail: bool=True) -> tuple[int, int]:
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
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y].id == 0:
            board[x][y].id = macro.HEAD
            break
    x, y = add_tail(board, x ,y, False)
    add_tail(board, x ,y)

def init_board() -> list:
    board = [[macro.square(x * macro.SQUARE_SIZE, y * macro.SQUARE_SIZE, 0, -1) for x in range(11)] for y in range(11)]
    init_walls(board)
    init_snake(board)
    place_food(board, macro.RED_APPLE)
    place_food(board, macro.GREEN_APPLE)
    place_food(board, macro.GREEN_APPLE)
    return board

def init_walls(board: list):
    for i, a in enumerate(board):
        if i == 0 or i == 10:
            for el in board[i]:
                el.id = 1
        else:
            a[0].id = 1
            a[10].id = 1