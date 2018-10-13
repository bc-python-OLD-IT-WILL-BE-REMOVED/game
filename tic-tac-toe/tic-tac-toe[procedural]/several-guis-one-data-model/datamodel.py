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

CROSS, EMPTY, DISK = range(-1, 2)

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0

GRID = None


# --------------- #
# -- FOR TESTS -- #
# --------------- #

COORDS_TO_TEST = []

for row in range(GRID_SIZE):
    COORDS_TO_TEST.append([
        (row, col)
        for col in range(GRID_SIZE)
    ])

    COORDS_TO_TEST.append([
        (col, row)
        for col in range(GRID_SIZE)
    ])

COORDS_TO_TEST.append([
    (row, row)
    for row in range(GRID_SIZE)
])

COORDS_TO_TEST.append([
    (GRID_SIZE - row - 1, row)
    for row in range(GRID_SIZE)
])


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #

def nextplayer(actual_player):
    actual_player += 1
    actual_player %= 2

    return actual_player


def reset_game(actual_player, grid):
    global GRID_SIZE, EMPTY

    actual_player = 0

    grid = {
        (row, col): EMPTY
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
    }

    return actual_player, grid


def cell_can_be_played(grid, row, col):
    global GRID_SIZE, EMPTY

    return grid[row, col] == EMPTY


def addtoken(grid, row, col, token):
    grid[row, col] = token

    return grid


def game_state(grid):
    global GRID_SIZE, EMPTY, COORDS_TO_TEST

# True : someone wins.
# None : noone wins.
# False: next player can play.

# A winner ?
    for onetest in COORDS_TO_TEST:
        total = sum([
            grid[row, col]
            for (row, col) in onetest
        ])

        if abs(total) == GRID_SIZE:
            return True

# No more choice ?
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col] == EMPTY:
                return False

# No more choice
    return None
