import tkinter

"""
Source for the rules and some useful comments :
    * http://www.lecomptoirdesjeux.com/regle-reversi.htm

This version is just for testing : only two humans can play using the mouse.
"""


# ------------------------------------------- #
# -- GENERAL CONSTANTS - LOGIC OF THE GAME -- #
# ------------------------------------------- #

GRID_SIZE = 8

# GRID_SIZE must be an even integer between 6 and 16 !
if not isinstance(GRID_SIZE, int) \
or not 5 < GRID_SIZE < 17 \
or GRID_SIZE %2 != 0:
    raise Exception(
        "GRID_SIZE must an even integer between 6 and 16 : GRID_SIZE = "
        + str(GRID_SIZE)
    )

# Little trick : 1 + 1 = 0 mod 2 , and 0 + 1 = 1 mod 2 make it easy
# to change the ID of the user who is playing.
EMPTY          = None
USER_1, USER_2 = range(2)

PLAYER_ID = USER_1 # The USER_1 starts to play.

PLAYING_GRID = [
    [EMPTY for _ in range(GRID_SIZE)]
    for _ in range(GRID_SIZE)
]

TOKENS_MAYBE_PLAYABLE = set()

TOKENS_PLAYABLE_BY_USER = {
    USER_1: {},
    USER_2: {}
}

SCORES_BY_USER = {
    USER_1: 0,
    USER_2: 0
}


# --------------------------- #
# -- CONSTANTS FOR THE GUI -- #
# --------------------------- #

WIDTH_CELL = None

TOKEN_IDS = None

GREEN, WHITE, BLACK = "green", "white", "black"

GRID, LINE = "grid", "line"

COLORS = {
    GRID  : GREEN,
    LINE  : BLACK,
    EMPTY : GREEN,
    USER_1: WHITE,
    USER_2: BLACK
}


# ------------------------------------------- #
# -- GENERAL FUNCTIONS - LOGIC OF THE GAME -- #
# ------------------------------------------- #

def thisistheendmyoldfriend():
    """
This function simply indicates that the game is finished or not.
    """
    global TOKENS_PLAYABLE_BY_USER

    return (
        not TOKENS_PLAYABLE_BY_USER[USER_1]
        and
        not TOKENS_PLAYABLE_BY_USER[USER_2]
    )


def otheruser(userid):
    """
This function switches the user ID :
    * 1 ---> 0
    * 0 ---> 1
    """
    return (userid + 1) % 2


def isingrid(rownb, colnb):
    """
This function simply tests if the row's and column's numbers are legal ones.
    """
    global GRID_SIZE

    return (
        0 <= rownb < GRID_SIZE
        and
        0 <= colnb < GRID_SIZE
    )


def addtoken(rownb, colnb, tokenid):
    """
This function adds a new token.

The variables `SCORES_BY_USER` and `TOKENS_MAYBE_PLAYABLE` are updated.
    """
    global PLAYING_GRID, EMPTY, \
           TOKENS_MAYBE_PLAYABLE, SCORES_BY_USER

    PLAYING_GRID[rownb][colnb] = tokenid

    if tokenid != EMPTY:
        SCORES_BY_USER[tokenid]   += 1

        for row in range(rownb - 1, rownb + 2):
            for col in range(colnb  - 1, colnb + 2):
                if isingrid(row, col):
                    coords = (row, col)

                    if PLAYING_GRID[row][col] == EMPTY:
                        TOKENS_MAYBE_PLAYABLE.add(coords)

                    else:
# We can't use here the method `remove`.
                        TOKENS_MAYBE_PLAYABLE -= set([coords])


