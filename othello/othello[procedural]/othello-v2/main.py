"""
For pedagogical purposes only : some easy-to-do enhancements must be done for
a "real life" use like for example choosing modes from the GUI, or changing
GUI from one GUI to another and so on...

Source for the rules and some useful comments :
    * http://www.lecomptoirdesjeux.com/regle-reversi.htm


info::
    So as to play easily with variables shared by several Python files, we store
    all our "global like" variables in a dictionnary, using the fact that Python
    works with references for this kind of variables.


warning::
    A lot of `global` used can be ommitted. Indeed they are there only for
    pedagogical reasons.
"""

import settings


# # ----------------- #
# # -- WHICH GUI ? -- #
# # ----------------- #
#
# print("""
# Choix de l'interface "graphique" :
#     [1] Interface via le "terminal"
#     [2] Interface `tkinter`
#     [3] Interface `matplotlib`
#     [4] Interface `PyQT`
#     [5] Étude statistique (pas de joueur humain dans ce cas)
# """.rstrip())
#
# guichoice = input("Votre choix : ")
#
# while guichoice not in [str(i) for i in range(1, 3)]:
#     guichoice = input("Mauvais choix. Recommencer : ")
#
#
# # ---------------------- #
# # -- SIZE OF THE GRID -- #
# # ---------------------- #
#
# gridsize = input("\nTaille de la grille (nombre pair entre 6 et 16) : ")
#
# while gridsize not in [str(i) for i in range(6, 27, 2)]:
#     gridsize = input("Mauvais choix. Recommencer : ")
#
# gridsize = int(gridsize)
#
#
# # ------------------ #
# # -- WHICH MODE ? -- #
# # ------------------ #
#
# players_modes = []
#
# for playernb in range(1, 3):
#     print("""
# Choix pour le joueur {0} :
#     [1] Un humain
#     [2] La SAI tout au hasard
#     [3] L'AI meilleur coup du tour
#     [4] L'AI meilleur coup sur 3 tours
#     """.format(playernb).rstrip())
#
#     modechoice = input("Votre choix : ")
#
#     while modechoice not in [str(i) for i in range(1, 5)]:
#         modechoice = input("Mauvais choix. Recommencer : ")
#
#     players_modes.append(int(modechoice) - 1)
#
#
# # -------------------- #
# # -- USER'S CHOICES -- #
# # -------------------- #
#
# print("""
# ------------------------------
#  CHOIX RETENUS
#
#
#            INTERFACE = N°{0}
#  TAILLE DE LA GRILLE = {1}
#             JOUEUR 1 = Type {2}
#             JOUEUR 2 = Type {3}
# ------------------------------
# """.format(
#         guichoice,
#         gridsize,
#         players_modes[0],
#         players_modes[1]
#     ).rstrip()
# )
#
#
# # -------------------------- #
# # -- IT'S TIME TO PLAY... -- #
# # -------------------------- #
#
# print("\nLancement du jeu...")

settings.init(
    gridsize      = 8,
    players_modes = [1, 3]
)

# Now than settings are done, we can import the good GUI.
# if guichoice == "1":
#     import guiterminal as gui
#
# elif guichoice == "2":
#     import guitkinter as gui
#
# elif guichoice == "3":
#     import guimatplotlib as gui
#
# elif guichoice == "4":
#     import guipyqt as gui
#
# else:
#     import guistat as gui
#

import guiterminal as gui

gui.launchgui()
