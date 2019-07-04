# Source
#     * https://www.tutorialspoint.com/python/tk_menu.htm

from tkinter import *
import os

from model.ope import *
from model.eval import *


# --------------------- #
# -- GUI - CONSTANTS -- #
# --------------------- #

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


OPES_TO_TEST = ALL_SYMB_OP
NB_QUEST     = 5
SIZES        = DEFAULT_SIZES

# For settings
TAG_OPE = "ope"

SETTINGS_UI = {
    TAG_NB_QUEST: "NOMBRE DE QUESTIONS",
    TAG_OPE     : "OPÉRATIONS VOULUES ( + - * / )",
    TAG_PLUS    : "TAILLE DES NOMBRES POUR LES ADDITIONS ET LES SOUSTRACTIONS",
    TAG_MULT_1  : "TAILLE DU 1ER NOMBRE POUR LES PRODUITS",
    TAG_MULT_2  : "TAILLE DU 2IÈME NOMBRE POUR LES PRODUITS",
    TAG_DIV_1   : "TAILLE DU NOMBRE À DIVISER POUR LES DIVISIONS",
    TAG_DIV_2   : "TAILLE DU NOMBRE QUI DIVISE POUR LES DIVISIONS",
}


TESTS      = None
NB_GOODS   = 0

REPORT_WIN   = None
SETTINGS_WIN = None

BUTTON_BCK_COLOR = 'blue'


# ----------- #
# -- TOOLS -- #
# ----------- #

def txtdigit(i):
    message = "chiffre"

    if i != 1:
        message += "s"

    return "{0} {1}".format(i, message)


# ---------------------------- #
# -- GUI - SETTINGS ACTIONS -- #
# ---------------------------- #

def illegal_message(text):
    return text  + " -- << NON COMPRIS >>"

def update_settings(ids, labels):
    global OPES_TO_TEST, NB_QUEST, SIZES, SETTINGS_WIN

    choices_are_ok = True

    for tag in ids:
        choice = ids[tag].get()

# Operations must be + , - , * or /
        if tag == TAG_OPE:
            opeset_wanted = set(
                x
                for x in choice
                if x.strip()
            )

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

        SETTINGS_WIN.destroy()
        SETTINGS_WIN = None


def change_settings():
    global SETTINGS_WIN

    if SETTINGS_WIN is None:
        SETTINGS_WIN = Toplevel(master = root)
        SETTINGS_WIN.title('Calculs au hasard - Réglages')