def switchtoken(rownb, colnb):
    """
This function only changes a token of one user to a token of the other user.

The variable `SCORES_BY_USER` is updated.
    """
    global PLAYING_GRID, \
           SCORES_BY_USER

    tokenid = PLAYING_GRID[rownb][colnb]

    if tokenid == EMPTY:
        raise Exception("impossible to switch an empty cell")

    otherid = otheruser(tokenid)

    PLAYING_GRID[rownb][colnb] = otherid

    SCORES_BY_USER[tokenid] -= 1
    SCORES_BY_USER[otherid] += 1


def searchonedirection(rowtest, coltest, deltarow, deltacol, tokenid):
    """
This function looks at consecutive switchable tokens forward one direction.
    """
    global PLAYING_GRID, EMPTY

    tokensfound = []

    while isingrid(rowtest, coltest):
        if PLAYING_GRID[rowtest][coltest] in [EMPTY, tokenid]:
            break

        tokensfound.append( (rowtest, coltest) )

        rowtest += deltarow
        coltest += deltacol

    if not isingrid(rowtest, coltest) \
    or PLAYING_GRID[rowtest][coltest] == EMPTY:
        tokensfound = []

    return tokensfound


def searchalldirections(rowstart, colstart, tokenid):
    """
This function looks for switchable tokens in all directions.
    """
    global PLAYING_GRID, EMPTY, TOKENS_MAYBE_PLAYABLE

    tokensfound = []

    if (rowstart, colstart) in TOKENS_MAYBE_PLAYABLE:
        for deltarow in range(-1, 2):
            rowtest = rowstart + deltarow

            for deltacol in range(-1, 2):
                coltest = colstart + deltacol

                if (deltarow, deltacol) != (0, 0) \
                and isingrid(rowtest, coltest) \
                and PLAYING_GRID[rowtest][coltest] not in [EMPTY, tokenid]:
                    tokensfound += searchonedirection(
                        rowtest  = rowtest,
                        coltest  = coltest,
                        deltarow = deltarow,
                        deltacol = deltacol,
                        tokenid  = tokenid
                    )

    return tokensfound


def findplayable():
    """
We look all empty cells near tokens where each user can play.
    """
    global TOKENS_MAYBE_PLAYABLE, TOKENS_PLAYABLE_BY_USER

    TOKENS_PLAYABLE_BY_USER = {
        USER_1: {},
        USER_2: {}
    }

    for row, col in TOKENS_MAYBE_PLAYABLE:
        for tokenid in [USER_1, USER_2]:
            tokensfound = searchalldirections(
                rowstart = row,
                colstart = col,
                tokenid  = tokenid
            )

# One token can be playable by the two users.
            if tokensfound:
                TOKENS_PLAYABLE_BY_USER[tokenid][(row, col)] = tokensfound


def resetgrid():
    """
This function (re)sets the grid in the original organization.
    """
    global PLAYING_GRID, GRID_SIZE, \
           SCORES_BY_USER, TOKENS_MAYBE_PLAYABLE

    TOKENS_MAYBE_PLAYABLE = set()

    SCORES_BY_USER = {
        USER_1: 0,
        USER_2: 0
    }

    middle_next = GRID_SIZE // 2
    middle      = middle_next - 1

    user_1_first_tokens = [(middle, middle), (middle_next, middle_next)]
    user_2_first_tokens = [(middle, middle_next), (middle_next, middle)]

    for rownb in range(GRID_SIZE):
        for colnb in range(GRID_SIZE):
            coords = (rownb, colnb)

            if coords in user_1_first_tokens:
                tokenid = USER_1

            elif coords in user_2_first_tokens:
                tokenid = USER_2

            else:
                tokenid = EMPTY

            addtoken(
                rownb   = rownb,
                colnb   = colnb,
                tokenid = tokenid
            )

    findplayable()


def tokenschanged(row, col):
    """
This function updates all tokens changed if the cell played has coordinates
`(row, col)`.

The function returns all the taken changed.
    """
    global PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    coords = (row, col)

    tokenfound = []

    if coords in TOKENS_PLAYABLE_BY_USER[PLAYER_ID]:
        tokenfound.append(coords)
        addtoken(row, col, PLAYER_ID)

        for (row, col) in TOKENS_PLAYABLE_BY_USER[PLAYER_ID][coords]:
            tokenfound.append( (row, col) )
            switchtoken(row, col)

    return tokenfound


