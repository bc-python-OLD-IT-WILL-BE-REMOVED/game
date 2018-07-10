import tkinter

"""
1er essai avec le fonctionnement général mais pas complet !

Joueur passant un coup pas géré : cas où un pion impossible à ajouter dans ce cas la règle impose de passer son rtour !

http://www.lecomptoirdesjeux.com/regle-reversi.htm
"""

# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

GRID_SIZE = 8

EMPTY          = None
USER_1, USER_2 = range(2)
# This allows to change the player's ID adiing 1 modulus 2.

PLAYING_GRID = [
    [EMPTY for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE)
]

PLAYER_ID = USER_1 # The USER_1 starts to play.

# GRID_SIZE must be even !
if GRID_SIZE %2 != 0:
    raise Exception(
        "GRID_SIZE must be even : GRID_SIZE = " + str(GRID_SIZE)
    )


# ----------------------- #
# -- CONSTANTS FOR GUI -- #
# ----------------------- #

DELTA = None

TOKEN_IDS = None

GREEN, WHITE, BLACK = "green", "white", "black"

COLORS = {
    "grid": GREEN,
    "line": BLACK,
    EMPTY : GREEN,
    USER_1  : WHITE,
    USER_2    : BLACK
}


# ----------------------- #
# -- GENERAL FUNCTIONS -- #
# ----------------------- #

def resetgrid():
    global PLAYING_GRID, GRID_SIZE

    middle_next = GRID_SIZE // 2
    middle      = middle_next - 1

    USER_2tokens = [
        (middle, middle_next), (middle_next, middle)
    ]

    playertokens = [
        (middle, middle), (middle_next, middle_next)
    ]

    for rownb in range(GRID_SIZE):
        for colnb in range(GRID_SIZE):
            coords = (rownb, colnb)

            if coords in USER_2tokens:
                PLAYING_GRID[rownb][colnb] = USER_2

            elif coords in playertokens:
                PLAYING_GRID[rownb][colnb] = USER_1

            else:
                PLAYING_GRID[rownb][colnb] = EMPTY

def searchonedirection(rowstart, colstart, deltarow, deltacol):
    global GRID_SIZE, PLAYING_GRID, EMPTY, PLAYER_ID

# << IMPORTANT ! >>
#
# We know that
#     `PLAYING_GRID[rowstart][colstart] = player_id`
# and that
#     `PLAYING_GRID[rowstart + deltarow][colstart + deltacol]`
# is the other player ID.
    tokensfound = [ (rowstart + deltarow, colstart + deltacol) ]

    rowtest = rowstart + 2*deltarow
    coltest = colstart + 2*deltacol

    while(
        0 <= rowtest < GRID_SIZE
        and
        0 <= coltest < GRID_SIZE
    ):
        if PLAYING_GRID[rowtest][coltest] in [EMPTY, PLAYER_ID]:
            break

        tokensfound.append( (rowtest, coltest) )

        rowtest += deltarow
        coltest += deltacol

    if not(0 <= rowtest < GRID_SIZE) \
    or not(0 <= coltest < GRID_SIZE) \
    or PLAYING_GRID[rowtest][coltest] != PLAYER_ID:
        tokensfound = []

    return tokensfound

def tokenstochange(rowstart, colstart):
    global GRID_SIZE, PLAYING_GRID, EMPTY, PLAYER_ID, \
           NB_TOKENS_AVAILABLE, NB_TOKENS_PLAYED

    tokensfound = []

    if PLAYING_GRID[rowstart][colstart] == EMPTY:
        for deltarow in range(-1, 2):
            rowtest = rowstart + deltarow

            for deltacol in range(-1, 2):
                coltest = colstart + deltacol

                if (deltarow, deltacol) != (0, 0) \
                and 0 <= rowtest < GRID_SIZE \
                and 0 <= coltest < GRID_SIZE \
                and PLAYING_GRID[rowtest][coltest] not in [EMPTY, PLAYER_ID]:
                    tokensfound += searchonedirection(
                        rowstart = rowstart,
                        colstart = colstart,
                        deltarow = deltarow,
                        deltacol = deltacol
                    )

    if tokensfound:
        for (row, col) in tokensfound:
            PLAYING_GRID[row][col] = PLAYER_ID

        PLAYING_GRID[rowstart][colstart] = PLAYER_ID

        PLAYER_ID += 1
        PLAYER_ID %= 2

    return tokensfound


