import pygame as py
import macro
from init import init_board, draw_grid_of_squares, place_food
from ai import get_state
from utils import find_square_by_dir, find_square_by_id
from DQN import DQNAgent
import joblib as jb
import sys

def render(board: list, win):
    win.fill('black')
    draw_grid_of_squares(board, win)
    for r in board:
        for el in r:
            if(el.id == macro.EMPTY):
                continue
            elif el.id == macro.WALL:
                win.fill("grey", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))
            elif el.id == macro.RED_APPLE:
                win.fill("purple", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))
            elif el.id == macro.GREEN_APPLE:
                win.fill("green", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))
            elif el.id == macro.HEAD:
                win.fill("yellow", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))
            elif el.id == macro.BODY:
                win.fill("orange", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))
            elif el.id == macro.TAIL:
                win.fill("red", (el.x + 5, el.y + 5, macro.SQUARE_SIZE - 10, macro.SQUARE_SIZE - 10))

def calculate_reward(board: list, head: macro.square, target: macro.square, dir: int, isCloser: bool, dist: int) -> float:
    if target.id == macro.GREEN_APPLE:
        return 10
    if isCloser:
        return 0.5 / dist
    return -0.6

def find_length(board: list) -> int:
    l = 0
    for line in board:
        for square in line:
            if square.id in {macro.HEAD, macro.BODY, macro.TAIL}:
                l += 1
    return l

def find_apples(board: list) -> tuple[int, int, int, int]:
    coord = []
    for x, line in enumerate(board):
        for y, square in enumerate(line):
            if square.id == macro.GREEN_APPLE:
                coord.extend((x, y))
    return tuple(coord)

def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs((x2 - x1)) + abs((y2 - y1))

def find_dist(board:list, head_x: int, head_y: int, target_x: int, target_y: int) -> tuple[int, int]:
    apple_x1, apple_y1, apple_x2, apple_y2 = find_apples(board)
    dist_before = min(get_distance(apple_x1, apple_y1, head_x, head_y), get_distance(apple_x2, apple_y2, head_x, head_y))
    dist_after = min(get_distance(apple_x1, apple_y1, target_x, target_y), get_distance(apple_x2, apple_y2, target_x, target_y))
    return dist_before, dist_after

def move_snake(board: list, dir: int) -> tuple[int, bool]:
    head_x, head_y, head = find_square_by_id(board, macro.HEAD)
    tail_x, tail_y, tail = find_square_by_id(board, macro.TAIL)
    target_x, target_y, target = find_square_by_dir(board, head_x, head_y, dir)
    prev_dist, curr_dist = find_dist(board, head_x, head_y, target_x, target_y)
    reward = calculate_reward(board, head, target, dir, prev_dist < curr_dist, curr_dist)
    head.dir = dir
    head.id = macro.BODY
    id = target.id
    target.id = macro.HEAD
    if id == macro.GREEN_APPLE:
        place_food(board, macro.GREEN_APPLE)
        macro.length += 1
        return reward, True
    elif id == macro.RED_APPLE:
        macro.length -= 1
        if macro.length == 0:
            return reward, False
        _, _, s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
        tail.id = macro.EMPTY
        tail.dir = -1
        if macro.length > 1:
            s.id = macro.TAIL
            x, y, _ = find_square_by_id(board, macro.TAIL)
            _, _, s2 = find_square_by_dir(board, x ,y ,s.dir)
            s.dir = -1
            s.id = macro.EMPTY
            s2.id = macro.TAIL
        else:
            head.id = macro.EMPTY
            head.dir = -1
        place_food(board, macro.RED_APPLE)
        return reward, True
    elif id == macro.BODY or id == macro.TAIL or id == macro.WALL:
        return reward, False
    _, _, s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
    tail.dir = -1
    tail.id = macro.EMPTY
    s.id = macro.TAIL
    return reward, True

def main():
    board = [[macro.square(x * macro.SQUARE_SIZE, y * macro.SQUARE_SIZE, 0, -1) for x in range(11)] for y in range(11)]
    viz = False
    if '-v' in sys.argv:
        viz = True
        py.init()
        win = py.display.set_mode((macro.WIDTH, macro.HEIGHT))
        py.display.set_caption("Snake Game")  
    running = True
    manual = False
    if manual == True and viz:
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_UP:
                        _, running = move_snake(board, macro.UP)
                    elif event.key == py.K_DOWN:
                        _, running = move_snake(board, macro.DOWN)
                    elif event.key == py.K_LEFT:
                        _, running = move_snake(board, macro.LEFT)
                    elif event.key == py.K_RIGHT:
                        _, running = move_snake(board, macro.RIGHT)
                    elif event.key == py.K_ESCAPE:
                        running = False
            render(board, win)
            py.display.update()
    else:
        agent = DQNAgent(12, 4)
    iteration = 100000
    for i in range(iteration):
        try:
            board = [[macro.square(x * macro.SQUARE_SIZE, y * macro.SQUARE_SIZE, 0, -1) for x in range(11)] for y in range(11)]
            init_board(board)
            steps = 0
            total_reward = 0
            if viz:
                render(board, win)
                py.display.update()
            while 1:
                move = False
                while move == False and i > iteration - 5 and viz:
                    for event in py.event.get():
                        if event.type == py.KEYDOWN:
                            if event.key == py.K_RIGHT:
                                move = True
                state = get_state(board)
                action = agent.act(state)
                reward, running = move_snake(board, action)
                if viz:
                    render(board, win)
                    py.display.update()
                next_state = get_state(board)
                reward = reward if running else -10
                total_reward += reward
                agent.memory.store(state, action, reward, next_state, running)
                agent.train(32)
                if not running:
                    if i > iteration - iteration:
                        print(f"Episode #{i} is over with a total score of {total_reward:.1f} and length {find_length(board)} after {steps} steps")
                    break
                steps += 1
        except:
            print(f"episode #{i} had a problem")
    jb.dump(agent, "model.ml")
    py.quit()

if __name__ == '__main__':
    main()