from time import sleep
import tkinter

from logic import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

# Useful
#     * 0   : steps controlled by pressing on ENTER.
#     * < 0 : no steps shown except when a human plays.
PAUSE = 0#.35

GREEN, WHITE, BLACK = "green", "white", "black"

COLORS = {
    EMPTY : GREEN,
    USER_1: WHITE,
    USER_2: BLACK
}


# --------------- #
# -- FUNCTIONS -- #
# --------------- #

def closethegameornot():
    global GAME_STATE, SCORES_BY_USER, USER_1, USER_2

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


        print(
            'Othello Fini - ' + COLORS[USER_1] + ' = ' + str(score_1)
            + ' et ' + COLORS[USER_2] + ' = ' + str(score_2)
            + ' - ' + winingmessage
        )

        while True:
            resp = input("Taper une touche pour tout stopper.\n")
            exit()


def choosecoords():
    global GAME_STATE, GRID_SIZE

    redrawgrid()

    coords = input("Colonne Ligne choisies spéarées par un espace : ").upper()

    coords = [x.strip() for x in coords.split(" ")]

    while len(coords) != 2 \
    or coords[0] not in COLNAMES \
    or coords[1] not in [
        str(i + 1)
        for i in range(GAME_STATE[GRID_SIZE])
    ]:
        redrawgrid()

        coords = input(
            "Choix illégaux. Colonne Ligne choisies spéarées par un espace : "
        ).upper()

        coords = [x.strip() for x in coords.split(" ")]

    row = int(coords[1]) - 1
    col = ord(coords[0]) - ord('A')

    return row, col


def sleepgame():
    global PAUSE

    if PAUSE < 0:
        ...

    elif PAUSE == 0:
        input("Presser entrée pour continuer...")

    else:
        sleep(PAUSE)


def playthegame():
    global THE_PLAYERS_INTERACT, PAUSE, \
           GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER, USER_1, USER_2

# Does the game is finished ?
    closethegameornot()

# Does the actual player can play or not ?
    player_id = GAME_STATE[PLAYER_ID]

    if not GAME_STATE[TOKENS_PLAYABLE_BY_USER][player_id]:
        print(
            'Othello - ' + COLORS[player_id] + ' passe, et '
            + COLORS[otheruser(player_id)] + ' joue.'
        )

        GAME_STATE[PLAYER_ID] = otheruser(player_id)

    else:
# Does the actual player have done a playable choice ?
        if THE_PLAYERS_INTERACT[player_id]:
            rownb, colnb = choosecoords()

        else:
            rownb, colnb = None, None

        newtokens = tokenschanged(
            THE_PLAYERS[player_id](
                row = rownb,
                col = colnb
            )
        )

# Just for human(?) debugging...  -  START
        print("playthegame :: newtokens :", newtokens)
        print("               TOKENS_PLAYABLE_BY_USER : ", GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]])
# Just for human(?) debugging...  -  END

        if PAUSE == 0 and not THE_PLAYERS_INTERACT[player_id]:
            sleepgame()

        if newtokens:
            updatetokens(newtokens)

            redrawgrid()

# Does the game is finished ?
            closethegameornot()

# Lets' continue...
    sleepgame()
    playthegame()


def drawtoken(color):
# Sources:
#     * https://unicode-table.com/fr
#     * https://stackoverflow.com/a/39452138/4589608
    global COLORS, EMPTY, USER_1

    if color == COLORS[EMPTY]:
        token = "."

    elif color == COLORS[USER_1]:
        token = "\u2B24"

    else:
        token = "\033[91m\u2B24\033[97m"

    print("", token, end = " ")


def redrawgrid():
# Source:
#     * https://stackoverflow.com/a/50921841/4589608
    global COLORS, LINE, NB_DIGITSINFOS, \
           GAME_STATE, \
           GRID_SIZE, PLAYING_GRID

# Let's clear the terminal.
    # print("\033c\033[97m")
    print("\n ==="*3)

    print(UPDOWNGRIDLINE)

    for rownb in range(GAME_STATE[GRID_SIZE]):
        rowinfo = str(rownb + 1)
        print(rowinfo.rjust(NB_DIGITSINFOS), "| ", end = "")

        for colnb in range(GAME_STATE[GRID_SIZE]):
            drawtoken(
                COLORS[GAME_STATE[PLAYING_GRID][rownb][colnb]]
            )

        print(" |", rowinfo)

    print(UPDOWNGRIDLINE)

    print(
        'Othello - ' + COLORS[GAME_STATE[PLAYER_ID]] + ' joue.'
    )


def launchgui():
    global COLORS, UPDOWNGRIDLINE, NB_DIGITSINFOS, COLNAMES, \
           GAME_STATE, \
           GRID_SIZE, THE_PLAYERS, THE_PLAYERS_INTERACT

# Which kind of players we have ?
    THE_PLAYERS = [
        GAME_STATE[PLAYERS][ GAME_STATE[PLAYERS_MODES][i] ]
        for i in range(2)
    ]

# Do we have to ask the player to give coordinates ?
    THE_PLAYERS_INTERACT = [
        bool(0 == GAME_STATE[PLAYERS_MODES][i])
        for i in range(2)
    ]

# Draw the initial playing grid.
    NB_DIGITSINFOS = len(str(GAME_STATE[GRID_SIZE]))
    COLNAMES       = [
        chr(ord('A') + i)
        for i in range(GAME_STATE[GRID_SIZE])
    ]

    UPDOWNGRIDLINE = " " * (NB_DIGITSINFOS + 2) \
        + "-" \
        + "".join([
            "-{0}-".format(letter)
            for letter in COLNAMES
        ]) \
        + "-"

    resetgrid()
    redrawgrid()

    playthegame()
