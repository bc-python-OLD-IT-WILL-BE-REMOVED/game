# Source
#     * https://www.tutorialspoint.com/python/tk_menu.htm

from tkinter import *
import os

from model.ope import *
from model.eval import *


# --------------------- #
# -- GUI - CONSTANTS -- #
# --------------------- #

OPES_TO_TEST = ALL_SYMB_OP
NB_QUEST     = 5
SIZES        = DEFAULT_SIZES


OPES_SET = set(ALL_SYMB_OP)


TAG_NB_QUEST = "nbquest"
TAG_OPE      = "ope"
TAG_PLUS     = "+"
TAG_MINUS    = "-"
TAG_FACT_1   = "*_1"
TAG_FACT_2   = "*_2"
TAG_DIV_1    = "/_1"
TAG_DIV_2    = "/_2"

_TAG_CALLING_WIN_ = "_CALLING_WIN_"


SETTINGS_UI = {
    TAG_NB_QUEST: "NOMBRE DE QUESTIONS",
    TAG_OPE     : "OPÉRATIONS VOULUES ( + - * / )",
    TAG_PLUS    : "TAILLE DES NOMBRES POUR LES ADDITIONS ET LES SOUSTRACTIONS",
    TAG_FACT_1  : "TAILLE DU 1ER NOMBRE POUR LES PRODUITS",
    TAG_FACT_2  : "TAILLE DU 2IÈME NOMBRE POUR LES PRODUITS",
    TAG_DIV_1   : "TAILLE DU NOMBRE À DIVISER POUR LES DIVISIONS",
    TAG_DIV_2   : "TAILLE DU NOMBRE QUI DIVISE POUR LES DIVISIONS",
}


TESTS = None

NB_GOODS = 0

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------- #
# -- GUI - SETTINGS ACTIONS -- #
# ---------------------------- #


def illegal_message(text):
    return text  + " -- << NON COMPRIS >>"

def update_settings(ids, labels):
    global OPES_TO_TEST, NB_QUEST, SIZES

    choices_are_ok = True

    for tag in ids:
        if tag == _TAG_CALLING_WIN_:
            continue

        choice = ids[tag].get()

# Operations must be + , - , * or /
        if tag == TAG_OPE:
            opeset_wanted = set(x.strip() for x in choice.split())

            if not opeset_wanted <= OPES_SET:
                choices_are_ok = False

                labels[tag].config(text = illegal_message(SETTINGS_UI[tag]))


            else:
                OPES_TO_TEST = [
                    one_ope
                    for one_ope in ALL_SYMB_OP
                    if one_ope in opeset_wanted
                ]

# Other settings must be none sero inetgers.
        else:
            if not choice.isdigit():
                choice = 0

            else:
                choice = int(choice)

            if choice <= 0:
                choices_are_ok = False

                labels[tag].config(text = illegal_message(SETTINGS_UI[tag]))

            elif tag == TAG_NB_QUEST:
                NB_QUEST = choice

            elif tag == "+":
                choice = [choice] * 2

                SIZES[tag]       = choice
                SIZES[TAG_MINUS] = choice

            else:
                tag, pos = tag.split("_")

                SIZES[tag][int(pos) - 1] = choice


# Everuthing is ok !
    if choices_are_ok:
        update_settings_infos()
        ids[_TAG_CALLING_WIN_].destroy()


def change_settings():
    settings_win = Toplevel(master = root)
    settings_win.title('Calculs au hasard - Réglages')

    user_frame = Frame(master = settings_win)
    user_frame.grid(
        row  = 0, column = 0,
        padx = 5, pady   = 5
    )

    ids    = {_TAG_CALLING_WIN_: settings_win}
    labels = {}
    row    = 0

    for kind, message in SETTINGS_UI.items():
        labels[kind] = Label(
            master = user_frame,
            text   = message
        )

        labels[kind].grid(
            row    = row,
            column = 0,
        )

        ids[kind] =  Entry(
            master = user_frame,
            relief = RAISED,
        )

        ids[kind].grid(row = row, column = 1)

        row += 1

    ids["nbquest"].insert(0, NB_QUEST)
    ids["ope"].insert(0, OPES_TO_TEST)

    for symb, size in SIZES.items():
        if symb == "+":
            ids[symb].insert(0, size[0])

        elif symb != "-":
            for i in range(2):
                ids["{0}_{1}".format(symb, i+1)].insert(0, size[i])


    button = Button(
        master = settings_win,
        text   = "MODIFIER",
        command = lambda: update_settings(ids, labels)
    )

    button.grid(
        row     = 1,
        column  = 0
    )


def update_settings_infos():
    global NB_QUEST, OPES_TO_TEST, SIZES, \
           settings_txt_var

    message = ["TAILLES DES NOMBRES"]

    for symb in OPES_TO_TEST:
        _, ope_name, _ = OPES[symb]

        sizes = SIZES[symb]

        infos  = ope_name.title()
        infos += " : "

        if symb == "*":
            template = "1er facteur à {0} chiffre(s) et 2ième facteur à {1} chiffre(s)"

        elif symb == "/":
            template  = "1er nombre à {0} chiffre(s) et diviseur à {1} chiffre(s)"

        else:
            template  = "deux nombres à {0} chiffre(s)"

        infos += template.format(
            sizes[0],
            sizes[1]
        )

        message.append(infos)

    message = "\n\n        + ".join(message)


    settings_txt_var.set("""
RÉGLAGES MODIFIABLES : VOIR LE MENU

    * NOMBRE DE QUESTIONS POSÉES : {0}

    * OPÉRATION(S) TESTÉE(S) : {1}

    * {2}
    """.format(
        NB_QUEST,
        "  ".join(OPES_TO_TEST),
        message
    ))

    root.update()


