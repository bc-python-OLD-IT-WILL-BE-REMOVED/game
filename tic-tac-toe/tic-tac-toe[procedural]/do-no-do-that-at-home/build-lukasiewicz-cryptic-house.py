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
# Some useful shortcuts.

{shortcuts}

# Some useful texts. We use UNICODE codification because all programers know it.

{declarations}

#  x indicates the id of the player using the following conventions :
#
#  - 1 = ×  |  0 = empty  |  1 = o
    """.rstrip()
)

PYCODE = PYCODE.replace("PLAYER_ID", "x")


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
    "#   g  |  h  |  i\n#"
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

PYCODE = PYCODE.replace("x = -x", "x = ~x + 1")

SHORTCUTS = {
    "-1"                          : "_",
    "0"                           : "__",
    "11"                          : "____",
    "1"                           : "___",
    "True"                        : "z",
    "False"                       : "y",
    "input"                       : "_i_",
    "print"                       : "_onl_",
    "lambda x: print(x, end = '')": "_ononl_",
}

shortcuts = []

for std, short in SHORTCUTS.items():
    if not std.isdigit() and std != "-1":
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

PYCODE = PYCODE.replace(
    "# Let's _onl_ the grid.",
    "# Let's print the grid."
)


# ---------------------- #
# -- CRYPTIC MESSAGES -- #
# ---------------------- #

old_messages = [
    '"  "',
    '" |"',
    '"-"*11',
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


# --------------------------------------- #
# -- CRYPTIC NAMES FOR OTHER VARIABLES -- #
# --------------------------------------- #

for old_name, new_name in {
    "bad_answer": "j",
    "choice"    : "k"
}.items():
    PYCODE = PYCODE.replace(old_name, new_name)


# -------------------------------------------------- #
# -- ONE LINERS FOR ``IF ... ELIF ... ELSE ...``  -- #
# -------------------------------------------------- #

pattern = re.compile(
    'if ([a-i] == -1):\s+(_ononl_\(t[0-9]\))\s+'
    +
    'elif ([a-i] == 1):\s+(_ononl_\(t[0-9]\))\s+'
    +
    'else:\s+(_ononl_\(t[0-9]\))'
)

match = True

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        onlinetest = "{0} if {1} else {2} if {3} else {4}".format(
            match.group(2),
            match.group(1),
            match.group(4),
            match.group(3),
            match.group(5),
        )

        PYCODE = "{start}{text}{end}".format(
            start = PYCODE[:match.start()],
            text  = onlinetest,
            end   = PYCODE[match.end():]
        )


# ---------------------------------------------- #
# -- ONE LINERS FOR SOME ``IF ... ELSE ...``  -- #
# ---------------------------------------------- #

pattern = re.compile(
    'if x == 1:\s+k = (.*)\s+'
    +
    'else:\s+k = (.*)'
)

match = True

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        onlinetest = "k = {0} if x == 1 else {1}".format(
            match.group(1),
            match.group(2),
        )

        PYCODE = "{start}{text}{end}".format(
            start = PYCODE[:match.start()],
            text  = onlinetest,
            end   = PYCODE[match.end():]
        )


# ------------------------------------------------------------------ #
# -- ONE LINERS FOR THE VERY LAST ``IF ... ELIF ... ELIF ...``  -- #
# ------------------------------------------------------------------ #

pattern = re.compile(
    '(el)*if (k == .*):\s+(.*)\s+(.*)\s+'
)

match = True
start = None

ifstatements = []

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        if start is None:
            start = PYCODE[:match.start()]

        names  = []
        values = []

        for i in range(3, 5):
            var, val = [x.strip() for x in match.group(i).split("=")]

            names.append(var)
            values.append(val)

        definition = '("{0}", "{1}")'.format(
            names[0],
            names[1],
            values[0],
            values[1],
        )

        ifstatements.append((
            match.group(2), definition
        ))

        PYCODE = PYCODE[match.end():]


onelineif = ""

for test, varstochange in ifstatements:
    onelineif += "{0} if {1} else ".format(
        varstochange,
        test
    )

onelineif = """
{tab[2]}nv1, nv2 = {onelineif}BUG
{tab[2]}vars()[nv1], vars()[nv2] = x, y

""".format(
    tab       = TAB,
    onelineif = onelineif
)

PYCODE = start + onelineif + PYCODE


# ------------------------------------ #
# -- CRYPTIC NAMES FOR CRYPTIC SUMS -- #
# ------------------------------------ #

PYCODE = PYCODE.replace(
    "# The game is finished.",
    """
# Some usefus sums.
{sum_declarations}
    """.strip()
)

sum_declarations = []
newvarssum       = []

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

    sum_declarations.append("{0} = {1}".format(newvar, sum))


sum_declarations = "\n".join(
    "{tab[0]}{newvar}".format(
        tab    = TAB,
        newvar = newvar
    )
    for newvar in sum_declarations
) + "\n"


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


# -------------------------- #
# -- LAST CRYPTIFICATIONS -- #
# -------------------------- #

PYCODE = PYCODE.replace(
    """
a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
g = 0
h = 0
i = 0
    """.strip(),
    "a = b = c = d = e = f = g = h = i = 0"
)

for std, short in SHORTCUTS.items():
    if std.isdigit() or std == "-1":
        for before in ["= ", "*", "+ "]:
            PYCODE       = PYCODE.replace(before + std, before + short)
            declarations = declarations.replace(before + std, before + short)


# -------------------------- #
# -- CLEANING EMPTY LINES -- #
# -------------------------- #

pattern = re.compile('\n[ \t]*\n')

match = True

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        PYCODE = "{start}{text}{end}".format(
            start = PYCODE[:match.start()],
            text  = "\n",
            end   = PYCODE[match.end():]
        )


# --------------------------------- #
# -- INSERT CRYPTIC DECLARATIONS -- #
# --------------------------------- #

PYCODE = PYCODE.format(
    declarations     = declarations,
    shortcuts        = shortcuts,
    sum_declarations = sum_declarations
)


# ------------------------------ #
# -- CRYPTIFICATIONS OF TEXTS -- #
# ------------------------------ #

pattern = re.compile('"(.+?)"')

match = True
parts = ["\n"]

while(match):
    match = re.search(pattern, PYCODE)

    if match:
        start = PYCODE[:match.start()]

        if parts[-1][-1] == "\n":
            parts.append(start)

        else:
            parts[-1] += start

        parts[-1] += '"' + "".join(
            '\\u%04x' % ord(c) for c in match.group()[1:-1]
        ) + '"'

        PYCODE = PYCODE[match.end():]

parts.append(PYCODE)

PYCODE = "\n".join(parts[1:])
PYCODE = PYCODE.replace("\n and", " and")


# ------------------------- #
# -- PYFILE CAN BE BUILD -- #
# ------------------------- #

with open(
    file     = NEW_PYFILE,
    mode     = "w",
    encoding = "utf8"
) as pyfile:
    pyfile.write(PYCODE)
