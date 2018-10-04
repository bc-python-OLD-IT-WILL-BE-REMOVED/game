import tkinter

from logic import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

WIDTH_CELL = None

TOKENS_TK_IDS = None

GREEN, WHITE, BLACK = "green", "white", "black"

GRID, LINE = "grid", "line"

COLORS = {
    GRID  : GREEN,
    LINE  : BLACK,
    EMPTY : GREEN,
    USER_1: WHITE,
    USER_2: BLACK
}


# --------------- #
# -- FUNCTIONS -- #
# --------------- #

def closethegameornot():
    global COLORS, MAIN_WINDOW, \
           GAME_STATE, SCORES_BY_USER, USER_1, USER_2

    if thisistheendmyoldfriend():
        score_1 = GAME_STATE[SCORES_BY_USER][USER_1]
        score_2 = GAME_STATE[SCORES_BY_USER][USER_2]

        if score_1 == score_2:
            winingmessage = "Ex Aequo"

        else:
            winingmessage = 'Jeu gagné par '

            if score_1 > score_2:
                winingmessage += COLORS[USER_1]

            else:
                winingmessage += COLORS[USER_2]

            winingmessage += "."


        MAIN_WINDOW.title(
            'Othello Fini - ' + COLORS[USER_1] + ' = ' + str(score_1)
            + ' et ' + COLORS[USER_2] + ' = ' + str(score_2)
            + ' - ' + winingmessage
        )

        print("Jeu gagné !")

        while True:
            resp = input("Taper une touche pour tout stopper.\n")
            exit()


def leftclick(event):
    global MAIN_WINDOW, WIDTH_CELL, TOKENS_TK_IDS, COLORS, \
           GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER, USER_1, USER_2

# Does the game is finished ?
    closethegameornot()

# Does the actual player can play or not ?
    player_id = GAME_STATE[PLAYER_ID]

    if not GAME_STATE[TOKENS_PLAYABLE_BY_USER][player_id]:
        MAIN_WINDOW.title(
            'Othello - ' + COLORS[player_id] + ' passe, et '
            + COLORS[otheruser(player_id)] + ' joue.'
        )

        GAME_STATE[PLAYER_ID] = otheruser(player_id)

    else:
# Does the actual player have done a playable choice ?
        rownb = event.y // WIDTH_CELL
        colnb = event.x // WIDTH_CELL

        newtokens = tokenschanged(
            PLAYERS[player_id](
                row = rownb,
                col = colnb
            )
        )

        if newtokens:
            updatetokens(newtokens)

            MAIN_WINDOW.title(
                'Othello - ' + COLORS[GAME_STATE[PLAYER_ID]] + ' joue.'
            )

# Does the game is finished ?
            closethegameornot()


def changecolor(tokenid, color):
    global CANVAS

    CANVAS.itemconfigure(
        tokenid,
        fill = color
    )


def redrawgrid():
    global TOKENS_TK_IDS, COLORS, \
           GAME_STATE, \
           GRID_SIZE, PLAYING_GRID

    for rownb in range(GAME_STATE[GRID_SIZE]):
        for colnb in range(GAME_STATE[GRID_SIZE]):
            changecolor(
                tokenid = TOKENS_TK_IDS[rownb][colnb],
                color   = COLORS[GAME_STATE[PLAYING_GRID][rownb][colnb]]
            )


def launchgui():
    global TOKENS_TK_IDS, CANVAS, XYDIM_CANVAS, WIDTH_CELL, COLORS, \
           GAME_STATE, \
           GRID_SIZE, PLAYERS

# Which kind of players we have ?
    PLAYERS = [
        GAME_STATE[PLAYERS][ GAME_STATE[PLAYERS_MODES][i] ]
        for i in range(2)
    ]

# Draw the grid once upon the time.
    WIDTH_CELL = XYDIM_CANVAS // GAME_STATE[GRID_SIZE]
    position   = 1 - WIDTH_CELL

    for i in range(GAME_STATE[GRID_SIZE] + 1):
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

    TOKENS_TK_IDS = []

    ystart = 3

    for rownb in range(GAME_STATE[GRID_SIZE]):
        xstart  = 3
        newline = []

        for colnb in range(GAME_STATE[GRID_SIZE]):
            newline.append(
                CANVAS.create_oval(
                    xstart, ystart,
                    xstart + diameter, ystart + diameter,
                    outline = COLORS[GRID],
                    fill    = COLORS[GRID]
                )
            )

            xstart += WIDTH_CELL

        TOKENS_TK_IDS.append(newline)

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
XYDIM_CANVAS -= XYDIM_CANVAS % GAME_STATE[GRID_SIZE]

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
