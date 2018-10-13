from mistool.os_use import PPath as Path


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent
PYFILE   = THIS_DIR / "tictactoe-nolist-nofonction.py"

PYCODE = []

TAB = []

for shift in range(4, 17, 4):
    TAB.append(" "*shift)


# ----------- #
# -- TOOLS -- #
# ----------- #

def celltext(col, row):
    return "CELL_{col}{row}".format(
        col = col,
        row = row
    )


# ---------------------------------------------------- #
# -- ONE VARIABLE FOR EACH CELL... IS THIS A JOKE ? -- #
# ---------------------------------------------------- #

SYMBOLS = {
    -1: "×",
    1 : "o",
    0 : " "
}

PYCODE += [
    """
# --------------- #
# -- CONSTANTS -- #
# --------------- #

#  - 1 = ×  |  0 = empty  |  1 = o

PLAYER_ID = - 1

#  Columns:       A     B     C
#
#  Rows   :  1    .  |  .  |  .
#               -----------------
#            2    .  |  .  |  .
#               -----------------
#            3    .  |  .  |  .
    """.strip(),
    ""
]

for col in "ABC":
    for row in range(1, 4):
        PYCODE.append(
            "{cell} = 0".format(
                cell = celltext(col, row)
            )
        )


# ------------------------- #
# -- MAIN LOOP - [START] -- #
# ------------------------- #

PYCODE += [
    "",
    "",
    """
# --------------- #
# -- MAIN LOOP -- #
# --------------- #

while True:
    """.strip()
]


# -- LET'S PRINT THE GRID -- #

PYCODE.append("""
# Let's print the grid.
{tab[0]}print()
    """.lstrip().format(tab = TAB)
)

print_template = """
{tab[0]}if {cell} == - 1:
{tab[1]}print(" ×", end = "")
{tab[0]}elif {cell} == 1:
{tab[1]}print(" o", end = "")
{tab[0]}else:
{tab[1]}print("  ", end = "")
""".strip()

for row in range(1, 4):
    for col in "ABC":
        PYCODE += [
            print_template.format(
               tab  = TAB,
               cell = celltext(col, row)
            ),
            ""
        ]

        if col != "C":
            PYCODE += ["""
{tab[0]}print(" |", end = "")
            """.strip().format(tab = TAB),
            ""
        ]

    PYCODE.append(
        "{tab[0]}print()".format(tab = TAB),
    )


    if row != 3:
        PYCODE += [
            "{tab[0]}print('-'*11)".format(tab = TAB),
            ""
        ]


# -- END OF THE GAME -- #

PYCODE.append(
    """
# The game is finished.
    """.rstrip())

#  - 1 = ×  |  0 = empty  |  1 = o
ifstatement = "if"

for token in [-1, 1]:
    symbol = SYMBOLS[token]

    wintests = []

    if token == 1:
        sign = "-"

    else:
        sign = "+"

    for iter_1, iter_2, swap in [
        (range(1, 4), "ABC", True),
        ("ABC", range(1, 4), False),
    ]:
        for x in iter_1:
            one_winning_test = []

            for y in iter_2:
                if swap:
                    col, row = y, x

                else:
                    col, row = x, y

                one_winning_test.append(
                    celltext(col, row)
                )

            wintests.append(
                "({addition} {sign} 3)".format(
                    addition = " + " .join(one_winning_test),
                    sign = sign
                )
            )

    for iter_1, iter_2 in [
        ("ABC", range(1, 4)),
        ("ABC", range(3, 0, -1)),
    ]:
        one_winning_test = []

        for x, y in zip(iter_1, iter_2):
            one_winning_test.append(
                celltext(col = x, row = y)
            )

        wintests.append(
            "({addition} {sign} 3)".format(
                addition = " + " .join(one_winning_test),
                sign = sign
            )
        )

    wintests = " * ".join(wintests)

    PYCODE.append(
        """
{tab[0]}{ifstatement} {wintests} == 0:
{tab[1]}print()
{tab[1]}print("Player with [ {symbol} ] wins.")
{tab[1]}break
        """.lstrip().format(
            tab         = TAB,
            ifstatement = ifstatement,
            wintests    = wintests,
            symbol      = symbol
        )
    )

    ifstatement = "elif"


factors = [
    celltext(col, row)
    for col in "ABC"
    for row in range(1, 4)
]

product = " * ".join(factors)

PYCODE.append(
    """
{tab[0]}elif {product} != 0:
{tab[1]}print()
{tab[1]}print("No one wins.")
{tab[1]}break
    """.lstrip().format(
        tab     = TAB,
        product = product
    )
)


# -- WE CAN PLAY -- #

PYCODE.append(
    """
# We can play...",
    else:
    """.strip()
)


# -- THE PLAYER HAS TO PLAY -- #

goodchoice_temp = """
{tab[2]}{ifstatement} choice == \"{col}{row}\" and {cell} == 0:
{tab[3]}{cell} = PLAYER_ID
{tab[3]}bad_answer = False
""".strip()

goodchoices = []

goodchoices = [
    goodchoice_temp.format(
            tab         = TAB,
            ifstatement = "if" if col == "A" and row == 1 else "elif",
            col         = col,
            row         = row,
            cell        = celltext(col, row)
        )
    for col in "ABC"
    for row in range(1, 4)
]

goodchoices = "\n\n".join(goodchoices)

PYCODE.append(
    """
{tab[1]}print()

        bad_answer = True

        while bad_answer:
            if PLAYER_ID == 1:
                choice = input("Player with [ o ], what is your choice ? Use A1 or B3 for example : ")

            else:
                choice = input("Player with [ × ], what is your choice ? Use A1 or B3 for example : ")

{goodchoices}
    """.strip().format(
        tab         = TAB,
        goodchoices = goodchoices)
)


# -- THE PLAYER CHANGES -- #

PYCODE.append(
    """
# The player changes.
        PLAYER_ID = -PLAYER_ID
    """.rstrip()
)


# ----------------------- #
# -- MAIN LOOP - [END] -- #
# ----------------------- #

PYCODE = "\n".join(PYCODE)


# ------------------------- #
# -- PYFILE CAN BE BUILD -- #
# ------------------------- #

with open(
    file     = PYFILE,
    mode     = "w",
    encoding = "utf8"
) as pyfile:
    pyfile.write(PYCODE)
