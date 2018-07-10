from collections import defaultdict
from random import choice

from settings import *


# ----------------------- #
# -- GENERAL FUNCTIONS -- #
# ----------------------- #

def thisistheendmyoldfriend():
    """
This function simply indicates if the game is finished or not.
    """
    global USER_1, USER_2, GAME_STATE, \
           TOKENS_PLAYABLE_BY_USER

    return (
        not GAME_STATE[TOKENS_PLAYABLE_BY_USER][USER_1]
        and
        not GAME_STATE[TOKENS_PLAYABLE_BY_USER][USER_2]
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
    global GAME_STATE, \
           GRID_SIZE

    return (
        0 <= rownb < GAME_STATE[GRID_SIZE]
        and
        0 <= colnb < GAME_STATE[GRID_SIZE]
    )


def addtoken(rownb, colnb, tokenid):
    """
This function adds a new token.

The variables `GAME_STATE[SCORES_BY_USER]` and `GAME_STATE[TOKENS_MAYBE_PLAYABLE]` are updated.
    """
    global EMPTY, GAME_STATE, \
           PLAYING_GRID, SCORES_BY_USER, TOKENS_MAYBE_PLAYABLE

    GAME_STATE[PLAYING_GRID][rownb][colnb] = tokenid

    if tokenid != EMPTY:
        GAME_STATE[SCORES_BY_USER][tokenid]   += 1

        for row in range(rownb - 1, rownb + 2):
            for col in range(colnb  - 1, colnb + 2):
                if isingrid(row, col):
                    coords = (row, col)

                    if GAME_STATE[PLAYING_GRID][row][col] == EMPTY:
                        GAME_STATE[TOKENS_MAYBE_PLAYABLE].add(coords)

                    else:
# We can't use here the method `remove`.
                        GAME_STATE[TOKENS_MAYBE_PLAYABLE] -= set([coords])


def switchtoken(rownb, colnb):
    """
This function only changes a token of one user to a token of the other user.

The variable `GAME_STATE[SCORES_BY_USER]` is updated.
    """
    global EMPTY, GAME_STATE, \
           PLAYING_GRID, SCORES_BY_USER

    tokenid = GAME_STATE[PLAYING_GRID][rownb][colnb]

    if tokenid == EMPTY:
        raise Exception("impossible to switch an empty cell")

    otherid = otheruser(tokenid)

    GAME_STATE[PLAYING_GRID][rownb][colnb] = otherid

    GAME_STATE[SCORES_BY_USER][tokenid] -= 1
    GAME_STATE[SCORES_BY_USER][otherid] += 1


def searchonedirection(rowtest, coltest, deltarow, deltacol, tokenid):
    """
This function looks at consecutive switchable tokens forward one direction.
    """
    global EMPTY, GAME_STATE, \
           PLAYING_GRID

    tokensfound = []

    while isingrid(rowtest, coltest):
        if GAME_STATE[PLAYING_GRID][rowtest][coltest] in [EMPTY, tokenid]:
            break

        tokensfound.append( (rowtest, coltest) )

        rowtest += deltarow
        coltest += deltacol

    if not isingrid(rowtest, coltest) \
    or GAME_STATE[PLAYING_GRID][rowtest][coltest] == EMPTY:
        tokensfound = []

    return tokensfound


def searchalldirections(rowstart, colstart, tokenid):
    """
This function looks for switchable tokens in all directions.
    """
    global EMPTY, GAME_STATE, \
           PLAYING_GRID, TOKENS_MAYBE_PLAYABLE

    tokensfound = []

    if (rowstart, colstart) in GAME_STATE[TOKENS_MAYBE_PLAYABLE]:
        for deltarow in range(-1, 2):
            rowtest = rowstart + deltarow

            for deltacol in range(-1, 2):
                coltest = colstart + deltacol

                if (deltarow, deltacol) != (0, 0) \
                and isingrid(rowtest, coltest) \
                and GAME_STATE[PLAYING_GRID][rowtest][coltest] not in [
                    EMPTY, tokenid
                ]:
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
    global GAME_STATE, \
           TOKENS_MAYBE_PLAYABLE, TOKENS_PLAYABLE_BY_USER

    GAME_STATE[TOKENS_PLAYABLE_BY_USER] = {
        USER_1: {},
        USER_2: {}
    }

    for row, col in GAME_STATE[TOKENS_MAYBE_PLAYABLE]:
        for tokenid in [USER_1, USER_2]:
            tokensfound = searchalldirections(
                rowstart = row,
                colstart = col,
                tokenid  = tokenid
            )

# One token can be playable by the two users.
            if tokensfound:
                GAME_STATE[TOKENS_PLAYABLE_BY_USER][tokenid][(row, col)] = tokensfound


def resetgrid():
    """
This function (re)sets the grid in the original organization.
    """
    global EMPTY, USER_1, USER_2, GAME_STATE, \
           GRID_SIZE, SCORES_BY_USER, TOKENS_MAYBE_PLAYABLE

    GAME_STATE[TOKENS_MAYBE_PLAYABLE] = set()

    GAME_STATE[SCORES_BY_USER] = {
        USER_1: 0,
        USER_2: 0
    }

    middle_next = GAME_STATE[GRID_SIZE] // 2
    middle      = middle_next - 1

    user_1_first_tokens = [(middle, middle), (middle_next, middle_next)]
    user_2_first_tokens = [(middle, middle_next), (middle_next, middle)]

    for rownb in range(GAME_STATE[GRID_SIZE]):
        for colnb in range(GAME_STATE[GRID_SIZE]):
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


def tokenschanged(coords):
    """
This function updates all tokens changed if the cell played has coordinates
`coords`.

The function returns all the taken changed.
    """
    global GAME_STATE, \
           PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    row, col = coords

    tokenfound = []

    if coords in GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]]:
        tokenfound.append(coords)
        addtoken(row, col, GAME_STATE[PLAYER_ID])

        for (row, col) in GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]][coords]:
            tokenfound.append( (row, col) )
            switchtoken(row, col)

    return tokenfound


