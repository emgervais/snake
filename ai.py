from utils import find_square_by_id
import macro
import numpy as np
import pygame as py
from game import move_snake
from render import render
import sys


def get_distance_to_item(line: list, target_items: int, reverse: bool) -> int:
    dist = 0
    if reverse:
        line = np.flip(line)
    for _, square in enumerate(line):
        if square.id == macro.HEAD:
            return dist
        dist += 1
        if square.id in target_items:
            dist = 0
    return len(line)


def find_id(line: list, item: int) -> int:
    for i, square in enumerate(line):
        if square.id == item:
            return i


def get_vision(board: list) -> list:
    x, y, _ = find_square_by_id(board, macro.HEAD)
    vertical = np.array(board)[:, y]
    horizontal = np.array(board)[x, :]
    return vertical, horizontal, y


def print_vision(board: list):
    vertical, horizontal, y = get_vision(board)
    for el in vertical:
        if el.id == macro.HEAD:
            print("".join([str(el.id) for el in horizontal]))
            continue
        print(" " * (y - 1), el.id, " " * (len(horizontal) - y))


def get_state(board: list) -> list:
    vertical, horizontal, _ = get_vision(board)
    obstacle = {macro.WALL, macro.BODY, macro.TAIL}
    distance_to_obstacle_up = get_distance_to_item(vertical, obstacle, False)
    distance_to_obstacle_down = get_distance_to_item(vertical, obstacle, True)
    distance_to_obstacle_left = get_distance_to_item(horizontal,
                                                     obstacle, False)
    distance_to_obstacle_right = get_distance_to_item(horizontal,
                                                      obstacle, True)
    distance_to_food_up = get_distance_to_item(vertical[::-1],
                                               {macro.GREEN_APPLE}, False)
    distance_to_food_down = get_distance_to_item(vertical,
                                                 {macro.GREEN_APPLE}, True)
    distance_to_food_left = get_distance_to_item(horizontal[::-1],
                                                 {macro.GREEN_APPLE}, False)
    distance_to_food_right = get_distance_to_item(horizontal,
                                                  {macro.GREEN_APPLE}, True)

    return [
        distance_to_obstacle_up, distance_to_obstacle_down,
        distance_to_obstacle_left, distance_to_obstacle_right,
        distance_to_food_up, distance_to_food_down,
        distance_to_food_left, distance_to_food_right,
    ]


def ai_decision(board: list, snakeGame,
                food_eaten: int, counter: int) -> tuple[float, bool]:
    agent = snakeGame.agent
    state = get_state(board)
    action = agent.act(state)
    prev_food = food_eaten
    # if viz:
    #     print(["up", "down", "left", "right"][action])
    #     print_vision(board)
    reward, running, food_eaten = move_snake(board, action, food_eaten)
    if snakeGame.viz:
        render(board, snakeGame.square_size, snakeGame.win)
        py.display.update()

    if prev_food == food_eaten:
        counter += 1
    else:
        counter = 0
    if counter >= 50:
        running = False
        print("looped")
    if "-e" not in sys.argv:
        reward = reward if running else -10
        if running:
            next_state = get_state(board)
        else:
            next_state = [0] * len(state)
        agent.memory.store(state, action, reward, next_state, running)
        agent.train()
    return reward, running, food_eaten, counter
