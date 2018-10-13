import tkinter

from datamodel import *


# --------------------------- #
# -- CONSTANTS FOR THE GUI -- #
# --------------------------- #

SYMBOLS = {
    CROSS: "×",
    DISK : "o"
}

WHITE, BLACK = "white", "black"


MAIN_WINDOW = tkinter.Tk()

larg_ecran = MAIN_WINDOW.winfo_screenwidth()
haut_ecran = MAIN_WINDOW.winfo_screenheight()

xydim_fen = int(min(larg_ecran, haut_ecran) * .75)

xpos_fen = larg_ecran//2 - xydim_fen//2
ypos_fen = haut_ecran//2 - xydim_fen//2

MAIN_WINDOW.geometry(
    "{0}x{1}+{2}+{3}".format(
        xydim_fen, xydim_fen,
        xpos_fen, ypos_fen
    )
)


FRAME = tkinter.Frame(master = MAIN_WINDOW)

FRAME.grid(row = 0, column = 0)


XYDIM_CANVAS  = int(xydim_fen * .9)
XYDIM_CANVAS -= XYDIM_CANVAS % 3

CANVAS = tkinter.Canvas(
    master     = FRAME,
    width      = XYDIM_CANVAS - 1,
    height     = XYDIM_CANVAS - 1,
    background = WHITE
)

padforstarting = (xydim_fen - XYDIM_CANVAS) // 2

CANVAS.grid(
    row = 0, column = 0,
    padx = padforstarting,
    pady = padforstarting
)

# Draw the grid once upon the time.
WIDTH_CELL = XYDIM_CANVAS // GRID_SIZE

SHIFT_XY = 5
DIAMETER = WIDTH_CELL - 2*SHIFT_XY

position   = 1 - WIDTH_CELL

for i in range(1, GRID_SIZE + 1):
    position += WIDTH_CELL

    CANVAS.create_line(
        position, 0,
        position, XYDIM_CANVAS,
        width = 2,
        fill  = BLACK
    )

    CANVAS.create_line(
        0, position,
        XYDIM_CANVAS, position,
        width = 2,
        fill  = BLACK
    )


# --------- #
# -- GUI -- #
# --------- #

def drawtoken(row, col, token):
    global CROSS, DISK, \
           CANVAS, WIDTH_CELL, SHIFT_XY, DIAMETER, BLACK

    x_left_up = col*WIDTH_CELL + SHIFT_XY
    y_left_up = row*WIDTH_CELL + SHIFT_XY

    x_right_down = x_left_up + DIAMETER
    y_right_down = y_left_up + DIAMETER

    if token == DISK:
        CANVAS.create_oval(
            x_left_up, y_left_up,
            x_right_down, y_right_down,
            outline = BLACK
        )

    else:
        CANVAS.create_line(
            x_left_up, y_left_up,
            x_right_down, y_right_down,
            width = 2,
            fill  = BLACK
        )

        CANVAS.create_line(
            x_left_up, y_right_down,
            x_right_down, y_left_up,
            width = 2,
            fill  = BLACK
        )


def infos(actual_player, play_ing, header = True):
    global PLAYERS, SYMBOLS

    if header:
        header = "TIC TAC TOE - "

    else:
        header = ""

    return "{header}Player {nbplayer} {verb} with {symbol}".format(
        header   = header,
        nbplayer = actual_player + 1,
        verb     = play_ing,
        symbol   = SYMBOLS[PLAYERS[actual_player]]
    )


def leftclick(event):
    global GRID, GRID_SIZE, PLAYERS, ACTUAL_PLAYER, COORDS_TO_TEST, \
           MAIN_WINDOW, SYMBOLS

    row = event.y // WIDTH_CELL
    col = event.x // WIDTH_CELL

    if cell_can_be_played(
        grid  = GRID,
        row   = row,
        col   = col
    ):
        GRID = addtoken(
            grid  = GRID,
            row   = row,
            col   = col,
            token = PLAYERS[ACTUAL_PLAYER]
        )

        drawtoken(row, col, PLAYERS[ACTUAL_PLAYER])

        endofgame = game_state(grid = GRID)

        if endofgame is None:
            endofgame = True
            title = "No one wins..."

        elif endofgame:
            title = infos(
                actual_player = ACTUAL_PLAYER,
                play_ing      = "playing",
                header        = False
            ) + " has won."

        if endofgame:
            MAIN_WINDOW.title(title + " [SEE YOUR TERMINAL]")

            input("Press some key in the terminal...")
            exit()

        ACTUAL_PLAYER = nextplayer(ACTUAL_PLAYER)

        MAIN_WINDOW.title(
            infos(
                actual_player = ACTUAL_PLAYER,
                play_ing      = "plays"
            )
        )


CANVAS.bind(
    sequence = '<Button-1>',
    func     = leftclick
)


def main():
    global ACTUAL_PLAYER, GRID, \
           MAIN_WINDOW, SYMBOLS

    ACTUAL_PLAYER, GRID = reset_game(
        actual_player = ACTUAL_PLAYER,
        grid          = GRID
    )

    MAIN_WINDOW.title(
        infos(
            actual_player = ACTUAL_PLAYER,
            play_ing      = "plays"
        )
    )

    MAIN_WINDOW.mainloop()


# ------------------- #
# -- LET'S PLAY... -- #
# ------------------- #

main()
