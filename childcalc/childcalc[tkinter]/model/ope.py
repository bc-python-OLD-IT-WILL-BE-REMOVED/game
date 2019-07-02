# ---------------- #
# -- CONSTANTS -- #
# ---------------- #

SYMB_DIV = "/"


# -------------------------- #
# -- OPERATIONS EVALUATED -- #
# -------------------------- #

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def eucldiv(a, b):
    return (a // b, a % b)


# KEY   : aithmétical symbol.
# Value : (
#     printed message,
#     name of the opration,
#     function doing the calculus
# )

def _datas_message(ope_symb):
    if ope_symb == SYMB_DIV:
        return "Divises {a} par {b}."

    return "Calcules {{a}} {ope} {{b}}.".format(ope = ope_symb)

def _datas_val(ope_symb, ope_name, func):
    return (_datas_message(ope_symb), ope_name, func)


OPES = {
    symb: _datas_val(symb, opename, func)
    for symb, (opename, func) in {
        "+": ("addition"      , add),
        "-": ("soustraction"  , sub),
        "*": ("multiplication", mult),
        "/": ("division"      , eucldiv),
    }.items()
}

ALL_SYMB_OP = list(OPES.keys())

DEFAULT_SIZES = {}

for symb in ALL_SYMB_OP:
    if symb in "/":
        sizes = [2, 1]

    elif symb == "*":
        sizes = [1, 1]

    else:
        sizes = [2, 2]

    DEFAULT_SIZES[symb] = sizes
