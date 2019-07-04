# Source
#     * https://www.tutorialspoint.com/python/tk_menu.htm

import os

from tkinter import *
from tkinter.font import Font

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

SETTINGS_GUI = {
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

BUTTON_BCK_COLOR = 'blue'


# ----------- #
# -- TOOLS -- #
# ----------- #

def txtdigit(nbdigits):
    text = "chiffre"

    if nbdigits != 1:
        text += "s"

    return "{0} {1}".format(nbdigits, text)


# ---------------------------- #
# -- GUI - SETTINGS ACTIONS -- #
# ---------------------------- #

def illegal_message(text):
    return text  + " -- << NON COMPRIS >>"


def update_settings(settings_ids, labels):
    global ALL_SYMB_OP, OPES_SET, OPES_TO_TEST, TAG_OPE, \
           NB_QUEST, SIZES, \
           SETTINGS_GUI, settings_win

    choices_are_ok = True

    for tag in settings_ids:
        choice = settings_ids[tag].get()

# Operations must be + , - , * or /
        if tag == TAG_OPE:
            opeset_wanted = set(
                x
                for x in choice
                if x.strip()
            )

            if not opeset_wanted <= OPES_SET:
                choices_are_ok = False

                settings_labels[tag].config(text = illegal_message(SETTINGS_GUI[tag]))

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

                settings_labels[tag].config(text = illegal_message(SETTINGS_GUI[tag]))

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

        bulid_new_tests()

        settings_win.withdraw()


def change_settings():
    global  OPES_TO_TEST, \
            NB_QUEST, SIZES,  \
            BUTTON_BCK_COLOR, SETTINGS_GUI, settings_win

    settings_ids["nbquest"].delete(0, 'end')
    settings_ids["nbquest"].insert(0, NB_QUEST)

    settings_ids["ope"].delete(0, 'end')
    settings_ids["ope"].insert(0, OPES_TO_TEST)

    for symb, size in SIZES.items():
        if symb == "+":
            settings_ids[symb].delete(0, 'end')
            settings_ids[symb].insert(0, size[0])

        elif symb != "-":
            for i in range(2):
                settings_ids["{0}_{1}".format(symb, i+1)].delete(0, 'end')
                settings_ids["{0}_{1}".format(symb, i+1)].insert(0, size[i])

# Source: http://www.blog.pythonlibrary.org/2012/07/26/tkinter-how-to-show-hide-a-window/
    settings_win.update()
    settings_win.deiconify()


def update_settings_infos():
    global OPES, OPES_TO_TEST, \
           NB_QUEST, SIZES, \
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
    global OPES_TO_TEST, TESTS, \
           NB_QUEST, SIZES, \
           ope_to_do_txt_var

    if TESTS is None:
        ope_to_do_txt_var.set("\n\n")
        return

    TESTS = do_test(OPES_TO_TEST, NB_QUEST, SIZES)

    update_working()


def clear_answers():
    global entries_answers

    for i in range(2):
        entries_answers[i].delete(0, 'end')
        entries_answers[i].config(fg = "black")


def hide_answers(indices):
    global labels_answers_txt_var, entries_answers

    for i in range(2):
        if i in indices:
            labels_answers_txt_var[i].set("")
            entries_answers[i].config(
                state = 'disabled',
                bd    = 0
            )


def update_working():
    global TESTS, \
           NB_QUEST, \
           labels_answers_txt_var, entries_answers, \
           validate_but, working_frame

    clear_answers()

    entries_answers[0].focus()

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
        hide_answers([1])


    validate_but.config(text = 'VALIDER')

    working_frame.update()


def errortxt(answer, good_answer):
    answer = answer.strip()

    if not answer.strip():
        message = "RÉPONSE VIDE !"

    elif not answer.isdigit():
        message = "{0} : ON VEUT UN NOMBRE !"

    else:
        message = "{0} : PAS CORRECT  -->  BONNE RÉPONSE : {1}"

    return message.format(
        answer,
        good_answer
    )


def show_bad(answers_wanted, answers_given):
    global entries_answers

    for i, ans in enumerate(answers_given):
        good_ans = answers_wanted[i]

        if ans != good_ans:
            entries_answers[i].delete(0, 'end')
            entries_answers[i].insert(0, errortxt(ans, good_ans))

            entries_answers[i].config(fg="red")


def update_neuropict(kind):
    global neuropict

    neuropict.config(
        file = THIS_DIR + '/img/{0}.png'.format(kind)
    )


def validate_answer():
    global TESTS, NB_GOODS, \
           ope_to_do, ope_to_do_txt_var, \
           entries_answers, validate_but, working_frame, report_win

# Quizz starts.
    if TESTS is None:
        report_win.withdraw()

        TESTS = []
        bulid_new_tests()

# One question validated.
    else:
        last_test = TESTS[-1]

        answers_wanted = [
            str(ans)
            for ans in last_test['answers']
        ]

        answers_given = [entries_answers[0].get()]

        if len(answers_wanted) == 2:
            answers_given.append(entries_answers[1].get())

# BAD (CONTINUE)
        if validate_but["text"] == 'CONTINUER':
            we_continue = True

            update_neuropict('question')
            clear_answers()

# BAD
        elif answers_wanted != answers_given:
            we_continue = False

            update_neuropict('bad')
            show_bad(answers_wanted, answers_given)
            validate_but.config(text = 'CONTINUER')

# GOOD
        else:
            we_continue = True

            NB_GOODS += 1
            update_neuropict('good')

# We continue.
        if we_continue:
            TESTS.pop(-1)

            if TESTS:
                update_working()

# This was the last question validated.
            else:
# Restart a new test.
                TESTS = None

                ope_to_do_txt_var.set("\n\n")
                ope_to_do.config(bd = 0)

                clear_answers()
                hide_answers([0, 1])

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
    global NB_QUEST, NB_GOODS, \
           report_message, report_win

    report_message.set(do_report(NB_QUEST, NB_GOODS))

    report_win.update()
    report_win.deiconify()


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
# -- GUI - CONFIG DIALOG -- #
# ------------------------- #

settings_win = Toplevel(master = root)
settings_win.title('Calculs au hasard - Réglages')

# No destroy button.
settings_win.protocol('WM_DELETE_WINDOW', lambda: None)

settings_user_frame = Frame(master = settings_win)

settings_user_frame.grid(
    row  = 0, column = 0,
    padx = 5, pady   = 5
)

settings_ids    = {}
settings_labels = {}

row = 0

for kind, message in SETTINGS_GUI.items():
    settings_labels[kind] = Label(
        master = settings_user_frame,
        text   = message
    )

    settings_labels[kind].grid(row = row, column = 0)

    settings_ids[kind] =  Entry(
        master = settings_user_frame,
        relief = RAISED,
    )

    settings_ids[kind].grid(row = row, column = 1)

    row += 1


settings_doit_but = Button(
    master  = settings_win,
    text    = "MODIFIER",
    command = lambda: update_settings(settings_ids, settings_labels),
    bg      = BUTTON_BCK_COLOR,
)

settings_doit_but.grid(row = 1, column = 0)

settings_win.withdraw()


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

setup_but.grid(
    row  = 1, column = 0,
    pady = 10
)


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

ope_to_do.grid(
    row  = 0, column = 0,
    pady = 5
)


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
        width  = 50,
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

validate_but.grid(
    row  = 5, column = 0,
    pady = 5
)


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


# ------------------------- #
# -- GUI - REPORT DIALOG -- #
# ------------------------- #

report_win = Toplevel(master = root)
report_win.title('Calculs au hasard - Score final')

width_screen = 550
height_screen = 150

width_ecran = root.winfo_screenwidth()
height_ecran = root.winfo_screenheight()

xpos_screen = width_ecran // 2 - width_screen // 2
ypos_screen = height_ecran // 2 - height_screen // 2

report_win.geometry(
    "{0}x{1}+{2}+{3}".format(
        width_screen, height_screen,
        xpos_screen , ypos_screen
    )
)


report_message = StringVar()

# Source: https://stackoverflow.com/a/31918553/4589608
report_label = Label(
    master       = report_win,
    textvariable = report_message,
    justify      = LEFT,
    relief       = RAISED,
    padx         = 5,
    font         = Font(size=18)
)
report_label.pack(
    anchor = 'center',  # H-centering
    expand = 1          # V-centering
)

report_win.withdraw()


# -------------- #
# -- LET'S GO -- #
# -------------- #

if __name__ == "__main__":
    update_settings_infos()
    bulid_new_tests()

    root.mainloop()