# No destroy button.
        SETTINGS_WIN.protocol('WM_DELETE_WINDOW', lambda: None)

    user_frame = Frame(master = SETTINGS_WIN)
    user_frame.grid(
        row  = 0, column = 0,
        padx = 5, pady   = 5
    )

    ids    = {}
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
        master  = SETTINGS_WIN,
        text    = "MODIFIER",
        command = lambda: update_settings(ids, labels),
        bg      = BUTTON_BCK_COLOR,
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
            template = "1er facteur à {0} et 2ième facteur à {1}"

        elif symb == "/":
            template  = "1er nombre à {0} et diviseur à {1}"

        else:
            template  = "deux nombres à {0}"

        infos += template.format(
            txtdigit(sizes[0]),
            txtdigit(sizes[1])
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
        ope_to_do_txt_var.set("\n\n")
        return

    TESTS = do_test(OPES_TO_TEST, NB_QUEST, SIZES)

    update_working()


def clear_answers():
    entries_answers[0].delete(0, 'end')
    entries_answers[1].delete(0, 'end')


def hide_answers(indices):
    if 1 in indices:
        labels_answers_txt_var[0].set("")
        entries_answers[0].config(
            state = 'disabled',
            bd    = 0
        )

    if 2 in indices:
        labels_answers_txt_var[1].set("")
        entries_answers[1].config(
            state = 'disabled',
            bd    = 0
        )

def update_working():
    clear_answers()

    last_test = TESTS[-1]
    quest_num = NB_QUEST - len(TESTS) + 1

    ope_to_do_txt_var.set(
        "Question {0} sur {1}\n\n{2}".format(
            quest_num,
            NB_QUEST,
            last_test["ope"]
        )
    )


    labels = last_test["labels"]

    labels_answers_txt_var[0].set(labels[0])
    entries_answers[0].config(
        state = 'normal',
        bd    = 2
    )

    if len(labels) == 2:
        labels_answers_txt_var[1].set(labels[1])
        entries_answers[1].config(
            state = 'normal',
            bd    = 2
        )

    else:
        labels_answers_txt_var[1].set("")
        hide_answers([2])


    validate_but.config(text = 'VALIDER')

    working_frame.update()


def validate_answer():
    global NB_GOODS, TESTS, neuropict, ope_to_do

# Quizz starts.
    if TESTS is None:
        if REPORT_WIN is not None:
            REPORT_WIN.destroy()

        TESTS = []
        bulid_new_tests()

# One question validated.
    else:
        last_test = TESTS.pop(-1)

        answers_wanted = [
            str(ans)
            for ans in last_test['answers']
        ]

        answers_given = [entries_answers[0].get()]

        if len(answers_wanted) == 2:
            answers_given.append(entries_answers[1].get())

# GOOD
        if answers_wanted == answers_given:
            NB_GOODS += 1
            imgname   = 'good'

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
# Restart a new test.
            TESTS = None

            ope_to_do_txt_var.set("\n\n")
            ope_to_do.config(bd = 0)

            clear_answers()
            hide_answers([1, 2])

            neuropict.config(file = THIS_DIR + '/img/question.png')


# Report
            show_report()

# Let(s go for another play !)
            validate_but.config(text = 'RECOMMENCER')


# Force the update othe GUI.
        working_frame.update()


# --------------------------- #
# -- GUI - WORKING ACTIONS -- #
# --------------------------- #

def show_report():
    global NB_QUEST, NB_GOODS, REPORT_WIN

    message = StringVar()
    message.set(do_report(NB_QUEST, NB_GOODS))

    REPORT_WIN = Toplevel(master = root)
    REPORT_WIN.title('Calculs au hasard - Score final')

    larg_fen = 350
    haut_fen = 150

    xpos_fen = ypos_fen = 300

    REPORT_WIN.geometry(
        "{0}x{1}+{2}+{3}".format(
            larg_fen, haut_fen,
            xpos_fen, ypos_fen
        )
    )


    report = Label(
        master       = REPORT_WIN,
        textvariable = message,
        justify      = LEFT,
        relief       = RAISED,
        padx         = 5,
    )
    report.grid(row = 0, column = 0)


# ---------------- #
# -- GUI - ROOT -- #
# ---------------- #

root = Tk()
root.title('Calculs au hasard')


# ----------------------- #
# -- GUI - CONFIG MENU -- #
# ----------------------- #

# This is just for testing the use of menu.

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
    bg      = BUTTON_BCK_COLOR,
)
setup_but.grid(row = 1, column = 0, pady = 10)


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
    justify      = CENTER,
    relief       = RAISED,
    bd           = 0,
    padx         = 5,
)
ope_to_do.grid(row = 0, column = 0, pady = 5)


labels_answers         = {}
labels_answers_txt_var = {}
entries_answers        = {}

for i in range(2):
    row = 1 + 2*i

    labels_answers_txt_var[i] = StringVar()

    labels_answers[i] = Label(
        master       = working_frame,
        textvariable = labels_answers_txt_var[i],
        justify      = CENTER,
    )
    labels_answers[i].grid(row = row, column = 0)

    entries_answers[i] =  Entry(
        master = working_frame,
        state  = 'disabled',
        relief = RAISED,
        bd     = 0,
    )
    entries_answers[i].grid(row = row + 1, column = 0, pady = 5)


validate_but = Button(
    master  = working_frame,
    text    = "COMMENCER",
    command = validate_answer,
    relief  = SOLID,
    bg      = BUTTON_BCK_COLOR,
)
validate_but.grid(row = 5, column = 0, pady = 5)


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
