import macro
from utils import find_square_by_dir, find_square_by_id, \
                        find_dist, find_length
from init import place_food


def calculate_reward(target: macro.square, isCloser: bool) -> float:
    if target.id == macro.GREEN_APPLE:
        return 10
    if isCloser:
        return 0.1
    return -1


def green_apple(board: list, head: macro.square, dir: int, length: int):
    if length == 1:
        head.dir = dir
        head.id = macro.TAIL
    place_food(board, macro.GREEN_APPLE)
    length += 1


def red_apple(board: list, x: int, y: int, tail: macro.square,
              head: macro.square, length: int):
    x, y, s = find_square_by_dir(board, x, y, tail.dir)
    tail.id = macro.EMPTY
    tail.dir = -1
    if length > 2:
        _, _, s2 = find_square_by_dir(board, x, y, s.dir)
        s.id = macro.EMPTY
        s.dir = -1
        s2.id = macro.TAIL
    else:
        head.id = macro.EMPTY
        head.dir = -1
    place_food(board, macro.RED_APPLE)


def move_head(target: macro.square, head: macro.square,
              dir: int, length: int) -> int:
    id = target.id
    target.id = macro.HEAD
    head.dir = dir
    head.id = macro.BODY
    if length == 1:
        head.dir = -1
        head.id = macro.EMPTY
    return id


def move_snake(board: list, dir: int, food_eaten: int) -> tuple[int, bool]:
    head_x, head_y, head = find_square_by_id(board, macro.HEAD)
    tail_x, tail_y, tail = find_square_by_id(board, macro.TAIL)
    target_x, target_y, target = find_square_by_dir(board, head_x, head_y, dir)
    length = find_length(board)
    prev_dist, curr_dist = find_dist(board, head_x, head_y, target_x, target_y)
    reward = calculate_reward(target, prev_dist > curr_dist)

    id = move_head(target, head, dir, length)

    if id == macro.GREEN_APPLE:
        green_apple(board, head, dir, length)
        food_eaten += 1
        return reward, True, food_eaten

    elif id == macro.RED_APPLE:
        if length == 1:
            return reward, False, food_eaten
        red_apple(board, tail_x, tail_y, tail, head, length)
        return reward, True, food_eaten

    elif id in {macro.BODY, macro.WALL, macro.TAIL}:
        return reward, False, food_eaten

    if length > 1:
        _, _, s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
        tail.dir = -1
        tail.id = macro.EMPTY
        s.id = macro.TAIL

    return reward, True, food_eaten
