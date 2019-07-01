from model.ope import *
from model.eval import *


# ------------------ #
# -- TUI - CONFIG -- #
# ------------------ #

def ask_int(message, min, max = float("inf")):
    n = submin = min - 1

    while(n < min or n > max):
        n = input(message)

        if n.isdigit():
            n = int(n)

        else:
            n = submin

    return n


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


    choice = ask_int(
        message = " * Choix : ",
        min     = 1,
        max     = 6
    )


    if choice == 5:
        symbols.pop(index_div)

    elif choice != 6:
        symbols = [symbols[choice - 1], ]


    return symbols


def nb_quest_wanted():
    print("""
Tu veux combien de calculs.
    """)

    return ask_int(
        message = " * Choix : ",
        min     = 1
    )


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


# --------------------- #
# -- TUI - MAIN LOOP -- #
# --------------------- #

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


# ------------------------ #
# -- THIS FILE LAUNCHED -- #
# ------------------------ #

if __name__ == '__main__':
    main()
