import macro
def find_square_by_id(board, target_id):
    # print_board(board)
    for ri, row in enumerate(board):
        for si, square in enumerate(row):
            if square.id == target_id:
                return ri, si, square
    # if target_id == macro.HEAD:
    #     return None
    return find_square_by_id(board, macro.HEAD)

def find_square_by_dir(board, x, y, dir):
    if dir == macro.RIGHT:
        return x, y+1, board[x][y + 1]
    elif dir == macro.LEFT:
        return x, y-1,board[x][y - 1]
    elif dir == macro.UP:
        return x-1, y,board[x - 1][y]
    elif dir == macro.DOWN:
        return x+1, y,board[x + 1][y]

def print_board(board: list):
    for line in board:
        print([square.id for square in line])
    # for line in board:
    #     print([square.dir for square in line])