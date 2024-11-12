from utils import find_square_by_id, print_board
import macro
import numpy as np

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

def find_visible_square(board: list) -> list:
    x, y, _ = find_square_by_id(board, macro.HEAD)
    vertical = np.array(board)[:, y]
    horizontal = np.array(board)[x, :]
    return vertical, horizontal

def find_id(line: list, item: int) -> int:
    for i, square in enumerate(line):
        if square.id == item:
            return i

def get_state(vertical: list, horizontal: list) -> list:
    distance_to_obstacle_up = get_distance_to_item(vertical, {macro.WALL, macro.BODY, macro.TAIL}, False)
    distance_to_obstacle_down = get_distance_to_item(vertical, {macro.WALL, macro.BODY, macro.TAIL}, True)
    distance_to_obstacle_left = get_distance_to_item(horizontal, {macro.WALL, macro.BODY, macro.TAIL}, False)
    distance_to_obstacle_right = get_distance_to_item(horizontal, {macro.WALL, macro.BODY, macro.TAIL}, True)

    distance_to_food_up = get_distance_to_item(vertical[::-1], {macro.GREEN_APPLE}, False)
    distance_to_food_down = get_distance_to_item(vertical, {macro.GREEN_APPLE}, True)
    distance_to_food_left = get_distance_to_item(horizontal[::-1], {macro.GREEN_APPLE}, False)
    distance_to_food_right = get_distance_to_item(horizontal, {macro.GREEN_APPLE}, True)

    food_up = macro.GREEN_APPLE in vertical[::-1]
    food_down =  macro.GREEN_APPLE in vertical
    food_left =  macro.GREEN_APPLE in horizontal[::-1]
    food_right =  macro.GREEN_APPLE in horizontal

    return [
        distance_to_obstacle_up, distance_to_obstacle_down, distance_to_obstacle_left, distance_to_obstacle_right,
        distance_to_food_up, distance_to_food_down, distance_to_food_left, distance_to_food_right,
        int(food_up), int(food_down), int(food_left), int(food_right),
    ]

def ai_decision(board: list) -> int:
    vertical, horizontal = find_visible_square(board)
    state = get_state(vertical, horizontal)
    print_board(board)
    print(state)
    exit(0)