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

TAG_DIV = "/"

def _datas_message(ope_symb):
    if ope_symb == TAG_DIV:
        return "Divises {a} par {b}."

    return "Calcules {{a}} {ope} {{b}}.".format(ope = ope_symb)

def _datas_val(ope_symb, ope_name, func):
    return (_datas_message(ope_symb), ope_name, func)


# ---------------- #
# -- CONSTANTS -- #
# ---------------- #

OPES = {}

for symb, (opename, tag, func) in {
    "+": ("addition"      , "PLUS" , add),
    "-": ("soustraction"  , "MINUS", sub),
    "*": ("multiplication", "MULT" , mult),
    "/": ("division"      , "DIV"  , eucldiv),
}.items():
    OPES[symb] = _datas_val(symb, opename, func)

    if symb in "*/":
        for i in range(1, 3):
            vars()[
                "TAG_{0}_{1}".format(tag, i)
            ] = "{0}_{1}".format(symb, i)

    else:
        vars()["TAG_{0}".format(tag)] = symb


ALL_SYMB_OP = list(OPES.keys())

OPES_SET = set(ALL_SYMB_OP)


DEFAULT_SIZES = {}

for symb in ALL_SYMB_OP:
    if symb in "/":
        sizes = [2, 1]

    elif symb == "*":
        sizes = [1, 1]

    else:
        sizes = [2, 2]

    DEFAULT_SIZES[symb] = sizes