# --------------------------- #
# -- FUNCTIONS FOR THE GUI -- #
# --------------------------- #

def leftclick(event):
    global MAIN_WINDOW, WIDTH_CELL, TOKEN_IDS, COLORS, \
           PLAYER_ID, USER_1, USER_2, TOKENS_PLAYABLE_BY_USER, SCORES_BY_USER

# Does the game is finished ?
    if thisistheendmyoldfriend():
        MAIN_WINDOW.title(
            'Othello - ' + COLORS[USER_1] + ' = '
            + str(SCORES_BY_USER[USER_1])
            + ' et ' + COLORS[USER_2] + ' = '
            + str(SCORES_BY_USER[USER_2])
        )

        print("Jeu fini !")

        while True:
            resp = input("Taper une touche pour tout stopper.\n")
            exit()

# Does the actual player can play or not ?
    if not TOKENS_PLAYABLE_BY_USER[PLAYER_ID]:
        MAIN_WINDOW.title(
            'Othello - ' + COLORS[PLAYER_ID] + ' passe, et '
            + COLORS[otheruser(PLAYER_ID)] + ' joue.'
        )

        PLAYER_ID = otheruser(PLAYER_ID)

    else:
# Does the actual player have done a playable choice ?
        rownb = event.y // WIDTH_CELL
        colnb = event.x // WIDTH_CELL

        newtokens = tokenschanged(
            row = rownb,
            col = colnb
        )

        if newtokens:
            for (row, col) in newtokens:
                changecolor(
                    tokenid = TOKEN_IDS[row][col],
                    color   = COLORS[PLAYER_ID]
                )

            PLAYER_ID = otheruser(PLAYER_ID)

            MAIN_WINDOW.title(
                'Othello - ' + COLORS[PLAYER_ID] + ' joue.'
            )

            findplayable()


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
    global TOKEN_IDS, CANVAS, XYDIM_CANVAS, WIDTH_CELL, COLORS, \
           GRID_SIZE

# Draw the grid once upon the time.
    WIDTH_CELL = XYDIM_CANVAS // GRID_SIZE
    position   = 1 - WIDTH_CELL

    for i in range(GRID_SIZE + 1):
        position += WIDTH_CELL

        CANVAS.create_line(
            position, 0,
            position, XYDIM_CANVAS,
            width = 2,
            fill  = COLORS[LINE]
        )

        CANVAS.create_line(
            0, position,
            XYDIM_CANVAS, position,
            width = 2,
            fill  = COLORS[LINE]
        )

# Draw all the tokens for ease the managment later by storing their ID
# in an easy to use matrix.
#
# The IDs will be used just to change the color of the tokens.
    diameter = WIDTH_CELL - 6

    TOKEN_IDS = []

    ystart = 3

    for rownb in range(GRID_SIZE):
        xstart  = 3
        newline = []

        for colnb in range(GRID_SIZE):
            newline.append(
                CANVAS.create_oval(
                    xstart, ystart,
                    xstart + diameter, ystart + diameter,
                    outline = COLORS[GRID],
                    fill    = COLORS[GRID]
                )
            )

            xstart += WIDTH_CELL

        TOKEN_IDS.append(newline)

        ystart += WIDTH_CELL

# Draw the initial playing grid.
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


XYDIM_CANVAS  = int(xydim_fen * .9)
XYDIM_CANVAS -= XYDIM_CANVAS % GRID_SIZE

CANVAS = tkinter.Canvas(
    master     = FRAME,
    width      = XYDIM_CANVAS - 1,
    height     = XYDIM_CANVAS - 1,
    background = COLORS[GRID]
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
