import re
import tkinter


# ---------------------- #
# -- SIZE OF THE GRID_INLINE -- #
# ---------------------- #

GRID_SIZE = None

while GRID_SIZE is None:
    GRID_SIZE = input("Size of the GRID_INLINE (min 3 , max = 20): ")

    if not GRID_SIZE.isdigit():
        GRID_SIZE = None

    else:
        GRID_SIZE = int(GRID_SIZE)

        if not 3 <= GRID_SIZE <= 20:
            GRID_SIZE = None


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# << Warning ! >>
# DO NOT USE SPECIAL REGEX CARACTERS.

CROSS, EMPTY, DISK = "× o"

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0

GRID_INLINE = None
LINE_SIZE   = GRID_SIZE**2


# --------------- #
# -- FOR TESTS -- #
# --------------- #

PATTERN_TO_TEST = []

pattern_template = ["." for _ in range(LINE_SIZE)]

for token in PLAYERS:
    or_patterns = []

    for row in range(GRID_SIZE):
        row_pattern = pattern_template[:]
        col_pattern = pattern_template[:]

        firsttoken = True

        for col in range(GRID_SIZE):
            if firsttoken:
                regtoken = "({0})".format(token)
                firsttoken = False

            else:
                regtoken = token

            row_pattern[3*row + col] = regtoken
            col_pattern[3*col + row] = regtoken

        or_patterns += [row_pattern, col_pattern]

    diag_1_pattern = pattern_template[:]
    diag_2_pattern = pattern_template[:]

    firsttoken = True

    for row in range(GRID_SIZE):
        if firsttoken:
            regtoken = "({0})".format(token)
            firsttoken = False

        else:
            regtoken = token

        diag_1_pattern[(GRID_SIZE + 1)*row]     = regtoken
        diag_2_pattern[2 + (GRID_SIZE - 1)*row] = regtoken

    or_patterns += [diag_1_pattern, diag_2_pattern]
    or_patterns  = ["".join(x) for x in or_patterns]

    PATTERN_TO_TEST.append(
        "|".join(
            "({0})".format(x) for x in or_patterns
        )
    )

PATTERN_TO_TEST = "^{0}$".format("|".join(PATTERN_TO_TEST))
PATTERN_TO_TEST = re.compile(PATTERN_TO_TEST)


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #


def replaceat(text, pos, char):
    return text[:pos] + char + text[pos + 1:]


def nextplayer():
    global ACTUAL_PLAYER

    ACTUAL_PLAYER += 1
    ACTUAL_PLAYER %= 2


def reset_game():
    global ACTUAL_PLAYER, GRID_INLINE, EMPTY

    ACTUAL_PLAYER = 0

    GRID_INLINE = EMPTY*LINE_SIZE


def cell_can_be_played(row, col):
    global GRID_INLINE, EMPTY

    return GRID_INLINE[3*row + col] == EMPTY


def addtoken(row, col, token):
    global GRID_INLINE

    GRID_INLINE = replaceat(GRID_INLINE, 3*row + col, token)


def game_state():
    global GRID_INLINE, GRID_SIZE, EMPTY, PATTERN_TO_TEST

# A winner ?
    match = PATTERN_TO_TEST.search(GRID_INLINE)

    if match:
        return True, CROSS

# No more choice ?
    if EMPTY in GRID_INLINE:
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

# Draw the GRID_INLINE once upon the time.
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
                title = "PLAYER " + str(ACTUAL_PLAYER + 1) + " playing with " \
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
