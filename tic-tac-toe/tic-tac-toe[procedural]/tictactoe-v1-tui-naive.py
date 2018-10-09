# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

CROSS, DISK, EMPTY = "×", "o", " "

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0

GRID = None


# ------------------- #
# -- TUI CONSTANTS -- #
# ------------------- #

HRULE = "-"*(3*3 + 2)


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #

def nextplayer():
    global ACTUAL_PLAYER

    ACTUAL_PLAYER += 1
    ACTUAL_PLAYER %= 2


def reset_game():
    global ACTUAL_PLAYER, GRID, EMPTY

    ACTUAL_PLAYER = 0

    GRID = [
        [EMPTY for _ in range(3)]
        for _ in range(3)
    ]


def cell_can_be_played(row, col):
    global GRID, EMPTY

    return GRID[row][col] == EMPTY


def addtoken(row, col, token):
    global GRID

    GRID[row][col] = token


def single_token_found(tokens):
    singletoken = None

    if len(tokens) == 1:
        singletoken = list(tokens)[0]

    return singletoken


def game_state():
    global GRID, PLAYERS, EMPTY

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
            if GRID[row, col] == EMPTY:
                return False, None

# No more choice
    return True, None


# --------- #
# -- TUI -- #
# --------- #

def update_grid_drawn():
    global GRID, HRULE

    for row in range(3):
        print(" " + " | ".join(GRID[row]) + " ")

        if row != 2:
            print(HRULE)


def validate_answer(answer):
    global GRID

    badanswer = (True, None, None)

    answer = answer.split(",")

    if len(answer) != 2:
        print("Too much colons....")
        return badanswer

    row, col = answer

    if not row.isdigit() or not col.isdigit():
        print("Bad number formats...")
        return badanswer

    row, col = int(row) - 1, int(col) - 1

    if not 0 <= row <= 2 or not 0 <= col <= 2:
        print("Numbers not in {1, 2, 3}...")
        return badanswer

    if not cell_can_be_played(row, col):
        print("Cell contains a", GRID[row][col], "token...")
        return badanswer

    return False, row, col


def main():
    global PLAYERS, ACTUAL_PLAYER

    reset_game()

    print()
    update_grid_drawn()

    while True:
        print()
        print("PLAYER", ACTUAL_PLAYER + 1, "plays with", PLAYERS[ACTUAL_PLAYER])

        badanswer = True

        while badanswer:
            answer = input("#row, #column (numbers between 1 and 2):")

            badanswer, row, col = validate_answer(answer)

        addtoken(row, col, PLAYERS[ACTUAL_PLAYER])
        update_grid_drawn()

        endofgame, winningtoken = game_state()

        if endofgame:
            if winningtoken == None:
                print("No one wins...")

            else:
                print("PLAYER", ACTUAL_PLAYER + 1, "playing with", PLAYERS[ACTUAL_PLAYER], "has won.")

            break

        nextplayer()


# ------------------- #
# -- LET'S PLAY... -- #
# ------------------- #

main()
