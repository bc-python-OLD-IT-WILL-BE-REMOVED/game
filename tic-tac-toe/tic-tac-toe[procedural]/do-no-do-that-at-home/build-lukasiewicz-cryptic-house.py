import re

import sympy

from mistool.os_use import PPath as Path


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent
OLD_PYFILE   = THIS_DIR / "tictactoe-nolist-nofonction.py"
NEW_PYFILE   = THIS_DIR / "tictactoe-nolist-nofonction-cryptified.py"

TAB = []

for shift in range(4, 17, 4):
    TAB.append(" "*shift)

# ------------------- #
# -- ORIGINAL CODE -- #
# ------------------- #

with open(
    file     = OLD_PYFILE,
    mode     = "r",
    encoding = "utf8"
) as pyfile:
    PYCODE = pyfile.read()


# ------------------------------------------- #
# -- CRYPTIC NAME FOR THE ID OF THE PLAYER -- #
# ------------------------------------------- #

PYCODE = PYCODE.replace(
    "#  - 1 = ×  |  0 = empty  |  1 = o",
    """
#  x indicates the id of the player using the following conventions :
#
#  - 1 = ×  |  0 = empty  |  1 = o
    """.strip()
)

PYCODE = PYCODE.replace("PLAYER_ID", "x")

PYCODE = PYCODE.replace(
    "x = - 1",
    """
x = - 1

# Some useful  texts.

{declarations}

# Some usefus shortcurts.

{shortcuts}
    """.strip()
)


# ----------------------------- #
# -- CRYPTIC NAMES FOR CELLS -- #
# ----------------------------- #

PYCODE = PYCODE.replace(
    "#  Columns:       A     B     C",
    "# Codification of the grid"
)

PYCODE = PYCODE.replace(
    "#               -----------------",
    "# -----------------"
)

PYCODE = PYCODE.replace(
    "#  Rows   :  1    .  |  .  |  .",
    "#   a  |  b  |  c"
)

PYCODE = PYCODE.replace(
    "#            2    .  |  .  |  .",
    "#   d  |  e  |  f"
)

PYCODE = PYCODE.replace(
    "#            3    .  |  .  |  .",
    "#   g  |  h  |  i"
)

letters = list("abcdefghi")[::-1]

for col in "ABC":
    for row in range(1, 4):
        old_name = "CELL_{col}{row}".format(
            col = col,
            row = row
        )

        new_name = letters.pop()

        PYCODE = PYCODE.replace(old_name, new_name)


# ----------------------------------- #
# -- SHORTCUTS FOR LON THINKING... -- #
# ----------------------------------- #

shortcuts = []

for std, short in {
    "False": "y",
    "True" : "z",
    "input": "_i_",
    "print": "_onl_",
    "lambda x: print(x, end = '')": "_ononl_",
}.items():
    PYCODE = PYCODE.replace(std, short)

    shortcuts.append(
        "{name} = {val}".format(
            name = short,
            val  = std
        )
    )

shortcuts = "\n".join(shortcuts)


# ------------------------ #
# -- USE OF ``_ononl_`` -- #
# ------------------------ #

pattern = re.compile('_onl_\((.+), end = ""\)')

match = True

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        PYCODE = "{start}_ononl_({text}){end}".format(
            start = PYCODE[:match.start()],
            text  = match.group(1),
            end   = PYCODE[match.end():]
        )


# ---------------------- #
# -- CRYPTIC MESSAGES -- #
# ---------------------- #

old_messages = [
    '"  "',
    '" |"',
    "'-'*11",
    '" ×"',
    '" o"',
    '"Player with [ × ] wins."',
    '"Player with [ o ] wins."',
    '"No one wins."',
    '"Player with [ o ], what is your choice ? Use A1 or B3 for example : "',
    '"Player with [ × ], what is your choice ? Use A1 or B3 for example : "'
]

declarations = []

for i, old_text in enumerate(old_messages):
    new_var = "t" +str(i)

    PYCODE = PYCODE.replace(old_text, new_var)

    declarations.append(
        "{name} = {text}".format(
            name = new_var,
            text = old_text
        )
    )

declarations = "\n".join(declarations)

PYCODE = PYCODE.format(
    declarations = declarations,
    shortcuts    = shortcuts
)


# --------------------------------------- #
# -- CRYPTIC NAMES FOR OTHER VARIABLES -- #
# --------------------------------------- #

for old_name, new_name in {
    "bad_answer": "j",
    "choice"    : "k"
}.items():
    PYCODE = PYCODE.replace(old_name, new_name)


# ------------------------------------ #
# -- CRYPTIC NAMES FOR CRYPTIC SUMS -- #
# ------------------------------------ #

PYCODE = PYCODE.replace(
    "# The game is finished.",
    """
# Some usefus sums.
{declarations}
    """.strip()
)

declarations = []
newvarssum   = []

for i, sum in enumerate([
    "a + d + g",
    "b + e + h",
    "c + f + i",
    "a + b + c",
    "d + e + f",
    "g + h + i",
    "a + e + i",
    "c + e + g"
]):
    newvar = "s" + chr(97 + i)
    newvarssum.append(newvar)

    PYCODE = PYCODE.replace(sum, newvar)

    declarations.append("{0} = {1}".format(newvar, sum))


declarations = "\n".join(
    "{tab[0]}{newvar}".format(
        tab    = TAB,
        newvar = newvar
    )
    for newvar in declarations
) + "\n"

PYCODE = PYCODE.format(declarations = declarations)


# ------------------------------------- #
# -- CRYPTIFICATION OF THE SUM TESTS -- #
# ------------------------------------- #

for old_sum_test in [
    "(sa + 3) * (sb + 3) * (sc + 3) * (sd + 3) * (se + 3) * (sf + 3) * (sg + 3) * (sh + 3)",
    "(sa - 3) * (sb - 3) * (sc - 3) * (sd - 3) * (se - 3) * (sf - 3) * (sg - 3) * (sh - 3)"
]:
    for newvar in newvarssum:
        sympy.var(newvar)

    test = eval(old_sum_test)

    PYCODE = PYCODE.replace(old_sum_test, str(test.expand()))


# ---------------------------------------- #
# -- CRYPTIFICATION OF THE PRODUCT TEST -- #
# ---------------------------------------- #

old_test = "a * b * c * d * e * f * g * h * i != 0"

new_test = "2"

for oneletter in "abcdefghi":
    new_test = "({0})**{1}".format(new_test, oneletter)

new_test = new_test + " != 1"

PYCODE = PYCODE.replace(old_test, new_test)


# --------------------------- #
# -- MISC. CRYPTIFICATIONS -- #
# --------------------------- #

PYCODE = PYCODE.replace("x = -x", "x = ~x+1")


# ------------------------- #
# -- PYFILE CAN BE BUILD -- #
# ------------------------- #

with open(
    file     = NEW_PYFILE,
    mode     = "w",
    encoding = "utf8"
) as pyfile:
    pyfile.write(PYCODE)
