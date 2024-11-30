from init import draw_grid_of_squares
import macro


def render(board: list, square_size: float,  win):
    win.fill('black')
    draw_grid_of_squares(board, square_size, win)
    s = square_size - 10
    for r in board:
        for el in r:
            if (el.id == macro.EMPTY):
                continue
            elif el.id == macro.WALL:
                win.fill("grey", (el.x + 5, el.y + 5, s, s))
            elif el.id == macro.RED_APPLE:
                win.fill("purple", (el.x + 5, el.y + 5, s, s))
            elif el.id == macro.GREEN_APPLE:
                win.fill("green", (el.x + 5, el.y + 5, s, s))
            elif el.id == macro.HEAD:
                win.fill("yellow", (el.x + 5, el.y + 5, s, s))
            elif el.id == macro.BODY:
                win.fill("orange", (el.x + 5, el.y + 5, s, s))
            elif el.id == macro.TAIL:
                win.fill("red", (el.x + 5, el.y + 5, s, s))
