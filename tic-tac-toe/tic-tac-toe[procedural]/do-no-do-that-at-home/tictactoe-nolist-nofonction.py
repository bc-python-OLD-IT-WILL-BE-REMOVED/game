# --------------- #
# -- CONSTANTS -- #
# --------------- #

#  - 1 = ×  |  0 = empty  |  1 = o

PLAYER_ID = - 1

#  Columns:       A     B     C
#  Rows   :  1    .  |  .  |  .
#               -----------------
#            2    .  |  .  |  .
#               -----------------
#            3    .  |  .  |  .

CELL_A1 = 0
CELL_A2 = 0
CELL_A3 = 0
CELL_B1 = 0
CELL_B2 = 0
CELL_B3 = 0
CELL_C1 = 0
CELL_C2 = 0
CELL_C3 = 0


# --------------- #
# -- MAIN LOOP -- #
# --------------- #

while True:
# Let's print the grid.
    print()
    
    if CELL_A1 == - 1:
        print(" ×", end = "")
    elif CELL_A1 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_B1 == - 1:
        print(" ×", end = "")
    elif CELL_B1 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_C1 == - 1:
        print(" ×", end = "")
    elif CELL_C1 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print()
    print('-'*11)

    if CELL_A2 == - 1:
        print(" ×", end = "")
    elif CELL_A2 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_B2 == - 1:
        print(" ×", end = "")
    elif CELL_B2 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_C2 == - 1:
        print(" ×", end = "")
    elif CELL_C2 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print()
    print('-'*11)

    if CELL_A3 == - 1:
        print(" ×", end = "")
    elif CELL_A3 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_B3 == - 1:
        print(" ×", end = "")
    elif CELL_B3 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print(" |", end = "")

    if CELL_C3 == - 1:
        print(" ×", end = "")
    elif CELL_C3 == 1:
        print(" o", end = "")
    else:
        print("  ", end = "")

    print()

# The game is finished.
    if (CELL_A1 + CELL_B1 + CELL_C1 + 3) * (CELL_A2 + CELL_B2 + CELL_C2 + 3) * (CELL_A3 + CELL_B3 + CELL_C3 + 3) * (CELL_A1 + CELL_A2 + CELL_A3 + 3) * (CELL_B1 + CELL_B2 + CELL_B3 + 3) * (CELL_C1 + CELL_C2 + CELL_C3 + 3) * (CELL_A1 + CELL_B2 + CELL_C3 + 3) * (CELL_A3 + CELL_B2 + CELL_C1 + 3) == 0:
        print()
        print("Player with [ × ] wins.")
        break
        
    elif (CELL_A1 + CELL_B1 + CELL_C1 - 3) * (CELL_A2 + CELL_B2 + CELL_C2 - 3) * (CELL_A3 + CELL_B3 + CELL_C3 - 3) * (CELL_A1 + CELL_A2 + CELL_A3 - 3) * (CELL_B1 + CELL_B2 + CELL_B3 - 3) * (CELL_C1 + CELL_C2 + CELL_C3 - 3) * (CELL_A1 + CELL_B2 + CELL_C3 - 3) * (CELL_A3 + CELL_B2 + CELL_C1 - 3) == 0:
        print()
        print("Player with [ o ] wins.")
        break
        
    elif CELL_A1 * CELL_A2 * CELL_A3 * CELL_B1 * CELL_B2 * CELL_B3 * CELL_C1 * CELL_C2 * CELL_C3 != 0:
        print()
        print("No one wins.")
        break
    
# We can play...",
    else:
        print()

        bad_answer = True

        while bad_answer:
            if PLAYER_ID == 1:
                choice = input("Player with [ o ], what is your choice ? Use A1 or B3 for example : ")

            else:
                choice = input("Player with [ × ], what is your choice ? Use A1 or B3 for example : ")

            if choice == "A1" and CELL_A1 == 0:
                CELL_A1 = PLAYER_ID
                bad_answer = False

            elif choice == "A2" and CELL_A2 == 0:
                CELL_A2 = PLAYER_ID
                bad_answer = False

            elif choice == "A3" and CELL_A3 == 0:
                CELL_A3 = PLAYER_ID
                bad_answer = False

            elif choice == "B1" and CELL_B1 == 0:
                CELL_B1 = PLAYER_ID
                bad_answer = False

            elif choice == "B2" and CELL_B2 == 0:
                CELL_B2 = PLAYER_ID
                bad_answer = False

            elif choice == "B3" and CELL_B3 == 0:
                CELL_B3 = PLAYER_ID
                bad_answer = False

            elif choice == "C1" and CELL_C1 == 0:
                CELL_C1 = PLAYER_ID
                bad_answer = False

            elif choice == "C2" and CELL_C2 == 0:
                CELL_C2 = PLAYER_ID
                bad_answer = False

            elif choice == "C3" and CELL_C3 == 0:
                CELL_C3 = PLAYER_ID
                bad_answer = False

# The player changes.
        PLAYER_ID = -PLAYER_ID