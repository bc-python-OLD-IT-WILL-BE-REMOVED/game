# --------------- #
# -- CONSTANTS -- #
# --------------- #

#  x indicates the id of the player using the following conventions :
#
#  - 1 = ×  |  0 = empty  |  1 = o

x = - 1

# Some useful  texts.

t0 = "  "
t1 = " |"
t2 = '-'*11
t3 = " ×"
t4 = " o"
t5 = "Player with [ × ] wins."
t6 = "Player with [ o ] wins."
t7 = "No one wins."
t8 = "Player with [ o ], what is your k ? Use A1 or B3 for example : "
t9 = "Player with [ × ], what is your k ? Use A1 or B3 for example : "

# Some usefus shortcurts.

y = False
z = True
_i_ = input
_onl_ = print
_ononl_ = lambda x: print(x, end = '')

# Codification of the grid
#
#   a  |  b  |  c
# -----------------
#   d  |  e  |  f
# -----------------
#   g  |  h  |  i

a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
g = 0
h = 0
i = 0


# --------------- #
# -- MAIN LOOP -- #
# --------------- #

while z:
# Let's _onl_ the grid.
    _onl_()
    
    if a == - 1:
        _ononl_(t3)
    elif a == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if d == - 1:
        _ononl_(t3)
    elif d == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if g == - 1:
        _ononl_(t3)
    elif g == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _onl_()
    _onl_(t2)

    if b == - 1:
        _ononl_(t3)
    elif b == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if e == - 1:
        _ononl_(t3)
    elif e == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if h == - 1:
        _ononl_(t3)
    elif h == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _onl_()
    _onl_(t2)

    if c == - 1:
        _ononl_(t3)
    elif c == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if f == - 1:
        _ononl_(t3)
    elif f == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _ononl_(t1)

    if i == - 1:
        _ononl_(t3)
    elif i == 1:
        _ononl_(t4)
    else:
        _ononl_(t0)

    _onl_()