# --------------------------- #
# -- GUI - WORKING ACTIONS -- #
# --------------------------- #

def bulid_new_tests():
    global root, QUIZZ_STARTED, TESTS

    if TESTS is None:
        ope_to_do_txt_var.set("Cliquer sur << COMMENCER >> !")
        return

    TESTS = do_test(OPES_TO_TEST, NB_QUEST, SIZES)

    update_working()


def clear_answers():
    answer_1.delete(0, 'end')
    answer_2.delete(0, 'end')

def update_working():
    last_test = TESTS[-1]

    ope_to_do_txt_var.set(last_test["ope"])

    labels = last_test["labels"]

    label_answer_1_txt_var.set(labels[0])
    answer_1.config(state = 'normal')

    if len(labels) == 2:
        label_answer_2_txt_var.set(labels[1])
        answer_2.config(state = 'normal')

    else:
        label_answer_2_txt_var.set("")
        answer_2.config(state = 'disabled')

    clear_answers()

    validate_but.config(text = 'VALIDER')


def validate_answer():
    global NB_GOODS, TESTS, neuropict

# Quizz starts.
    if TESTS is None:
        TESTS = []
        bulid_new_tests()

# One question validated.
    else:
        last_test = TESTS.pop(-1)

        answers_wanted = [
            str(ans)
            for ans in last_test['answers']
        ]

        answers_given = [answer_1.get()]

        if len(answers_wanted) == 2:
            answers_given.append(answer_2.get())

# GOOD
        if answers_wanted == answers_given:
            NB_GOODS += 1

            imgname = 'good'

# BAD
        else:
            imgname = 'bad'

        neuropict.config(
            file = THIS_DIR + '/img/{0}.png'.format(imgname)
        )

# We continue.
        if TESTS:
            update_working()

# This was the last question validated.
        else:
# Report

# Restart a new test.
            TESTS = None

            ope_to_do_txt_var.set("Cliquer sur << RECOMMENCER >> !")
            clear_answers()

            validate_but.config(text = 'RECOMMENCER')

            neuropict.config(file = THIS_DIR + '/img/question.png')

# Force the update othe GUI.
        working_frame.update()


# ---------------- #
# -- GUI - ROOT -- #
# ---------------- #

root = Tk()
root.title('Calculs au hasard')


# ----------------------- #
# -- GUI - CONFIG MENU -- #
# ----------------------- #

menubar = Menu(master = root)

configmenu = Menu(
    master  = menubar,
    tearoff = 0
)

configmenu.add_command(
    label   = "Changer",
    command = change_settings
)

menubar.add_cascade(
    label = "Réglages",
    menu  = configmenu
)

root.config(menu = menubar)


# ------------------------- #
# -- GUI - SETTINGS AREA -- #
# ------------------------- #

settings_frame = Frame(master = root)
settings_frame.grid(
    row  = 0, column = 0,
    padx = 5, pady   = 5
)


settings_txt_var = StringVar()

settings = Label(
    master       = settings_frame,
    textvariable = settings_txt_var,
    justify      = LEFT,
    relief       = RAISED,
    padx         = 5,
)
settings.grid(row = 0, column = 0)

setup_but = Button(
    master  = settings_frame,
    text    = "CHANGER LES RÉGLAGES",
    command = change_settings,
    relief  = SOLID,
)
setup_but.grid(row = 1, column = 0)

# ------------------------ #
# -- GUI - WORKING AREA -- #
# ------------------------ #

working_frame = Frame(master = root)
working_frame.grid(
    row  = 1, column = 0,
    padx = 5, pady   = 5
)


ope_to_do_txt_var = StringVar()

ope_to_do = Label(
    master       = working_frame,
    textvariable = ope_to_do_txt_var,
    justify      = LEFT,
    relief       = RAISED,
    padx         = 5,
)
ope_to_do.grid(row = 0, column = 0)


label_answer_1_txt_var = StringVar()

label_answer_1 = Label(
    master       = working_frame,
    textvariable = label_answer_1_txt_var,
    justify      = RIGHT,
    padx         = 5,
)
label_answer_1.grid(row = 1, column = 0)

answer_1 =  Entry(
    master = working_frame,
    state  = 'disabled',
    relief = RAISED,
)
answer_1.grid(row = 2, column = 0)


label_answer_2_txt_var = StringVar()

label_answer_2 = Label(
    master       = working_frame,
    textvariable = label_answer_2_txt_var,
    justify      = RIGHT,
    padx         = 5,
)
label_answer_2.grid(row = 3, column = 0)

answer_2 =  Entry(
    master = working_frame,
    state  = 'disabled',
    relief = RAISED,
)
answer_2.grid(row = 4, column = 0)


validate_but = Button(
    master  = working_frame,
    text    = "COMMENCER",
    command = validate_answer,
    relief  = SOLID,
)
validate_but.grid(row = 5, column = 0)


neuropict = PhotoImage(file = THIS_DIR + '/img/question.png')

neuropict_label = Label(
    master = working_frame,
    image  = neuropict
)
neuropict_label.grid(
    row    = 6,
    column = 0,
    sticky = "ew"
)


# -------------- #
# -- LET'S GO -- #
# -------------- #

if __name__ == "__main__":
    update_settings_infos()
    bulid_new_tests()

    root.mainloop()
