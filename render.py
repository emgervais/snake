from init import draw_grid_of_squares
import macro

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