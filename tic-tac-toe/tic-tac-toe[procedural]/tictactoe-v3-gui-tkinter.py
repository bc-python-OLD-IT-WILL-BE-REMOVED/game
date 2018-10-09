import tkinter


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CROSS, EMPTY, DISK = range(-1, 2)

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0

GRID = None

COORDS_TO_TEST = []

for nb in range(3):
    COORDS_TO_TEST.append([
        (nb, col)
        for col in range(3)
    ])

    COORDS_TO_TEST.append([
        (col, nb)
        for col in range(3)
    ])

COORDS_TO_TEST.append([
    (nb, nb)
    for nb in range(3)
])

COORDS_TO_TEST.append([
    (2 - nb, nb)
    for nb in range(3)
])


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #

def nextplayer():
    global ACTUAL_PLAYER

    ACTUAL_PLAYER += 1
    ACTUAL_PLAYER %= 2


def reset_game():
    global ACTUAL_PLAYER, GRID, EMPTY

    ACTUAL_PLAYER = 0

    GRID = {
        (row, col): EMPTY
        for row in range(3)
        for col in range(3)
    }


def cell_can_be_played(row, col):
    global GRID, EMPTY

    return GRID[row, col] == EMPTY


def addtoken(row, col, token):
    global GRID

    GRID[row, col] = token


def game_state():
    global GRID, EMPTY, COORDS_TO_TEST

# A winner ?
    for onetest in COORDS_TO_TEST:
        total = sum([
            GRID[row, col]
            for (row, col) in onetest
        ])

        if abs(total) == 3:
            return True, total // 3

# No more choice ?
    for row in range(3):
        for col in range(3):
            if GRID[row, col] == EMPTY:
                return False, None

# No more choice
    return True, None


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
WIDTH_CELL = XYDIM_CANVAS // 3

SHIFT_XY = 5
DIAMETER = WIDTH_CELL - 2*SHIFT_XY

position   = 1 - WIDTH_CELL

for i in range(1, 4):
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


def leftclick(event):
    global PLAYERS, ACTUAL_PLAYER, \
           MAIN_WINDOW, WIDTH_CELL, SYMBOLS

    row = event.y // WIDTH_CELL
    col = event.x // WIDTH_CELL

    if cell_can_be_played(row, col):
        addtoken(row, col, PLAYERS[ACTUAL_PLAYER])
        drawtoken(row, col, PLAYERS[ACTUAL_PLAYER])

        endofgame, winningtoken = game_state()

        if endofgame:
            if winningtoken == None:
                title = "No one wins..."

            else:
                title = "PLAYER " + str(ACTUAL_PLAYER + 1) + "playing with" \
                      + SYMBOLS[PLAYERS[ACTUAL_PLAYER]] + " has won."

            MAIN_WINDOW.title(title + " [SEE YOUR TERMINAL]")

            input("Press some key in the terminal...")

            exit()

        else:
            nextplayer()

            MAIN_WINDOW.title(
                'TIC TAC TOE - Player ' + str(ACTUAL_PLAYER + 1) + " plays with " + SYMBOLS[PLAYERS[ACTUAL_PLAYER]]
            )


CANVAS.bind(
    sequence = '<Button-1>',
    func     = leftclick
)


def main():
    global PLAYERS, ACTUAL_PLAYER, \
           MAIN_WINDOW, SYMBOLS


    reset_game()

    MAIN_WINDOW.title(
        'TIC TAC TOE - Player ' + str(ACTUAL_PLAYER + 1) + " plays with " + SYMBOLS[PLAYERS[ACTUAL_PLAYER]]
    )

    MAIN_WINDOW.mainloop()


# ------------------- #
# -- LET'S PLAY... -- #
# ------------------- #

main()
