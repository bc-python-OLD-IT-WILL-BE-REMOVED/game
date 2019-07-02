from random import randint, choice

from model.ope import *


# --------------- #
# -- CONSTANTS -- #
# --------------- #

WIN, LOOSE, ILLEGAL = range(3)

SET_WIN   = set([WIN])
SET_LOOSE = set([LOOSE])


# -------------- #
# -- EVALUATE -- #
# -------------- #

def ask(ope_symbol, a_tmax, b_tmax):
    a = randint(1, 10**(a_tmax) - 1)
    b = randint(1, 10**(b_tmax) - 1)

    if ope_symbol in "-/" and a < b:
        a, b = b, a

    message, _, func = OPES[ope_symbol]

# Asks it.
    ope_to_do = message.format(a = a, b = b)

# Let's the pupils answers.
    labels = ["Ça donne combien ?"]

    if ope_symbol == SYMB_DIV:
        labels.append("Et il reste combien ?")

    answers = func(a, b)

    if type(answers) == int:
        answers = (answers,)

# Nothing more to do ...
    return {
        "ope"    : ope_to_do,
        "labels" : labels,
        "answers": answers
    }


def do_test(opes_to_test, nb_quest, sizes):
    if len(opes_to_test) == 1:
        choice_ope = lambda onelist: onelist[0]
    else:
        choice_ope = choice

    tests = []

    for i in range(nb_quest):
        ope_tested = choice_ope(opes_to_test)

        a_tmax, b_tmax = sizes[ope_tested]

        tests.append(
            ask(
                ope_symbol = ope_tested,
                a_tmax     = a_tmax,
                b_tmax     = b_tmax
            )
        )

    return tests
