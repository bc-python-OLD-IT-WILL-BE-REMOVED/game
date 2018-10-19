import ast

import sympy

from mistool.os_use import PPath as Path


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR   = Path(__file__).parent
OLD_PYFILE = THIS_DIR / "tictactoe-01-nolist-nofonction.py"
NEW_PYFILE = THIS_DIR / "tictactoe-03-nolist-nofonction-nochar-nocomment.py"
_MODULE    = THIS_DIR / "_.py"


# ----------- #
# -- TOOLS -- #
# ----------- #

def sortme(x):
    if not isinstance(x, str):
        x = str(x)

    return -len(x)


# ----------------------------- #
# -- LET'S PLAY WITH THE AST -- #
# ----------------------------- #

with open(
    file     = OLD_PYFILE,
    mode     = "r",
    encoding = "utf8"
) as pyfile:
    PYCODE = pyfile.read()


VARIABLES_USED = {
    k: set()
    for k in ['nb', 'str', 'value', 'var']
}


def walk_in_ast(code_ast, shift = ""):
    global VARIABLES_USED

    if isinstance(code_ast, ast.AST):
        for onefield in code_ast._fields:
            if onefield == "id":
                id = code_ast.id

                if id in ['print', 'input']:
                    VARIABLES_USED['value'].add(id)

                else:
                    VARIABLES_USED['var'].add(id)

            elif onefield == "n":
                VARIABLES_USED['nb'].add(code_ast.n)

            elif onefield == "s":
                VARIABLES_USED['str'].add(code_ast.s)

            elif onefield == "value":
                value = code_ast.value

                if type(value) in [bool, int]:
                    VARIABLES_USED['value'].add(value)

# Messy -1 and co...
            elif onefield == "comparators":
                try:
                    if isinstance(code_ast.comparators[0].op, ast.USub):
                        VARIABLES_USED['nb'].add(
                            -code_ast.comparators[0].operand.n
                        )

                except:
                    ...

            walk_in_ast(getattr(code_ast, onefield), shift + " "*2)

    elif isinstance(code_ast, list):
        for el in code_ast:
            walk_in_ast(el, shift + " "*2)


walk_in_ast(ast.parse(PYCODE))

VARIABLES_USED = {
    k: sorted(list(s), key = sortme)
    for k, s in VARIABLES_USED.items()
}


# --------------- #
# -- __IFY ALL -- #
# --------------- #

_ = "__"

SHORTCUTS = {}

# Strings first !
for onestr in VARIABLES_USED['str']:
    for quote in ['"', "'"]:
        PYCODE = PYCODE.replace(
            f"{quote}{onestr}{quote}",
            f"_.{_}"
        )

    SHORTCUTS[f'"{onestr}"'] = _

    _ += "_"


# Other things...
for kind in ['value', 'var', 'nb']:
    for onething in VARIABLES_USED[kind]:
        if kind == 'var':
            replacement = _

        else:
            replacement = f"_.{_}"

            SHORTCUTS[str(onething)] = _

        PYCODE = PYCODE.replace(
            f"{onething}",
            replacement
        )

        _ += "_"


# -------------------------------- #
# -- NO COMMENT, NO EMPTY LINES -- #
# -------------------------------- #

NEWPYCODE = ["import _"]

for oneline in PYCODE.splitlines():
    testline = oneline.strip()

    if not testline or testline.startswith("#"):
        ...

    else:
        NEWPYCODE.append(oneline)

NEWPYCODE = "\n".join(NEWPYCODE)


# -------------- #
# -- _ MODULE -- #
# -------------- #

MOD_CODE = []

lastnbof_ = 1

for val, _ in SHORTCUTS.items():
    nbof_ = len(_)

    for i in range(lastnbof_, nbof_ - 1):
        MOD_CODE.append(f"#{'_'*i}")

    lastnbof_ = nbof_

    MOD_CODE.append(f"{_} = {val}")

MOD_CODE = "\n".join(MOD_CODE)


# -------------------------- #
# -- PYFILES CAN BE BUILD -- #
# -------------------------- #

with open(
    file     = NEW_PYFILE,
    mode     = "w",
    encoding = "utf8"
) as pyfile:
    pyfile.write(NEWPYCODE)


with open(
    file     = _MODULE,
    mode     = "w",
    encoding = "utf8"
) as pyfile:
    pyfile.write(MOD_CODE)
