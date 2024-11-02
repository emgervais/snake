import pygame
import random
from dataclasses import dataclass

global snake_direction
# Initialize Pygame
pygame.init()   
# Set up display
WIDTH, HEIGHT = 900, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")    
# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
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

@dataclass
class square:
    x: float
    y: float
    id: int
    dir: int

def draw_grid_of_squares(board):
    for row in board:
        for el in row:
            pygame.draw.rect(win, WHITE, (el.x, el.y, SQUARE_SIZE, SQUARE_SIZE), 1)

def place_food(board, item):
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y].id == 0:
            board[x][y].id = item
            break

def add_tail(board, x, y, tail=True):
    if board[x][y + 1].id == 0:
        board[x][y + 1].id = TAIL if tail else BODY
        board[x][y + 1].dir = LEFT
        return x, y + 1
    elif board[x][y - 1].id == 0:
        board[x][y - 1].id = TAIL if tail else BODY
        board[x][y + 1].dir = RIGHT
        return x, y - 1
    elif board[x + 1][y].id == 0:
        board[x + 1][y].id = TAIL if tail else BODY
        board[x][y + 1].dir = UP
        return x + 1, y
    elif board[x - 1][y].id == 0:
        board[x - 1][y].id = TAIL if tail else BODY
        board[x][y + 1].dir = DOWN
        return x - 1, y

def init_snake(board):
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y].id == 0:
            board[x][y].id = HEAD
            break
    x, y = add_tail(board, x ,y, False)
    add_tail(board, x ,y)
    

def render(board):
    for r in board:
        for el in r:
            if(el.id == EMPTY):
                continue
            elif el.id == WALL:
                win.fill("grey", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            elif el.id == RED_APPLE:
                win.fill("purple", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            elif el.id == GREEN_APPLE:
                win.fill("green", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            elif el.id == HEAD:
                win.fill("yellow", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            elif el.id == BODY:
                win.fill("orange", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
            elif el.id == TAIL:
                win.fill("red", (el.x + 5, el.y + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))

def init_board(board):
    init_walls(board)
    init_snake(board)
    place_food(board, RED_APPLE)
    place_food(board, GREEN_APPLE)
    place_food(board, GREEN_APPLE)

def init_walls(board):
    for i, a in enumerate(board):
        if i == 0 or i == 10:
            for el in board[i]:
                el.id = 1
        else:
            a[0].id = 1
            a[10].id = 1

def find_square_by_id(board, target_id):
    for ri, row in enumerate(board):
        for si, square in enumerate(row):
            if square.id == target_id:
                return ri, si, square

def find_square_by_dir(board, x, y, dir):
    if dir == RIGHT:
        return board[x][y + 1]
    elif dir == LEFT:
        return board[x][y - 1]
    elif dir == UP:
        return board[x - 1][y]
    elif dir == DOWN:
        return board[x + 1][y]

def move_snake(board, dir):
    head_x, head_y, head = find_square_by_id(board, HEAD)
    tail_x, tail_y, tail = find_square_by_id(board, TAIL)
    head.dir = dir
    head.id = BODY
    s = find_square_by_dir(board, head_x, head_y, dir)
    id = s.id
    if id == GREEN_APPLE or id == RED_APPLE:
        print("bigger")
        return True
    elif id == BODY or id == TAIL or id == WALL:
        print("dead")
        return False
    s.id = HEAD
    s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
    tail.dir = -1
    tail.id = EMPTY
    s.id = TAIL
    return True

def main():
    board = [[square(x * SQUARE_SIZE, y * SQUARE_SIZE, 0, -1) for x in range(11)] for y in range(11)]
    running = True
    init_board(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    running = move_snake(board, UP)
                elif event.key == pygame.K_DOWN:
                    running = move_snake(board, DOWN)
                elif event.key == pygame.K_LEFT:
                    running = move_snake(board, LEFT)
                elif event.key == pygame.K_RIGHT:
                    running = move_snake(board, RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                # render(board)
        win.fill('black')
        draw_grid_of_squares(board)
        render(board)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()