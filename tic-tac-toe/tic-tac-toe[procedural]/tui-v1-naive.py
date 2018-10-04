# --------------- #
# -- CONSTANTS -- #
# --------------- #

CROSS, DISK, EMPTY = "×", "o", " "

PLAYERS = [CROSS, DISK]

HRULE = "-"*(3*3 + 2)

GRID = None


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #


def reset_grid():
    global GRID

    GRID = [
        [EMPTY for _ in range(3)]
        for _ in range(3)
    ]


def cell_can_be_played(row, col):
    return GRID[row][col] == EMPTY


def addtoken(row, col, token):
    GRID[row][col] = token


def single_token_found(tokens):
    global EMPTY

    singletoken = None

    if len(tokens) == 1:
        singletoken = list(tokens)[0]

    return singletoken


def gamefinished():
    global GRID

# A winner ?
    for nb in range(3):
# Vertical test.
        oneline_tokens = set([
            GRID[nb][cell]
            for cell in range(3)
        ])

        singletoken = single_token_found(oneline_tokens)

        if singletoken in PLAYERS:
            return True, singletoken

# Horizontal test.
        oneline_tokens = set([
            GRID[cell][nb]
            for cell in range(3)
        ])

        singletoken = single_token_found(oneline_tokens)

        if singletoken in PLAYERS:
            return True, singletoken

# Diagonal LU-2-RD test.
    oneline_tokens = set([
        GRID[nb][nb]
        for nb in range(3)
    ])

    singletoken = single_token_found(oneline_tokens)

    if singletoken in PLAYERS:
        return True, singletoken

# Diagonal LD-2-RU test.
    oneline_tokens = set([
        GRID[2 - nb][nb]
        for nb in range(3)
    ])

    singletoken = single_token_found(oneline_tokens)

    if singletoken in PLAYERS:
        return True, singletoken

# No more choice ?
    for row in range(3):
        for col in range(3):
            if GRID[row][col] != EMPTY:
                return False, None

    return True, None


# --------- #
# -- TUI -- #
# --------- #

def printgrid():
    global GRID

    for row in range(3):
        print(" " + " | ".join(GRID[row]) + " ")

        if row != 2:
            print(HRULE)

def main():
    reset_grid()

    actual_player = 0

    print()
    printgrid()

    while True:
        print()
        print("PLAYER ", actual_player + 1, "plays with", PLAYERS[actual_player])

        while True:
            answer = input("#row, #column (numbers between 1 and 2):")

            answer = answer.split(",")

            if len(answer) != 2:
                print("Too much colons....")
                continue

            row, col = answer

            if not row.isdigit() or not col.isdigit():
                print("Bad number formats...")
                continue

            row, col = int(row) - 1, int(col) - 1

            if not 0 <= row <= 2 or not 0 <= col <= 2:
                print("Numbers not in {1, 2, 3}...")
                continue

            if not cell_can_be_played(row, col):
                print("Cell contains a", GRID[row][col], "token...")
                continue

            break

        addtoken(row, col, PLAYERS[actual_player])
        printgrid()

        endofgame, winningtoken = gamefinished()

        if endofgame:
            if winningtoken == None:
                print("Noone wins...")

            else:
                print("PLAYER ", actual_player + 1, "playing with", PLAYERS[actual_player], "has won.")

            break

        actual_player += 1
        actual_player %= 2


# ------------------- #
# -- LET'S PLAY... -- #
# ------------------- #

main()
