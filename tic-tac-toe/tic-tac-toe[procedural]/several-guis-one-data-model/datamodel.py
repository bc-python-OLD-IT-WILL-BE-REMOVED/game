# ---------------------- #
# -- SIZE OF THE GRID -- #
# ---------------------- #

GRID_SIZE = None

while GRID_SIZE is None:
    GRID_SIZE = input("Size of the grid (min 3 , max = 20): ")

    if not GRID_SIZE.isdigit():
        GRID_SIZE = None

    else:
        GRID_SIZE = int(GRID_SIZE)

        if not 3 <= GRID_SIZE <= 20:
            GRID_SIZE = None


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


def reset_game(actual_player, grid, grid_size, empty):
    actual_player = 0

    grid = {
        (row, col): empty
        for row in range(grid_size)
        for col in range(grid_size)
    }

    return actual_player, grid


def cell_can_be_played(grid, empty, row, col):
    return grid[row, col] == empty


def addtoken(grid, row, col, token):
    grid[row, col] = token

    return grid


def game_state(grid, grid_size, empty, coords_to_test):
# A winner ?
    for onetest in coords_to_test:
        total = sum([
            grid[row, col]
            for (row, col) in onetest
        ])

        if abs(total) == grid_size:
            return True, total // grid_size

# No more choice ?
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row, col] == empty:
                return False, None

# No more choice
    return True, None
