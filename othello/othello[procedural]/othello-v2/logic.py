from collections import defaultdict
from copy import deepcopy
from random import choice

from settings import *


# ----------------------- #
# -- GENERAL FUNCTIONS -- #
# ----------------------- #

def thisistheendmyoldfriend():
    """
This function simply indicates if the game is finished or not.
    """
    global USER_1, USER_2, \
           GAME_STATE, TOKENS_PLAYABLE_BY_USER

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
    global EMPTY, \
           GAME_STATE, PLAYING_GRID, SCORES_BY_USER, TOKENS_MAYBE_PLAYABLE

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
    global EMPTY, \
           GAME_STATE, PLAYING_GRID, SCORES_BY_USER

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
    global EMPTY, \
           GAME_STATE, PLAYING_GRID

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
    global EMPTY, \
           GAME_STATE, PLAYING_GRID, TOKENS_MAYBE_PLAYABLE

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
    global GAME_STATE, TOKENS_MAYBE_PLAYABLE, TOKENS_PLAYABLE_BY_USER

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
                GAME_STATE[TOKENS_PLAYABLE_BY_USER][tokenid][(row, col)] \
                = tokensfound


def updatetokens(newtokens):
    """
This function simply changes all the tokens indicated in the list `newtokens`,
and then it changes the ID of the player.
    """
    global GAME_STATE, PLAYING_GRID, PLAYER_ID

# Just for human(?) debugging...  -  START
    print("updatetokens :: newtokens :", newtokens)
    print("player_ai_best_three_levels :: grid BEFORE:")
    for row in GAME_STATE['playing_grid']:
        print(str(row).replace("None", "."))
# Just for human(?) debugging...  -  END

    player_id = GAME_STATE[PLAYER_ID]

    for (row, col) in newtokens:
        GAME_STATE[PLAYING_GRID][row][col] = player_id

    GAME_STATE[PLAYER_ID] = otheruser(player_id)

    findplayable()


def resetgrid():
    """
This function (re)sets the grid in the original organization.
    """
    global EMPTY, USER_1, USER_2, \
           GAME_STATE, GRID_SIZE, SCORES_BY_USER, TOKENS_MAYBE_PLAYABLE

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

    tokens_playable = GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]]

# Just for human(?) debugging...  -  START
    print("playthegame :: TOKENS_PLAYABLE_BY_USER : ", GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]])
# Just for human(?) debugging...  -  END

    if coords in tokens_playable:
        tokenfound.append(coords)
        addtoken(row, col, GAME_STATE[PLAYER_ID])

        for (row, col) in tokens_playable[coords]:
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

# Just for human(?) debugging...  -  START
    # print("grid:")
    # for row in GAME_STATE['playing_grid']:
    #     print(str(row).replace("None", "."))
# Just for human(?) debugging...  -  END

    return choice(
        list(
            GAME_STATE[TOKENS_PLAYABLE_BY_USER][GAME_STATE[PLAYER_ID]].keys()
        )
    )


GAME_STATE[PLAYERS].append(player_sai)


# -------------------------------------------- #
# -- PLAYER 3 : AI - BEST JUST AT THIS TIME -- #
# -------------------------------------------- #

def findbestcoords(cells_scores):
    """
????
    """
    bestscore  = -1
    bestcoords = defaultdict(list)

    for coords, score in cells_scores.items():
        if score >= bestscore:
            bestscore = score

            bestcoords[score].append(coords)

    return bestscore, bestcoords[bestscore]


def player_ai_best_one_level(row, col):
    """
`(row, col)` are coordinates of the cell choosen. There are not used by the AI.
This is just a way to seet the AI plays when the user clicks on the game.


This function uses is the following one.

    * We build a list of the tokens given most new tokens of our color.

    * We choose randomly one token in the previous list and we return its
      coordinates.
    """
    global GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER

    bestscore, coordstochoose = findbestcoords(
        cells_scores = {
            new: len(changed)
            for new, changed in GAME_STATE[TOKENS_PLAYABLE_BY_USER][
                GAME_STATE[PLAYER_ID]
            ].items()
        }
    )

    print()
    print("BEST FOUND - ai_best_one_level")
    print(bestscore, "tokens at", coordstochoose)

    return choice(coordstochoose)


