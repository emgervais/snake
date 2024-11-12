import macro
def find_square_by_id(board, target_id):
    for ri, row in enumerate(board):
        for si, square in enumerate(row):
            if square.id == target_id:
                return ri, si, square
    return find_square_by_id(board, macro.HEAD)

def find_square_by_dir(board, x, y, dir):
    if dir == macro.RIGHT:
        return board[x][y + 1]
    elif dir == macro.LEFT:
        return board[x][y - 1]
    elif dir == macro.UP:
        return board[x - 1][y]
    elif dir == macro.DOWN:
        return board[x + 1][y]

def print_board(board: list):
    for line in board:
        print([square.id for square in line])