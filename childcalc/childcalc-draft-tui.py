from random import randint, choice


# --------------- #
# -- CONSTANTS -- #
# --------------- #

SYMB_DIV = "/"

WIN, LOOSE, ILLEGAL = range(3)

SET_WIN   = set([WIN])
SET_LOOSE = set([LOOSE])


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


# -------- #
# -- TUI-- #
# -------- #

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
        answers.append(input("Et il reste combien ? "))

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


def opes_wanted():
    message = ["", "Que veux-tu faire ?", ""]

    nb = 0

    symbols   = []
    index_div = None

    for onesymb, (_, ope_name, _) in OPES.items():
        symbols.append(onesymb)

        if onesymb == SYMB_DIV:
            index_div = nb

        nb += 1

        message.append("    ({0}) Des {1}s".format(nb, ope_name))

    message += [
        "    ---------------------------",
        "    (5) Tout sauf des divisions",
        "    (6) Tout",
        "",
    ]

    message = "\n".join(message)

    print(message)


    choice = "x"

    while(choice not in "123456"):
        choice = input("    * Choix : ")

    choice = int(choice)


    if choice == 5:
        symbols.pop(index_div)

    elif choice != 6:
        symbols = [symbols[choice - 1], ]


    return symbols


def ask_int(message, min):
    min -= 1

    n = min

    while(n == min):
        n = input(message)

        if n.isdigit():
            n = int(n)

        else:
            n = min

    return n


def nb_quest_wanted():
    print("""
Tu veux combien de calculs.
    """)

    return ask_int("    * Choix : ", 1)


def size_messages(pieces):
    if len(pieces) == 1:
        return [
            "Pour {0}, combien de chiffres ? ".format(pieces[0])
        ]

    return [
        "Pour {0}, combien de chiffres ? ".format(pieces[0]),
        "Et pour {0} ? ".format(pieces[1])
    ]


def ask_sizes(messages):
    if messages is None:
        return None

    sizes = [
        ask_int(
            message = m,
            min     = 1
        )
        for m in messages
    ]

    return sizes


def sizes_wanted(opes_wanted):
    sizes = {
        symb: None
        for symb in OPES
    }

# Additions and/or substractions
    if '+' in opes_wanted:
        if '-' in opes_wanted:
            sizes['+'] = ["tes additions et tes soustactions"]
            sizes['-'] = sizes['+']

        else:
            sizes['+'] = ["tes additions"]

    elif '-' in opes_wanted:
        sizes['-'] = ["tes soustactions"]

# Multiplicactions
    if '*' in opes_wanted:
        sizes['*'] = [
            "le premier facteur",
            "le deuxième"
        ]

# Divisions
    if '/' in opes_wanted:
        sizes['/'] = [
            "le nombre à diviser",
            "le diviseur"
        ]

# Ask the sizes.
    print()

    addition_asked = False

    for symb, messages in sizes.items():
        if messages is None \
        or addition_asked and symb == "-":
            continue

        if symb in ["+", "-"]:
            addition_asked = True

        sizes[symb] = ask_sizes(
            size_messages(messages)
        )

        if len(sizes[symb]) == 1:
            sizes[symb] *= 2

    if sizes['+'] is not None \
    and sizes['-'] is not None:
        sizes['-'] = sizes['+']

# Job done...
    return sizes


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
        score = ask(ope_tested, a_tmax, b_tmax)

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


def main():
    continue_to_play = "oui"

    while continue_to_play == "oui":
        opes_to_test = opes_wanted()
        nb_quest     = nb_quest_wanted()
        sizes        = sizes_wanted(opes_to_test)

        nb_good = do_test(opes_to_test, nb_quest, sizes)

        do_report(nb_quest, nb_good)

        continue_to_play = input("\nVeux-tu continuer ? [oui | non] ")
        continue_to_play = continue_to_play.lower()


# --------------- #
# -- MAIN CASE -- #
# --------------- #

if __name__ == '__main__':
    main()
