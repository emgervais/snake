import pygame as py
import macro
from init import init_board, draw_grid_of_squares, place_food
from ai import get_state
from utils import find_square_by_dir, find_square_by_id, print_board
from DQN import DQNAgent
import joblib as jb
import sys
import time
import threading
import os
import signal

class exitTrainingProgram(Exception): 
    pass

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

    # Calculate reward based on distances and direction
    reward = calculate_reward(board, head, target, dir, prev_dist < curr_dist, curr_dist)

    id = target.id
    target.id = macro.HEAD  # Move the head
    head.dir = dir
    head.id = macro.BODY  # Update previous head position to body

    if macro.length == 1:
        head.dir = -1
        head.id = macro.EMPTY  # Reset head if snake is reduced to single length

    # Handling various targets
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
        else:
            head.id = macro.EMPTY
            head.dir = -1
        place_food(board, macro.RED_APPLE)
        return reward, True
    elif id in {macro.BODY, macro.WALL, macro.TAIL}:
        return reward, False

    # Update the tail if snake length > 1
    if macro.length > 1:
        _, _, s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
        tail.dir = -1
        tail.id = macro.EMPTY
        s.id = macro.TAIL

    return reward, True

def key_hook():
    global delay
    try:
        while True:
            if close:
                break
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    if event.key == py.K_RIGHT:
                        delay += 0.1
                    elif event.key == py.K_LEFT and delay - 0.1 >= 0:
                        delay -= 0.1
                    elif event.key == py.K_ESCAPE:
                        raise exitTrainingProgram
                time.sleep(0.01)
            time.sleep(0.05)
    except exitTrainingProgram:
        print(f"Training was ended")
        py.quit()
        os.kill(os.getpid(), signal.SIGINT)

def ai_decision(board:list, agent: DQNAgent, win=None, viz: bool=False) -> tuple[float, bool]:
    state = get_state(board)
    action = agent.act(state)
    reward, running = move_snake(board, action)
    reward = reward if running else -10
    if viz:
        render(board, win)
        py.display.update()
    next_state = get_state(board)
    agent.memory.store(state, action, reward, next_state, running)
    agent.train(32)
    return reward, running

delay = 0
def main():
    global close
    close = False
    viz = False
    iteration = 0
    win = None
    if '-v' in sys.argv:
        viz = True
        py.init()
        win = py.display.set_mode((macro.WIDTH, macro.HEIGHT))
        py.display.set_caption("Snake Game") 
        keyhook_thread = threading.Thread(target=key_hook)
        keyhook_thread.start()
    try:
        i = sys.argv.index('-i') + 1
        iteration = int(sys.argv[i])
        if iteration <= 0:
            print(f"Please enter the amount of iterations greater than 0")
    except:
        print(f"Please enter the amount of iterations with the flag -i num_of_iterations")
        exit(1)
    agent = DQNAgent(12, 4)
    try:
        for i in range(iteration):
            board = init_board()
            if viz:
                render(board, win)
                py.display.update()
            steps = 0
            total_reward = 0
            while 1:
                time.sleep(delay)
                reward, running = ai_decision(board, agent, win, viz)
                total_reward += reward
                if not running:
                    if i > iteration - iteration:
                        print(f"Episode #{i} is over with a total score of {total_reward:.1f} and length {find_length(board)} after {steps} steps")
                    break
                steps += 1
    except KeyboardInterrupt as e:
        print(e)
        close = True
        py.quit()
        exit(0)
    jb.dump(agent, "model.ml")
    py.quit()
    exit(0)

if __name__ == '__main__':
    main()