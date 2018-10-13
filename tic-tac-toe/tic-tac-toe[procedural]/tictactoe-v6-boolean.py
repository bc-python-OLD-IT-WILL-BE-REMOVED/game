import re
import tkinter


# ---------------------- #
# -- SIZE OF THE GRID -- #
# ---------------------- #

GRID_SIZE = 3

# while GRID_SIZE is None:
#     GRID_SIZE = input("Size of the grid (min 3 , max = 20): ")
#
#     if not GRID_SIZE.isdigit():
#         GRID_SIZE = None
#
#     else:
#         GRID_SIZE = int(GRID_SIZE)
#
#         if not 3 <= GRID_SIZE <= 20:
#             GRID_SIZE = None


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# We use 2 bits to indicate one cell such as to have a "linear" binary
# representation of the grid.

CROSS, EMPTY, DISK = 0b01, 0b11, 0b10

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0b0

GRID_INLINE = 0b0
LINE_SIZE   = GRID_SIZE**2


# --------------- #
# -- FOR TESTS -- #
# --------------- #

DUO_MASKS_FOR_TEST = []

for token in PLAYERS:
# Tokens everywhere
    tokens_everywhere = token

    for _ in range(LINE_SIZE - 1):
        tokens_everywhere <<= 2
        tokens_everywhere  |= token

# Rows
    section_mask   = 0b1
    section_mask <<= 2*GRID_SIZE
    section_mask  -= 1

    for _ in range(GRID_SIZE):
        DUO_MASKS_FOR_TEST.append((
            section_mask,
            section_mask & tokens_everywhere
        ))

        section_mask <<= 2*GRID_SIZE

# Columns
    for i in range(GRID_SIZE):
        firstcell   = 0b11
        firstcell <<= 2*i

        section_mask = firstcell

        for _ in range(GRID_SIZE - 1):
            section_mask <<= 2*GRID_SIZE
            section_mask  |= firstcell

        DUO_MASKS_FOR_TEST.append((
            section_mask,
            section_mask & tokens_everywhere
        ))

# Diagonal LEFT-UP to RIGHT-DOWN.
    firstcell = 0b11

    for _ in range(GRID_SIZE - 1):
        section_mask <<= 2*(GRID_SIZE + 1)
        section_mask  |= firstcell

    DUO_MASKS_FOR_TEST.append((
        section_mask,
        section_mask & tokens_everywhere
    ))

# Diagonal LEFT-DOWN to RIGHT-UP.
    section_mask = 0b0

    for i in range(GRID_SIZE):
        section_mask <<= 2*(GRID_SIZE - i)
        section_mask  |= firstcell
        section_mask <<= 2*i

    DUO_MASKS_FOR_TEST.append((
        section_mask,
        section_mask & tokens_everywhere
    ))


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #

def coord_2_pos(row, col):
    global GRID_SIZE

    return GRID_SIZE*row + col


def replaceat(text, pos, token):
    global GRID_INLINE, LINE_SIZE

    left_pos = LINE_SIZE - pos - 1

    mask_right_part   = 0b1
    mask_right_part <<= 2*left_pos
    mask_right_part  -= 1

    token <<= 2*left_pos

    left_pos += 1

    left_part   = GRID_INLINE
    left_part >>= 2*left_pos
    left_part <<= 2*left_pos

    right_part = GRID_INLINE & mask_right_part

    return left_part | token | right_part


def nextplayer():
    global ACTUAL_PLAYER

    ACTUAL_PLAYER ^= 0b1


def reset_game():
    global ACTUAL_PLAYER, GRID_INLINE, LINE_SIZE

    ACTUAL_PLAYER = 0b0

    GRID_INLINE   = 0b1
    GRID_INLINE <<= 2*LINE_SIZE
    GRID_INLINE  -= 1


def cell_can_be_played(row, col):
    global GRID_INLINE, GRID_SIZE, LINE_SIZE, EMPTY

    cell   = GRID_INLINE
    cell >>= 2*(LINE_SIZE - GRID_SIZE*row - col - 1)

    return cell & EMPTY == EMPTY


def addtoken(row, col, token):
    global GRID_INLINE, GRID_SIZE

    GRID_INLINE = replaceat(GRID_INLINE, coord_2_pos(row, col), token)


def game_state():
# True : someone wins.
# None : noone wins.
# False: next player can play.
    global GRID_INLINE, EMPTY, LINE_SIZE, DUO_MASKS_FOR_TEST

# A winner ?
    for sectmask, winmask in DUO_MASKS_FOR_TEST:
        sectiontotest = GRID_INLINE & sectmask

        if sectiontotest & winmask == sectiontotest:
            return True

# Remaining choices
    cells = GRID_INLINE

    for _ in range(LINE_SIZE):
        if cells & EMPTY == EMPTY:
            return False

        cells >>= 2

# No more choice
    return None


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

        endofgame = game_state()

        if endofgame is None:
            endofgame = True
            title     = "No one wins..."

        elif endofgame:
            title = "PLAYER " + str(ACTUAL_PLAYER + 1) + " playing with " \
                  + SYMBOLS[PLAYERS[ACTUAL_PLAYER]] + " has won."

        if endofgame:
            MAIN_WINDOW.title(title + " [SEE YOUR TERMINAL]")

            input("Press some key in the terminal...")
            exit()

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