# ----------------------- #
# -- FUNCTIONS FOR GUI -- #
# ----------------------- #

def leftclick(event):
    global MAIN_WINDOW, DELTA, TOKEN_IDS, COLORS, \
           PLAYER_ID

    actual_player = PLAYER_ID

    rownb = event.y // DELTA
    colnb = event.x // DELTA

    newtokens = tokenstochange(
        rowstart = rownb,
        colstart = colnb
    )

    if newtokens:
        MAIN_WINDOW.title(
            'Othello - Joueur ' + COLORS[PLAYER_ID] + ' doit jouer.'
        )

        changecolor(
            tokenid = TOKEN_IDS[rownb][colnb],
            color   = COLORS[actual_player]
        )

        for (row, col) in newtokens:
            changecolor(
                tokenid = TOKEN_IDS[row][col],
                color   = COLORS[actual_player]
            )


def changecolor(tokenid, color):
    global CANVAS

    CANVAS.itemconfigure(
        tokenid,
        fill = color
    )

def redrawgrid():
    global TOKEN_IDS, COLORS, \
           PLAYING_GRID

    for rownb in range(GRID_SIZE):
        for colnb in range(GRID_SIZE):
            changecolor(
                tokenid = TOKEN_IDS[rownb][colnb],
                color   = COLORS[PLAYING_GRID[rownb][colnb]]
            )


def launchgui():
    global TOKEN_IDS, CANVAS, XYDIM_CANVAS, DELTA, COLORS, \
           GRID_SIZE

# Draw the grid once upon the time.
    DELTA    = XYDIM_CANVAS // GRID_SIZE
    position = 1 - DELTA

    for i in range(GRID_SIZE + 1):
        position += DELTA

        CANVAS.create_line(
            position, 0,
            position, XYDIM_CANVAS,
            width = 2,
            fill  = COLORS["line"]
        )

        CANVAS.create_line(
            0, position,
            XYDIM_CANVAS, position,
            width = 2,
            fill  = COLORS["line"]
        )

# Draw all the tokens for ease the managment later by storing their ID
# in an easy to use matrix.
#
# The IDs will be use just to change the color of the tokens.
    dUSER_2meter = DELTA - 6

    TOKEN_IDS = []

    ystart = 3

    for rownb in range(GRID_SIZE):
        xstart  = 3
        newline = []

        for colnb in range(GRID_SIZE):
            newline.append(
                CANVAS.create_oval(
                    xstart, ystart,
                    xstart + dUSER_2meter, ystart + dUSER_2meter,
                    outline = COLORS["grid"],
                    fill    = COLORS["grid"]
                )
            )

            xstart += DELTA

        TOKEN_IDS.append(newline)

        ystart += DELTA

# Draw the initUSER_2l playing grid.
    resetgrid()
    redrawgrid()

# Interaction
    CANVAS.bind(
        sequence = '<Button-1>',
        func     = leftclick
    )

# Let's start to play...
    MAIN_WINDOW.mainloop()



# --------- #
# -- GUI -- #
# --------- #

MAIN_WINDOW = tkinter.Tk()
MAIN_WINDOW.title(
    'Aplha Othello - À vous de commencer, vous avez les ' + COLORS[USER_1] + '.'
)

# Dimensions choisies pour la fenêtre

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


XYDIM_CANVAS = int(xydim_fen * .9)
XYDIM_CANVAS -= XYDIM_CANVAS % GRID_SIZE

CANVAS = tkinter.Canvas(
    master     = FRAME,
    width      = XYDIM_CANVAS - 1,
    height     = XYDIM_CANVAS - 1,
    background = COLORS["grid"]
)

padforstarting = (xydim_fen - XYDIM_CANVAS) // 2

CANVAS.grid(
    row = 0, column = 0,
    padx = padforstarting,
    pady = padforstarting
)


# ---------------- #
# -- LET'S GO ! -- #
# ---------------- #

launchgui()
