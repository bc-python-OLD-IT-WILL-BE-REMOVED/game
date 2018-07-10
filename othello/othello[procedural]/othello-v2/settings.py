# ---------------------- #
# -- COMMON CONSTANTS -- #
# ---------------------- #

EMPTY = None

# Little trick : 1 + 1 = 0 mod 2 , and 0 + 1 = 1 mod 2 make it easy
# to change the ID of the user who is playing.
USER_1, USER_2 = range(2)


GRID_SIZE = "grid_size"

PLAYER_ID     = "player_id"
PLAYERS       = "players"
PLAYERS_MODES = "players_modes"
PLAYING_GRID  = "playing_grid"

SCORES_BY_USER = "scores_by_user"

TOKENS_MAYBE_PLAYABLE   = "tokens_maybe_playable"
TOKENS_PLAYABLE_BY_USER = "tokens_playable_by_user"


GAME_STATE = {
    PLAYER_ID              : USER_1,
    PLAYERS                : [],
    TOKENS_MAYBE_PLAYABLE  : set(),
    TOKENS_PLAYABLE_BY_USER: { USER_1: {}, USER_2: {} },
    SCORES_BY_USER         : { USER_1: 0, USER_2: 0 }
}


def init(gridsize, players_modes):
    global GAME_STATE, \
           GRID_SIZE, PLAYERS_MODES, PLAYING_GRID

    GAME_STATE[GRID_SIZE]     = gridsize
    GAME_STATE[PLAYERS_MODES] = players_modes
    GAME_STATE[PLAYING_GRID]  = [
        [EMPTY for _ in range(gridsize)]
        for _ in range(gridsize)
    ]
