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
    print(message.format(a = a, b = b))

# Let's the pupils answers.
    answers = [input("Ça donne combien ? ")]

    if ope_symbol == SYMB_DIV:
        answers.append(
            input("Et il reste combien ? ")
        )

# Answers must be integers.
    for oneans in answers:
        if not oneans.isdigit():
            return ILLEGAL

    answers = [int(oneans) for oneans in answers]

# Good or bad answers ?
    answers_wanted = func(a, b)

    if len(answers) == 1:
        answers_wanted = [answers_wanted]

    score = []

    for i, oneans in enumerate(answers):
        if oneans == answers_wanted[i]:
            score.append(WIN)

        else:
            score.append(LOOSE)

    return score


def do_test(opes_to_test, nb_quest, sizes):
    if len(opes_to_test) == 1:
        choice_ope = lambda onelist: onelist[0]
    else:
        choice_ope = choice

    nb_good = 0

    for i in range(nb_quest):
        ope_tested = choice_ope(opes_to_test)

        a_tmax, b_tmax = sizes[ope_tested]

        print()
        score = ask(
            ope_symbol = ope_tested,
            a_tmax     = a_tmax,
            b_tmax     = b_tmax
        )

        if set(score) == SET_WIN:
            nb_good += 1

            print("Bravo pour cette fois !")

        elif score == ILLEGAL:
            print("Les réponses sont des nombres !")

        elif set(score) == SET_LOOSE:
            print("Dommage pour ce coup là...")

# Only for divisions !
        elif score[0] == LOOSE:
            print("Dommage pour ce coup là, ta division est fausse.")

        else:
            print("Dommage pour ce coup là, ton reste est faux.")

    return nb_good


# ------------ #
# -- REPORT -- #
# ------------ #

def do_report(nb_quest, nb_good):
    rate = nb_good / nb_quest

    if rate == 0:
        report = "Aucune réponse juste, t'es une quiche..."

    else:
        message_good = "bonne réponse"

        if nb_good > 1:
            message_good = " ".join(
                word + "s"
                for word in message_good.split()
            )

        message_good = "{0} {1} sur {2}".format(
            nb_good,
            message_good,
            nb_quest
        )


        if rate <= 0.2:
            comment = "il faut bosser encore un peu."

        elif rate <= 0.4:
            comment = "presque la moyenne !"

        elif rate <= 0.6:
            comment = "c'est pas mal !"

        elif rate <= 0.8:
            comment = "t'es une brute de calcul !"

        elif rate < 1:
            comment = "presque tout bon gamin.e ! Impressionnant."

        elif nb_good == 1:
            comment = "TOUT BON mon pote maaaaaaaaais tu n'as fait qu'un calcul !"

        else:
            comment = "oh my godness ! MY GODNESS HiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiYA  TOUT BON !!!"


        report = message_good + ", " + comment


    print(
        "",
        "BILAN",
        "-----",
        report,
        sep = "\n"
    )
