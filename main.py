import pygame as py
import macro
from init import init_board, draw_grid_of_squares, place_food

def render(board, win):
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

#protect from no tail
def find_square_by_id(board, target_id):
    for ri, row in enumerate(board):
        for si, square in enumerate(row):
            if square.id == target_id:
                return ri, si, square

def find_square_by_dir(board, x, y, dir):
    if dir == macro.RIGHT:
        return board[x][y + 1]
    elif dir == macro.LEFT:
        return board[x][y - 1]
    elif dir == macro.UP:
        return board[x - 1][y]
    elif dir == macro.DOWN:
        return board[x + 1][y]

def move_snake(board, dir):
    head_x, head_y, head = find_square_by_id(board, macro.HEAD)
    tail_x, tail_y, tail = find_square_by_id(board, macro.TAIL)
    head.dir = dir
    head.id = macro.BODY
    target = find_square_by_dir(board, head_x, head_y, dir)
    id = target.id
    target.id = macro.HEAD
    if id == macro.GREEN_APPLE:
        place_food(board, macro.GREEN_APPLE)
        macro.length += 1
        return True
    elif id == macro.RED_APPLE:
        macro.length -= 1
        if macro.length == 0:
            return False
        s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
        tail.id = macro.EMPTY
        tail.dir = -1
        if macro.length > 1:
            s.id = macro.TAIL
            x, y, _ = find_square_by_id(board, macro.TAIL)
            s2 = find_square_by_dir(board, x ,y ,s.dir)
            s.dir = -1
            s.id = macro.EMPTY
            s2.id = macro.TAIL
        else:
            head.id = macro.EMPTY
            head.dir = -1
        place_food(board, macro.RED_APPLE)
        return True
    elif id == macro.BODY or id == macro.TAIL or id == macro.WALL:
        return False
    s = find_square_by_dir(board, tail_x, tail_y, tail.dir)
    tail.dir = -1
    tail.id = macro.EMPTY
    s.id = macro.TAIL
    return True

def main():
    board = [[macro.square(x * macro.SQUARE_SIZE, y * macro.SQUARE_SIZE, 0, -1) for x in range(11)] for y in range(11)]
    py.init()
    win = py.display.set_mode((macro.WIDTH, macro.HEIGHT))
    py.display.set_caption("Snake Game")  
    running = True
    init_board(board)
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    running = move_snake(board, macro.UP)
                elif event.key == py.K_DOWN:
                    running = move_snake(board, macro.DOWN)
                elif event.key == py.K_LEFT:
                    running = move_snake(board, macro.LEFT)
                elif event.key == py.K_RIGHT:
                    running = move_snake(board, macro.RIGHT)
                elif event.key == py.K_ESCAPE:
                    running = False
        win.fill('black')
        draw_grid_of_squares(board, win)
        render(board, win)
        py.display.update()

    py.quit()

if __name__ == '__main__':
    main()