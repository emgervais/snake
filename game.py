import macro
from utils import find_square_by_dir, find_square_by_id, find_dist, print_board
from init import place_food

def calculate_reward(board: list, head: macro.square, target: macro.square, dir: int, isCloser: bool, dist: int) -> float:
    if target.id == macro.GREEN_APPLE:
        return 10
    if isCloser:
        return 0.5 / dist
    return -0.6

def green_apple(board: list, head: macro.square, dir: int):
    if macro.length == 1:
        head.dir = dir
        head.id = macro.TAIL
    place_food(board, macro.GREEN_APPLE)
    macro.length += 1

def red_apple(board:list, x: int, y: int, tail: macro.square, head: macro.square):
        x, y, s = find_square_by_dir(board, x, y, tail.dir)
        tail.id = macro.EMPTY
        tail.dir = -1
        if macro.length > 1:
            _,_,s2 = find_square_by_dir(board, x, y, s.dir)#
            s.id = macro.EMPTY
            s.dir = -1
            s2.id = macro.TAIL
        else:
            head.id = macro.EMPTY
            head.dir = -1
        place_food(board, macro.RED_APPLE)

def move_head(target: macro.square, head: macro.square, dir:int ) -> int:
    id = target.id
    target.id = macro.HEAD
    head.dir = dir
    head.id = macro.BODY
    if macro.length == 1:
        head.dir = -1
        head.id = macro.EMPTY
    return id

def move_snake(board: list, dir: int) -> tuple[int, bool]:
    head_x, head_y, head = find_square_by_id(board, macro.HEAD)
    tail_x, tail_y, tail = find_square_by_id(board, macro.TAIL)
    target_x, target_y, target = find_square_by_dir(board, head_x, head_y, dir)

    prev_dist, curr_dist = find_dist(board, head_x, head_y, target_x, target_y)
    reward = calculate_reward(board, head, target, dir, prev_dist < curr_dist, curr_dist)

    id = move_head(target, head, dir)

    if id == macro.GREEN_APPLE:
        green_apple(board, head, dir)
        return reward, True

    elif id == macro.RED_APPLE:
        macro.length -= 1
        if macro.length == 0:
            return reward, False
        red_apple(board, tail_x, tail_y, tail, head)
        return reward, True

    elif id in {macro.BODY, macro.WALL, macro.TAIL}:
        return reward, False

    if macro.length > 1:
        _, _, s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
        tail.dir = -1
        tail.id = macro.EMPTY
        s.id = macro.TAIL

    return reward, True