# ---------------------- #
# -- PLAYER 1 : HUMAN -- #
# ---------------------- #

def player_human(row, col):
    """
`(row, col)` are coordinates of the cell choosen.which are directly returned
here because this is the choice of a human.
    """
    return (row, col)

# A decorator for the following wille be better (it is easy to do). I keep
# this ugly method just for pedagogical reasons.
GAME_STATE[PLAYERS].append(player_human)


# -------------------------- #
# -- PLAYER 2 : Stupid AI -- #
# -------------------------- #

def player_sai(row, col):
    """
`(row, col)` are coordinates of the cell choosen. There are not used by the AI.
This is just a way to seet the AI plays when the user clicks on the game.


This function returns the coordinate of a cell choosed randomly in the list
of playable cells.
    """
    global GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    return choice(
        list(
            GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]].keys()
        )
    )


GAME_STATE[PLAYERS].append(player_sai)


# -------------------------------------------- #
# -- PLAYER 3 : AI - BEST JUST AT THIS TIME -- #
# -------------------------------------------- #

def bestchoicenow():
    """
See the functions `player_ai_best_one_level` and `findbestchoicesdeeply`.
    """
    global GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    maxchanged = 0
    tochoose   = defaultdict(list)

    for new, changed in GAME_STATE[TOKENS_PLAYABLE_BY_USER][
        GAME_STATE[PLAYER_ID]
    ].items():
        nbchanged = len(changed)

        if nbchanged >= maxchanged:
            maxchanged = nbchanged

            tochoose[nbchanged].append(new)

    return maxchanged, tochoose[maxchanged]


def player_ai_best_one_level(row, col):
    """
`(row, col)` are coordinates of the cell choosen. There are not used by the AI.
This is just a way to seet the AI plays when the user clicks on the game.


This function uses is the following one.

    * We build a list of the tokens given most new tokens of our color.

    * We choose randomly one token in the previous list and we return its
      coordinates.


Indeed the first job is done by the function `bestchoicenow`.


info::
    This function prepares the job for the more general function
    `player_ai_best_three_levels` above.
    In other word we could have just write one single function for
    `player_ai_best_one_level` and `player_ai_best_three_levels`
    (this is a very easy exercise).
    """
    maxchanged, tochoose = bestchoicenow()

    print()
    print("BEST FOUND - ai_best_one_level")
    print(maxchanged, "tokens at", tochoose)

    return choice(tochoose)


GAME_STATE[PLAYERS].append(player_ai_best_one_level)


# -------------------------------------------- #
# -- PLAYER 4 : AI - MOST TOKENS ON 3 TURNS -- #
# -------------------------------------------- #

def findbestchoicesdeeply(level):
    """
This function implements the method for the AI programmed in the function
`player_ai_best_three_levels`.
    """
    global GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    maxchanged, totry = bestchoicenow()

    for coords in totry:
        print(coords)

    exit()

# Let's continue recursively... or not !
    level -= 1

    if level == 0:
        return totry

    else:
        findbestchoicesdeeply(level = level)


def player_ai_best_three_levels(row, col):
    """
`(row, col)` are coordinates of the cell choosen. There are not used by the AI.
This is just a way to seet the AI plays when the user clicks on the game.


This function uses is the following one.

    * We build a list of the tokens given most new tokens of our color if
      we simulate all the possibilities on three levels of the game. We have
      to take care of cases with two first moves not really interesting at
      a first glance but then very good with the third choice...

    * We choose randomly one token in the previous list and we return its
      coordinates.


Indeed the job is done by the recursive function `findbestchoicesdeeply`
(this allows to imagine depper search as soon as your computer can do
the search...).
    """
    bestchoices = findbestchoicesdeeply(level = 3)

    print()
    print("BEST FOUND - player_ai_best_three_levels")
    print(bestchoices)

    return choice(bestchoices)


GAME_STATE[PLAYERS].append(player_ai_best_three_levels)
