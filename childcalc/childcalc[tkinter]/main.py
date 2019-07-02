# Source
#     * https://www.tutorialspoint.com/python/tk_menu.htm

from tkinter import *

from model.ope import *
from model.eval import *


# --------------------- #
# -- GUI - CONSTANTS -- #
# --------------------- #

OPES_TO_TEST = ALL_SYMB_OP
NB_QUEST     = 5
SIZES        = DEFAULT_SIZES

TESTS = None

NB_GOODS = 0

# ---------------------------- #
# -- GUI - SETTINGS ACTIONS -- #
# ---------------------------- #

def donothing():
    filewin = Toplevel(master = root)
    button = Button(
        master = filewin,
        text   = "Coquille vide pour le moment !"
    )
    button.pack()


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

    root.update()


def validate_answer():
    global NB_GOODS, TESTS

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

        if answers_wanted == answers_given:
            NB_GOODS += 1

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

            root.update()


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

configmenu.add_command(label="Changer", command=donothing)

menubar.add_cascade(label="Réglages", menu=configmenu)

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

update_settings_infos()


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


canvas_neuro_picture = Canvas(
    master     = working_frame,
    width      = 200,
    height     = 200,
    background = 'grey'
)
canvas_neuro_picture.grid(
    row    = 6,
    column = 0,
    sticky = "ew"
)


bulid_new_tests()


# -------------- #
# -- LET'S GO -- #
# -------------- #

root.mainloop()
