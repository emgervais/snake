import macro


def find_square_by_id(board, target_id):
    for ri, row in enumerate(board):
        for si, square in enumerate(row):
            if square.id == target_id:
                return ri, si, square
    return find_square_by_id(board, macro.HEAD)


def find_square_by_dir(board, x, y, dir):
    if dir == macro.RIGHT:
        return x, y+1, board[x][y + 1]
    elif dir == macro.LEFT:
        return x, y-1, board[x][y - 1]
    elif dir == macro.UP:
        return x-1, y, board[x - 1][y]
    elif dir == macro.DOWN:
        return x+1, y, board[x + 1][y]


def print_board(board: list):
    for line in board:
        print([square.id for square in line])
    # for line in board:
    #     print([square.dir for square in line])


def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs((x2 - x1)) + abs((y2 - y1))


def find_dist(board: list, head_x: int, head_y: int,
              target_x: int, target_y: int) -> tuple[int, int]:
    apple_x1, apple_y1, apple_x2, apple_y2 = find_apples(board)
    dist_before = min(get_distance(apple_x1, apple_y1, head_x, head_y),
                      get_distance(apple_x2, apple_y2, head_x, head_y))
    dist_after = min(get_distance(apple_x1, apple_y1, target_x, target_y),
                     get_distance(apple_x2, apple_y2, target_x, target_y))
    return dist_before, dist_after


def find_length(board: list) -> int:
    len = 0
    for line in board:
        for square in line:
            if square.id in {macro.HEAD, macro.BODY, macro.TAIL}:
                len += 1
    return len


def find_apples(board: list) -> tuple[int, int, int, int]:
    coord = []
    for x, line in enumerate(board):
        for y, square in enumerate(line):
            if square.id == macro.GREEN_APPLE:
                coord.extend((x, y))
    return tuple(coord)
