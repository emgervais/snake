import pygame
import random

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
TAIL = 3
RED_APPLE = 4
GREEN_APPLE = 5

def draw_grid_of_squares():
    start_x, start_y = 0,0
    square_size =  HEIGHT / 11

    for row in range(11):
        for col in range(11):
            x = start_x + col * square_size
            y = start_y + row * square_size
            pygame.draw.rect(win, WHITE, (x, y, square_size, square_size), 1)

def place_food(board, item):
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y] == 0:
            board[x][y] = item
            break

def init_snake(board):
    while True:
        x = random.randint(0, 11 - 1)
        y = random.randint(0, 11 - 1)
        if board[x][y] == 0:
            board[x][y] = 2
            break
def render(board):
    for r in board:
        for c in r:
            if(c == EMPTY):
                continue
            # elif c == WALL:
            # elif c ==

# def move(board):

def init_board(board):
    init_walls(board)
    place_food(board, RED_APPLE)
    place_food(board, GREEN_APPLE)
    place_food(board, GREEN_APPLE)

def init_walls(board):
    for i, a in enumerate(board):
        if i == 0 or i == 10:
            board[i] = [1 for x in a]
        else:
            a[0] = 1
            a[10] = 1
    

def main():
    board = [[0 for _ in range(11)] for _ in range(11)]
    speed = 15

    # Set up the clock
    clock = pygame.time.Clock()
    running = True
    init_board(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake_pos = "UP"
                elif event.key == pygame.K_DOWN:
                    snake_pos = "DOWN"
                elif event.key == pygame.K_LEFT:
                    snake_pos = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    snake_pos = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    running = False
                # render(board)
        win.fill('black')
        draw_grid_of_squares()
        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

if __name__ == '__main__':
    main()