# Some usefus sums.
    sa = a + d + g
    sb = b + e + h
    sc = c + f + i
    sd = a + b + c
    se = d + e + f
    sf = g + h + i
    sg = a + e + i
    sh = c + e + g

    if sa*sb*sc*sd*se*sf*sg*sh + 3*sa*sb*sc*sd*se*sf*sg + 3*sa*sb*sc*sd*se*sf*sh + 9*sa*sb*sc*sd*se*sf + 3*sa*sb*sc*sd*se*sg*sh + 9*sa*sb*sc*sd*se*sg + 9*sa*sb*sc*sd*se*sh + 27*sa*sb*sc*sd*se + 3*sa*sb*sc*sd*sf*sg*sh + 9*sa*sb*sc*sd*sf*sg + 9*sa*sb*sc*sd*sf*sh + 27*sa*sb*sc*sd*sf + 9*sa*sb*sc*sd*sg*sh + 27*sa*sb*sc*sd*sg + 27*sa*sb*sc*sd*sh + 81*sa*sb*sc*sd + 3*sa*sb*sc*se*sf*sg*sh + 9*sa*sb*sc*se*sf*sg + 9*sa*sb*sc*se*sf*sh + 27*sa*sb*sc*se*sf + 9*sa*sb*sc*se*sg*sh + 27*sa*sb*sc*se*sg + 27*sa*sb*sc*se*sh + 81*sa*sb*sc*se + 9*sa*sb*sc*sf*sg*sh + 27*sa*sb*sc*sf*sg + 27*sa*sb*sc*sf*sh + 81*sa*sb*sc*sf + 27*sa*sb*sc*sg*sh + 81*sa*sb*sc*sg + 81*sa*sb*sc*sh + 243*sa*sb*sc + 3*sa*sb*sd*se*sf*sg*sh + 9*sa*sb*sd*se*sf*sg + 9*sa*sb*sd*se*sf*sh + 27*sa*sb*sd*se*sf + 9*sa*sb*sd*se*sg*sh + 27*sa*sb*sd*se*sg + 27*sa*sb*sd*se*sh + 81*sa*sb*sd*se + 9*sa*sb*sd*sf*sg*sh + 27*sa*sb*sd*sf*sg + 27*sa*sb*sd*sf*sh + 81*sa*sb*sd*sf + 27*sa*sb*sd*sg*sh + 81*sa*sb*sd*sg + 81*sa*sb*sd*sh + 243*sa*sb*sd + 9*sa*sb*se*sf*sg*sh + 27*sa*sb*se*sf*sg + 27*sa*sb*se*sf*sh + 81*sa*sb*se*sf + 27*sa*sb*se*sg*sh + 81*sa*sb*se*sg + 81*sa*sb*se*sh + 243*sa*sb*se + 27*sa*sb*sf*sg*sh + 81*sa*sb*sf*sg + 81*sa*sb*sf*sh + 243*sa*sb*sf + 81*sa*sb*sg*sh + 243*sa*sb*sg + 243*sa*sb*sh + 729*sa*sb + 3*sa*sc*sd*se*sf*sg*sh + 9*sa*sc*sd*se*sf*sg + 9*sa*sc*sd*se*sf*sh + 27*sa*sc*sd*se*sf + 9*sa*sc*sd*se*sg*sh + 27*sa*sc*sd*se*sg + 27*sa*sc*sd*se*sh + 81*sa*sc*sd*se + 9*sa*sc*sd*sf*sg*sh + 27*sa*sc*sd*sf*sg + 27*sa*sc*sd*sf*sh + 81*sa*sc*sd*sf + 27*sa*sc*sd*sg*sh + 81*sa*sc*sd*sg + 81*sa*sc*sd*sh + 243*sa*sc*sd + 9*sa*sc*se*sf*sg*sh + 27*sa*sc*se*sf*sg + 27*sa*sc*se*sf*sh + 81*sa*sc*se*sf + 27*sa*sc*se*sg*sh + 81*sa*sc*se*sg + 81*sa*sc*se*sh + 243*sa*sc*se + 27*sa*sc*sf*sg*sh + 81*sa*sc*sf*sg + 81*sa*sc*sf*sh + 243*sa*sc*sf + 81*sa*sc*sg*sh + 243*sa*sc*sg + 243*sa*sc*sh + 729*sa*sc + 9*sa*sd*se*sf*sg*sh + 27*sa*sd*se*sf*sg + 27*sa*sd*se*sf*sh + 81*sa*sd*se*sf + 27*sa*sd*se*sg*sh + 81*sa*sd*se*sg + 81*sa*sd*se*sh + 243*sa*sd*se + 27*sa*sd*sf*sg*sh + 81*sa*sd*sf*sg + 81*sa*sd*sf*sh + 243*sa*sd*sf + 81*sa*sd*sg*sh + 243*sa*sd*sg + 243*sa*sd*sh + 729*sa*sd + 27*sa*se*sf*sg*sh + 81*sa*se*sf*sg + 81*sa*se*sf*sh + 243*sa*se*sf + 81*sa*se*sg*sh + 243*sa*se*sg + 243*sa*se*sh + 729*sa*se + 81*sa*sf*sg*sh + 243*sa*sf*sg + 243*sa*sf*sh + 729*sa*sf + 243*sa*sg*sh + 729*sa*sg + 729*sa*sh + 2187*sa + 3*sb*sc*sd*se*sf*sg*sh + 9*sb*sc*sd*se*sf*sg + 9*sb*sc*sd*se*sf*sh + 27*sb*sc*sd*se*sf + 9*sb*sc*sd*se*sg*sh + 27*sb*sc*sd*se*sg + 27*sb*sc*sd*se*sh + 81*sb*sc*sd*se + 9*sb*sc*sd*sf*sg*sh + 27*sb*sc*sd*sf*sg + 27*sb*sc*sd*sf*sh + 81*sb*sc*sd*sf + 27*sb*sc*sd*sg*sh + 81*sb*sc*sd*sg + 81*sb*sc*sd*sh + 243*sb*sc*sd + 9*sb*sc*se*sf*sg*sh + 27*sb*sc*se*sf*sg + 27*sb*sc*se*sf*sh + 81*sb*sc*se*sf + 27*sb*sc*se*sg*sh + 81*sb*sc*se*sg + 81*sb*sc*se*sh + 243*sb*sc*se + 27*sb*sc*sf*sg*sh + 81*sb*sc*sf*sg + 81*sb*sc*sf*sh + 243*sb*sc*sf + 81*sb*sc*sg*sh + 243*sb*sc*sg + 243*sb*sc*sh + 729*sb*sc + 9*sb*sd*se*sf*sg*sh + 27*sb*sd*se*sf*sg + 27*sb*sd*se*sf*sh + 81*sb*sd*se*sf + 27*sb*sd*se*sg*sh + 81*sb*sd*se*sg + 81*sb*sd*se*sh + 243*sb*sd*se + 27*sb*sd*sf*sg*sh + 81*sb*sd*sf*sg + 81*sb*sd*sf*sh + 243*sb*sd*sf + 81*sb*sd*sg*sh + 243*sb*sd*sg + 243*sb*sd*sh + 729*sb*sd + 27*sb*se*sf*sg*sh + 81*sb*se*sf*sg + 81*sb*se*sf*sh + 243*sb*se*sf + 81*sb*se*sg*sh + 243*sb*se*sg + 243*sb*se*sh + 729*sb*se + 81*sb*sf*sg*sh + 243*sb*sf*sg + 243*sb*sf*sh + 729*sb*sf + 243*sb*sg*sh + 729*sb*sg + 729*sb*sh + 2187*sb + 9*sc*sd*se*sf*sg*sh + 27*sc*sd*se*sf*sg + 27*sc*sd*se*sf*sh + 81*sc*sd*se*sf + 27*sc*sd*se*sg*sh + 81*sc*sd*se*sg + 81*sc*sd*se*sh + 243*sc*sd*se + 27*sc*sd*sf*sg*sh + 81*sc*sd*sf*sg + 81*sc*sd*sf*sh + 243*sc*sd*sf + 81*sc*sd*sg*sh + 243*sc*sd*sg + 243*sc*sd*sh + 729*sc*sd + 27*sc*se*sf*sg*sh + 81*sc*se*sf*sg + 81*sc*se*sf*sh + 243*sc*se*sf + 81*sc*se*sg*sh + 243*sc*se*sg + 243*sc*se*sh + 729*sc*se + 81*sc*sf*sg*sh + 243*sc*sf*sg + 243*sc*sf*sh + 729*sc*sf + 243*sc*sg*sh + 729*sc*sg + 729*sc*sh + 2187*sc + 27*sd*se*sf*sg*sh + 81*sd*se*sf*sg + 81*sd*se*sf*sh + 243*sd*se*sf + 81*sd*se*sg*sh + 243*sd*se*sg + 243*sd*se*sh + 729*sd*se + 81*sd*sf*sg*sh + 243*sd*sf*sg + 243*sd*sf*sh + 729*sd*sf + 243*sd*sg*sh + 729*sd*sg + 729*sd*sh + 2187*sd + 81*se*sf*sg*sh + 243*se*sf*sg + 243*se*sf*sh + 729*se*sf + 243*se*sg*sh + 729*se*sg + 729*se*sh + 2187*se + 243*sf*sg*sh + 729*sf*sg + 729*sf*sh + 2187*sf + 729*sg*sh + 2187*sg + 2187*sh + 6561 == 0:
        _onl_()
        _onl_(t5)
        break
        
    elif sa*sb*sc*sd*se*sf*sg*sh - 3*sa*sb*sc*sd*se*sf*sg - 3*sa*sb*sc*sd*se*sf*sh + 9*sa*sb*sc*sd*se*sf - 3*sa*sb*sc*sd*se*sg*sh + 9*sa*sb*sc*sd*se*sg + 9*sa*sb*sc*sd*se*sh - 27*sa*sb*sc*sd*se - 3*sa*sb*sc*sd*sf*sg*sh + 9*sa*sb*sc*sd*sf*sg + 9*sa*sb*sc*sd*sf*sh - 27*sa*sb*sc*sd*sf + 9*sa*sb*sc*sd*sg*sh - 27*sa*sb*sc*sd*sg - 27*sa*sb*sc*sd*sh + 81*sa*sb*sc*sd - 3*sa*sb*sc*se*sf*sg*sh + 9*sa*sb*sc*se*sf*sg + 9*sa*sb*sc*se*sf*sh - 27*sa*sb*sc*se*sf + 9*sa*sb*sc*se*sg*sh - 27*sa*sb*sc*se*sg - 27*sa*sb*sc*se*sh + 81*sa*sb*sc*se + 9*sa*sb*sc*sf*sg*sh - 27*sa*sb*sc*sf*sg - 27*sa*sb*sc*sf*sh + 81*sa*sb*sc*sf - 27*sa*sb*sc*sg*sh + 81*sa*sb*sc*sg + 81*sa*sb*sc*sh - 243*sa*sb*sc - 3*sa*sb*sd*se*sf*sg*sh + 9*sa*sb*sd*se*sf*sg + 9*sa*sb*sd*se*sf*sh - 27*sa*sb*sd*se*sf + 9*sa*sb*sd*se*sg*sh - 27*sa*sb*sd*se*sg - 27*sa*sb*sd*se*sh + 81*sa*sb*sd*se + 9*sa*sb*sd*sf*sg*sh - 27*sa*sb*sd*sf*sg - 27*sa*sb*sd*sf*sh + 81*sa*sb*sd*sf - 27*sa*sb*sd*sg*sh + 81*sa*sb*sd*sg + 81*sa*sb*sd*sh - 243*sa*sb*sd + 9*sa*sb*se*sf*sg*sh - 27*sa*sb*se*sf*sg - 27*sa*sb*se*sf*sh + 81*sa*sb*se*sf - 27*sa*sb*se*sg*sh + 81*sa*sb*se*sg + 81*sa*sb*se*sh - 243*sa*sb*se - 27*sa*sb*sf*sg*sh + 81*sa*sb*sf*sg + 81*sa*sb*sf*sh - 243*sa*sb*sf + 81*sa*sb*sg*sh - 243*sa*sb*sg - 243*sa*sb*sh + 729*sa*sb - 3*sa*sc*sd*se*sf*sg*sh + 9*sa*sc*sd*se*sf*sg + 9*sa*sc*sd*se*sf*sh - 27*sa*sc*sd*se*sf + 9*sa*sc*sd*se*sg*sh - 27*sa*sc*sd*se*sg - 27*sa*sc*sd*se*sh + 81*sa*sc*sd*se + 9*sa*sc*sd*sf*sg*sh - 27*sa*sc*sd*sf*sg - 27*sa*sc*sd*sf*sh + 81*sa*sc*sd*sf - 27*sa*sc*sd*sg*sh + 81*sa*sc*sd*sg + 81*sa*sc*sd*sh - 243*sa*sc*sd + 9*sa*sc*se*sf*sg*sh - 27*sa*sc*se*sf*sg - 27*sa*sc*se*sf*sh + 81*sa*sc*se*sf - 27*sa*sc*se*sg*sh + 81*sa*sc*se*sg + 81*sa*sc*se*sh - 243*sa*sc*se - 27*sa*sc*sf*sg*sh + 81*sa*sc*sf*sg + 81*sa*sc*sf*sh - 243*sa*sc*sf + 81*sa*sc*sg*sh - 243*sa*sc*sg - 243*sa*sc*sh + 729*sa*sc + 9*sa*sd*se*sf*sg*sh - 27*sa*sd*se*sf*sg - 27*sa*sd*se*sf*sh + 81*sa*sd*se*sf - 27*sa*sd*se*sg*sh + 81*sa*sd*se*sg + 81*sa*sd*se*sh - 243*sa*sd*se - 27*sa*sd*sf*sg*sh + 81*sa*sd*sf*sg + 81*sa*sd*sf*sh - 243*sa*sd*sf + 81*sa*sd*sg*sh - 243*sa*sd*sg - 243*sa*sd*sh + 729*sa*sd - 27*sa*se*sf*sg*sh + 81*sa*se*sf*sg + 81*sa*se*sf*sh - 243*sa*se*sf + 81*sa*se*sg*sh - 243*sa*se*sg - 243*sa*se*sh + 729*sa*se + 81*sa*sf*sg*sh - 243*sa*sf*sg - 243*sa*sf*sh + 729*sa*sf - 243*sa*sg*sh + 729*sa*sg + 729*sa*sh - 2187*sa - 3*sb*sc*sd*se*sf*sg*sh + 9*sb*sc*sd*se*sf*sg + 9*sb*sc*sd*se*sf*sh - 27*sb*sc*sd*se*sf + 9*sb*sc*sd*se*sg*sh - 27*sb*sc*sd*se*sg - 27*sb*sc*sd*se*sh + 81*sb*sc*sd*se + 9*sb*sc*sd*sf*sg*sh - 27*sb*sc*sd*sf*sg - 27*sb*sc*sd*sf*sh + 81*sb*sc*sd*sf - 27*sb*sc*sd*sg*sh + 81*sb*sc*sd*sg + 81*sb*sc*sd*sh - 243*sb*sc*sd + 9*sb*sc*se*sf*sg*sh - 27*sb*sc*se*sf*sg - 27*sb*sc*se*sf*sh + 81*sb*sc*se*sf - 27*sb*sc*se*sg*sh + 81*sb*sc*se*sg + 81*sb*sc*se*sh - 243*sb*sc*se - 27*sb*sc*sf*sg*sh + 81*sb*sc*sf*sg + 81*sb*sc*sf*sh - 243*sb*sc*sf + 81*sb*sc*sg*sh - 243*sb*sc*sg - 243*sb*sc*sh + 729*sb*sc + 9*sb*sd*se*sf*sg*sh - 27*sb*sd*se*sf*sg - 27*sb*sd*se*sf*sh + 81*sb*sd*se*sf - 27*sb*sd*se*sg*sh + 81*sb*sd*se*sg + 81*sb*sd*se*sh - 243*sb*sd*se - 27*sb*sd*sf*sg*sh + 81*sb*sd*sf*sg + 81*sb*sd*sf*sh - 243*sb*sd*sf + 81*sb*sd*sg*sh - 243*sb*sd*sg - 243*sb*sd*sh + 729*sb*sd - 27*sb*se*sf*sg*sh + 81*sb*se*sf*sg + 81*sb*se*sf*sh - 243*sb*se*sf + 81*sb*se*sg*sh - 243*sb*se*sg - 243*sb*se*sh + 729*sb*se + 81*sb*sf*sg*sh - 243*sb*sf*sg - 243*sb*sf*sh + 729*sb*sf - 243*sb*sg*sh + 729*sb*sg + 729*sb*sh - 2187*sb + 9*sc*sd*se*sf*sg*sh - 27*sc*sd*se*sf*sg - 27*sc*sd*se*sf*sh + 81*sc*sd*se*sf - 27*sc*sd*se*sg*sh + 81*sc*sd*se*sg + 81*sc*sd*se*sh - 243*sc*sd*se - 27*sc*sd*sf*sg*sh + 81*sc*sd*sf*sg + 81*sc*sd*sf*sh - 243*sc*sd*sf + 81*sc*sd*sg*sh - 243*sc*sd*sg - 243*sc*sd*sh + 729*sc*sd - 27*sc*se*sf*sg*sh + 81*sc*se*sf*sg + 81*sc*se*sf*sh - 243*sc*se*sf + 81*sc*se*sg*sh - 243*sc*se*sg - 243*sc*se*sh + 729*sc*se + 81*sc*sf*sg*sh - 243*sc*sf*sg - 243*sc*sf*sh + 729*sc*sf - 243*sc*sg*sh + 729*sc*sg + 729*sc*sh - 2187*sc - 27*sd*se*sf*sg*sh + 81*sd*se*sf*sg + 81*sd*se*sf*sh - 243*sd*se*sf + 81*sd*se*sg*sh - 243*sd*se*sg - 243*sd*se*sh + 729*sd*se + 81*sd*sf*sg*sh - 243*sd*sf*sg - 243*sd*sf*sh + 729*sd*sf - 243*sd*sg*sh + 729*sd*sg + 729*sd*sh - 2187*sd + 81*se*sf*sg*sh - 243*se*sf*sg - 243*se*sf*sh + 729*se*sf - 243*se*sg*sh + 729*se*sg + 729*se*sh - 2187*se - 243*sf*sg*sh + 729*sf*sg + 729*sf*sh - 2187*sf + 729*sg*sh - 2187*sg - 2187*sh + 6561 == 0:
        _onl_()
        _onl_(t6)
        break
        
    elif (((((((((2)**a)**b)**c)**d)**e)**f)**g)**h)**i != 1:
        _onl_()
        _onl_(t7)
        break
    
# We can play...",
    else:
        _onl_()

        j = z

        while j:
            if x == 1:
                k = _i_(t8)

            else:
                k = _i_(t9)

            if k == "A1" and a == 0:
                a = x
                j = y

            elif k == "A2" and b == 0:
                b = x
                j = y

            elif k == "A3" and c == 0:
                c = x
                j = y

            elif k == "B1" and d == 0:
                d = x
                j = y

            elif k == "B2" and e == 0:
                e = x
                j = y

            elif k == "B3" and f == 0:
                f = x
                j = y

            elif k == "C1" and g == 0:
                g = x
                j = y

            elif k == "C2" and h == 0:
                h = x
                j = y

            elif k == "C3" and i == 0:
                i = x
                j = y

# The player changes.
        x = ~x+1