GAME_STATE[PLAYERS].append(player_ai_best_one_level)


# -------------------------------------------- #
# -- PLAYER 4 : AI - MOST TOKENS ON 3 TURNS -- #
# -------------------------------------------- #

def recusearchforscores(level, initial_player_id):
    """
This function implements the method for the AI corresponding to the function
`player_ai_best_three_levels`.


warning::
    We must have `level > 0` the first time the funcion is called.
    """
    global GAME_STATE, PLAYER_ID, TOKENS_PLAYABLE_BY_USER

# Just for human(?) debugging...  -  START
    # print("level =", level, "grid:")
    # for row in GAME_STATE['playing_grid']:
    #     print(str(row).replace("None", "."))
# Just for human(?) debugging...  -  END

# We just return the current scores.
    if level == 0:
        scores = {
            None: GAME_STATE[SCORES_BY_USER][initial_player_id]
        }

# Let's try all and investigate recursively...
    else:
        player_id   = GAME_STATE[PLAYER_ID]
        the_players = GAME_STATE[PLAYERS]

        scores = {}

        for (row, col) in GAME_STATE[TOKENS_PLAYABLE_BY_USER][player_id]:
# We must store actual GAME_STATE so as to restore it just after the job
# will been done recursively.
            lastgamestate = deepcopy(GAME_STATE)

            updatetokens(
                newtokens = tokenschanged(
                    the_players[player_id](
                        row = row,
                        col = col
                    )
                )
            )

            bestscore, _ = findbestcoords(
                cells_scores = recusearchforscores(
                    level             = level - 1,
                    initial_player_id = initial_player_id
                )
            )

            scores[(row, col)] = bestscore

            GAME_STATE = deepcopy(lastgamestate)

# Scores calculated.
    return scores


def player_ai_best_three_levels(row, col):
    """
`(row, col)` are coordinates of the cell choosen. There are not used by the AI.
This is just a way to seet the AI plays when the user clicks on the game.


This function uses is the following one.

    * We build a list of the tokens with their score. This score is calculated
      by taking the most tokens won after three turns
      ((
        We could also have evaluted means, or works with the best and the worst
        numbers of tokens won... There are ither choices possible.
      )).

    * We build a list of the tokens with the best score.

    * We choose randomly one token in the previous list and we return its
      coordinates.


This tactic tries to take care of cases with two first moves not very
interesting at a first glance but that are very useful with a good third
choice...


info::
    Most of the job is done by the recursive function `recusearchforscores`
    (this allows to imagine depper search as long as your computer can seek).
    """
    global GAME_STATE, PLAYER_ID

    print("player_ai_best_three_levels :: id BEFORE -", GAME_STATE[PLAYER_ID])
# Just for human(?) debugging...  -  START
    print("player_ai_best_three_levels :: grid BEFORE:")
    for row in GAME_STATE['playing_grid']:
        print(str(row).replace("None", "."))
# Just for human(?) debugging...  -  END

    lastgamestate = deepcopy(GAME_STATE)

    bestscore, coordstochoose = findbestcoords(
        cells_scores = recusearchforscores(
            level             = 3,
            initial_player_id = GAME_STATE[PLAYER_ID]
        )
    )

    GAME_STATE = deepcopy(lastgamestate)

    print("player_ai_best_three_levels :: id AFTER -", GAME_STATE[PLAYER_ID])
# Just for human(?) debugging...  -  START
    print("player_ai_best_three_levels :: grid AFTER:")
    for row in GAME_STATE['playing_grid']:
        print(str(row).replace("None", "."))
# Just for human(?) debugging...  -  END
    print()
    print("BEST FOUND - player_ai_best_three_levels", choice(coordstochoose))
    print(bestscore, "tokens at", coordstochoose)
    print("?", choice(coordstochoose))

    return choice(coordstochoose)


GAME_STATE[PLAYERS].append(player_ai_best_three_levels)
