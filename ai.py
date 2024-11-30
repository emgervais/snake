from utils import find_square_by_id, print_board
import macro
import numpy as np
from DQN import DQNAgent
import pygame as py
from game import move_snake
from render import render
import sys

def get_distance_to_item(line: list, target_items: int, reverse: bool) -> int:
    dist = 0
    if reverse == True:
        line = np.flip(line)
    for idx, square in enumerate(line):
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

def get_state(board: list) -> list:
    x, y, _ = find_square_by_id(board, macro.HEAD)
    vertical = np.array(board)[:, y]
    horizontal = np.array(board)[x, :]
    distance_to_obstacle_up = get_distance_to_item(vertical, {macro.WALL, macro.BODY, macro.TAIL}, False)
    distance_to_obstacle_down = get_distance_to_item(vertical, {macro.WALL, macro.BODY, macro.TAIL}, True)
    distance_to_obstacle_left = get_distance_to_item(horizontal, {macro.WALL, macro.BODY, macro.TAIL}, False)
    distance_to_obstacle_right = get_distance_to_item(horizontal, {macro.WALL, macro.BODY, macro.TAIL}, True)

    distance_to_food_up = get_distance_to_item(vertical[::-1], {macro.GREEN_APPLE}, False)
    distance_to_food_down = get_distance_to_item(vertical, {macro.GREEN_APPLE}, True)
    distance_to_food_left = get_distance_to_item(horizontal[::-1], {macro.GREEN_APPLE}, False)
    distance_to_food_right = get_distance_to_item(horizontal, {macro.GREEN_APPLE}, True)


    return [
        distance_to_obstacle_up, distance_to_obstacle_down, distance_to_obstacle_left, distance_to_obstacle_right,
        distance_to_food_up, distance_to_food_down, distance_to_food_left, distance_to_food_right,
    ]

def ai_decision(board:list, agent: DQNAgent, food_eaten: int, steps: int, counter:int, win=None, viz: bool=False) -> tuple[float, bool]:
    state = get_state(board)
    action = agent.act(state)
    prev_food = food_eaten
    reward, running, food_eaten = move_snake(board, action, food_eaten)
    if viz:
        render(board, win)
        py.display.update()

    if not "-p" in sys.argv:
        if prev_food == food_eaten:
            counter += 1
        else:
            counter = 0
        if counter >= 50:
            running = False
        reward = reward if running else -10
        if running:
            next_state = get_state(board)
        else:
            next_state = [0] * len(state)
        agent.memory.store(state, action, reward, next_state, running)
        agent.train()
    return reward, running, food_eaten, counter
