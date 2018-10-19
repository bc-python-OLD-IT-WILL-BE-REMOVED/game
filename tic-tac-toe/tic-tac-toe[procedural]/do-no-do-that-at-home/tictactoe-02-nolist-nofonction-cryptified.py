# --------------- #
# -- CONSTANTS -- #
# --------------- #
# Some useful shortcuts.
__ = -1
___ = 0
____ = 1
_____ = 11
y = False
z = True
_i_ = input
_ononl_ = lambda _: print(_, end = '')
_onl_ = print
# Some useful texts. We use UNICODE codification because all programers know it.
t0 = "\u0020\u0020"
t1 = "\u0020\u007c"
t2 = "\u002d"*_____
t3 = "\u0020\u00d7"
t4 = "\u0020\u006f"
t5 = "\u0050\u006c\u0061\u0079\u0065\u0072\u0020\u0077\u0069\u0074\u0068\u0020\u005b\u0020\u00d7\u0020\u005d\u0020\u0077\u0069\u006e\u0073\u002e"
t6 = "\u0050\u006c\u0061\u0079\u0065\u0072\u0020\u0077\u0069\u0074\u0068\u0020\u005b\u0020\u006f\u0020\u005d\u0020\u0077\u0069\u006e\u0073\u002e"
t7 = "\u004e\u006f\u0020\u006f\u006e\u0065\u0020\u0077\u0069\u006e\u0073\u002e"
t8 = "\u0050\u006c\u0061\u0079\u0065\u0072\u0020\u0077\u0069\u0074\u0068\u0020\u005b\u0020\u006f\u0020\u005d\u002c\u0020\u0077\u0068\u0061\u0074\u0020\u0069\u0073\u0020\u0079\u006f\u0075\u0072\u0020\u0063\u0068\u006f\u0069\u0063\u0065\u0020\u003f\u0020\u0055\u0073\u0065\u0020\u0041\u0031\u0020\u006f\u0072\u0020\u0042\u0033\u0020\u0066\u006f\u0072\u0020\u0065\u0078\u0061\u006d\u0070\u006c\u0065\u0020\u003a\u0020"
t9 = "\u0050\u006c\u0061\u0079\u0065\u0072\u0020\u0077\u0069\u0074\u0068\u0020\u005b\u0020\u00d7\u0020\u005d\u002c\u0020\u0077\u0068\u0061\u0074\u0020\u0069\u0073\u0020\u0079\u006f\u0075\u0072\u0020\u0063\u0068\u006f\u0069\u0063\u0065\u0020\u003f\u0020\u0055\u0073\u0065\u0020\u0041\u0031\u0020\u006f\u0072\u0020\u0042\u0033\u0020\u0066\u006f\u0072\u0020\u0065\u0078\u0061\u006d\u0070\u006c\u0065\u0020\u003a\u0020"
#  x indicates the id of the player using the following conventions :
#
#  __ = ×  |  ___ = empty  |  ____ = o
x = __
# Codification of the grid
#
#   a  |  b  |  c
# -----------------
#   d  |  e  |  f
# -----------------
#   g  |  h  |  i
#
a = b = c = d = e = f = g = h = i = ___
# --------------- #
# -- MAIN LOOP -- #
# --------------- #
while z:
# Let's print the grid.
    _onl_()
    _ononl_(t3) if a == __ else _ononl_(t4) if a == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if d == __ else _ononl_(t4) if d == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if g == __ else _ononl_(t4) if g == ____ else _ononl_(t0)
    _onl_()
    _onl_(t2)
    _ononl_(t3) if b == __ else _ononl_(t4) if b == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if e == __ else _ononl_(t4) if e == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if h == __ else _ononl_(t4) if h == ____ else _ononl_(t0)
    _onl_()
    _onl_(t2)
    _ononl_(t3) if c == __ else _ononl_(t4) if c == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if f == __ else _ononl_(t4) if f == ____ else _ononl_(t0)
    _ononl_(t1)
    _ononl_(t3) if i == __ else _ononl_(t4) if i == ____ else _ononl_(t0)
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

    if sa*sb*sc*sd*se*sf*sg*sh + 3*sa*sb*sc*sd*se*sf*sg + 3*sa*sb*sc*sd*se*sf*sh + 9*sa*sb*sc*sd*se*sf + 3*sa*sb*sc*sd*se*sg*sh + 9*sa*sb*sc*sd*se*sg + 9*sa*sb*sc*sd*se*sh + 27*sa*sb*sc*sd*se + 3*sa*sb*sc*sd*sf*sg*sh + 9*sa*sb*sc*sd*sf*sg + 9*sa*sb*sc*sd*sf*sh + 27*sa*sb*sc*sd*sf + 9*sa*sb*sc*sd*sg*sh + 27*sa*sb*sc*sd*sg + 27*sa*sb*sc*sd*sh + 81*sa*sb*sc*sd + 3*sa*sb*sc*se*sf*sg*sh + 9*sa*sb*sc*se*sf*sg + 9*sa*sb*sc*se*sf*sh + 27*sa*sb*sc*se*sf + 9*sa*sb*sc*se*sg*sh + 27*sa*sb*sc*se*sg + 27*sa*sb*sc*se*sh + 81*sa*sb*sc*se + 9*sa*sb*sc*sf*sg*sh + 27*sa*sb*sc*sf*sg + 27*sa*sb*sc*sf*sh + 81*sa*sb*sc*sf + 27*sa*sb*sc*sg*sh + 81*sa*sb*sc*sg + 81*sa*sb*sc*sh + 243*sa*sb*sc + 3*sa*sb*sd*se*sf*sg*sh + 9*sa*sb*sd*se*sf*sg + 9*sa*sb*sd*se*sf*sh + 27*sa*sb*sd*se*sf + 9*sa*sb*sd*se*sg*sh + 27*sa*sb*sd*se*sg + 27*sa*sb*sd*se*sh + 81*sa*sb*sd*se + 9*sa*sb*sd*sf*sg*sh + 27*sa*sb*sd*sf*sg + 27*sa*sb*sd*sf*sh + 81*sa*sb*sd*sf + 27*sa*sb*sd*sg*sh + 81*sa*sb*sd*sg + 81*sa*sb*sd*sh + 243*sa*sb*sd + 9*sa*sb*se*sf*sg*sh + 27*sa*sb*se*sf*sg + 27*sa*sb*se*sf*sh + 81*sa*sb*se*sf + 27*sa*sb*se*sg*sh + 81*sa*sb*se*sg + 81*sa*sb*se*sh + 243*sa*sb*se + 27*sa*sb*sf*sg*sh + 81*sa*sb*sf*sg + 81*sa*sb*sf*sh + 243*sa*sb*sf + 81*sa*sb*sg*sh + 243*sa*sb*sg + 243*sa*sb*sh + 729*sa*sb + 3*sa*sc*sd*se*sf*sg*sh + 9*sa*sc*sd*se*sf*sg + 9*sa*sc*sd*se*sf*sh + 27*sa*sc*sd*se*sf + 9*sa*sc*sd*se*sg*sh + 27*sa*sc*sd*se*sg + 27*sa*sc*sd*se*sh + 81*sa*sc*sd*se + 9*sa*sc*sd*sf*sg*sh + 27*sa*sc*sd*sf*sg + 27*sa*sc*sd*sf*sh + 81*sa*sc*sd*sf + 27*sa*sc*sd*sg*sh + 81*sa*sc*sd*sg + 81*sa*sc*sd*sh + 243*sa*sc*sd + 9*sa*sc*se*sf*sg*sh + 27*sa*sc*se*sf*sg + 27*sa*sc*se*sf*sh + 81*sa*sc*se*sf + 27*sa*sc*se*sg*sh + 81*sa*sc*se*sg + 81*sa*sc*se*sh + 243*sa*sc*se + 27*sa*sc*sf*sg*sh + 81*sa*sc*sf*sg + 81*sa*sc*sf*sh + 243*sa*sc*sf + 81*sa*sc*sg*sh + 243*sa*sc*sg + 243*sa*sc*sh + 729*sa*sc + 9*sa*sd*se*sf*sg*sh + 27*sa*sd*se*sf*sg + 27*sa*sd*se*sf*sh + 81*sa*sd*se*sf + 27*sa*sd*se*sg*sh + 81*sa*sd*se*sg + 81*sa*sd*se*sh + 243*sa*sd*se + 27*sa*sd*sf*sg*sh + 81*sa*sd*sf*sg + 81*sa*sd*sf*sh + 243*sa*sd*sf + 81*sa*sd*sg*sh + 243*sa*sd*sg + 243*sa*sd*sh + 729*sa*sd + 27*sa*se*sf*sg*sh + 81*sa*se*sf*sg + 81*sa*se*sf*sh + 243*sa*se*sf + 81*sa*se*sg*sh + 243*sa*se*sg + 243*sa*se*sh + 729*sa*se + 81*sa*sf*sg*sh + 243*sa*sf*sg + 243*sa*sf*sh + 729*sa*sf + 243*sa*sg*sh + 729*sa*sg + 729*sa*sh + 2187*sa + 3*sb*sc*sd*se*sf*sg*sh + 9*sb*sc*sd*se*sf*sg + 9*sb*sc*sd*se*sf*sh + 27*sb*sc*sd*se*sf + 9*sb*sc*sd*se*sg*sh + 27*sb*sc*sd*se*sg + 27*sb*sc*sd*se*sh + 81*sb*sc*sd*se + 9*sb*sc*sd*sf*sg*sh + 27*sb*sc*sd*sf*sg + 27*sb*sc*sd*sf*sh + 81*sb*sc*sd*sf + 27*sb*sc*sd*sg*sh + 81*sb*sc*sd*sg + 81*sb*sc*sd*sh + 243*sb*sc*sd + 9*sb*sc*se*sf*sg*sh + 27*sb*sc*se*sf*sg + 27*sb*sc*se*sf*sh + 81*sb*sc*se*sf + 27*sb*sc*se*sg*sh + 81*sb*sc*se*sg + 81*sb*sc*se*sh + 243*sb*sc*se + 27*sb*sc*sf*sg*sh + 81*sb*sc*sf*sg + 81*sb*sc*sf*sh + 243*sb*sc*sf + 81*sb*sc*sg*sh + 243*sb*sc*sg + 243*sb*sc*sh + 729*sb*sc + 9*sb*sd*se*sf*sg*sh + 27*sb*sd*se*sf*sg + 27*sb*sd*se*sf*sh + 81*sb*sd*se*sf + 27*sb*sd*se*sg*sh + 81*sb*sd*se*sg + 81*sb*sd*se*sh + 243*sb*sd*se + 27*sb*sd*sf*sg*sh + 81*sb*sd*sf*sg + 81*sb*sd*sf*sh + 243*sb*sd*sf + 81*sb*sd*sg*sh + 243*sb*sd*sg + 243*sb*sd*sh + 729*sb*sd + 27*sb*se*sf*sg*sh + 81*sb*se*sf*sg + 81*sb*se*sf*sh + 243*sb*se*sf + 81*sb*se*sg*sh + 243*sb*se*sg + 243*sb*se*sh + 729*sb*se + 81*sb*sf*sg*sh + 243*sb*sf*sg + 243*sb*sf*sh + 729*sb*sf + 243*sb*sg*sh + 729*sb*sg + 729*sb*sh + 2187*sb + 9*sc*sd*se*sf*sg*sh + 27*sc*sd*se*sf*sg + 27*sc*sd*se*sf*sh + 81*sc*sd*se*sf + 27*sc*sd*se*sg*sh + 81*sc*sd*se*sg + 81*sc*sd*se*sh + 243*sc*sd*se + 27*sc*sd*sf*sg*sh + 81*sc*sd*sf*sg + 81*sc*sd*sf*sh + 243*sc*sd*sf + 81*sc*sd*sg*sh + 243*sc*sd*sg + 243*sc*sd*sh + 729*sc*sd + 27*sc*se*sf*sg*sh + 81*sc*se*sf*sg + 81*sc*se*sf*sh + 243*sc*se*sf + 81*sc*se*sg*sh + 243*sc*se*sg + 243*sc*se*sh + 729*sc*se + 81*sc*sf*sg*sh + 243*sc*sf*sg + 243*sc*sf*sh + 729*sc*sf + 243*sc*sg*sh + 729*sc*sg + 729*sc*sh + 2187*sc + 27*sd*se*sf*sg*sh + 81*sd*se*sf*sg + 81*sd*se*sf*sh + 243*sd*se*sf + 81*sd*se*sg*sh + 243*sd*se*sg + 243*sd*se*sh + 729*sd*se + 81*sd*sf*sg*sh + 243*sd*sf*sg + 243*sd*sf*sh + 729*sd*sf + 243*sd*sg*sh + 729*sd*sg + 729*sd*sh + 2187*sd + 81*se*sf*sg*sh + 243*se*sf*sg + 243*se*sf*sh + 729*se*sf + 243*se*sg*sh + 729*se*sg + 729*se*sh + 2187*se + 243*sf*sg*sh + 729*sf*sg + 729*sf*sh + 2187*sf + 729*sg*sh + 2187*sg + 2187*sh + 6561 == ___:
        _onl_()
        _onl_(t5)
        break
    elif sa*sb*sc*sd*se*sf*sg*sh - 3*sa*sb*sc*sd*se*sf*sg - 3*sa*sb*sc*sd*se*sf*sh + 9*sa*sb*sc*sd*se*sf - 3*sa*sb*sc*sd*se*sg*sh + 9*sa*sb*sc*sd*se*sg + 9*sa*sb*sc*sd*se*sh - 27*sa*sb*sc*sd*se - 3*sa*sb*sc*sd*sf*sg*sh + 9*sa*sb*sc*sd*sf*sg + 9*sa*sb*sc*sd*sf*sh - 27*sa*sb*sc*sd*sf + 9*sa*sb*sc*sd*sg*sh - 27*sa*sb*sc*sd*sg - 27*sa*sb*sc*sd*sh + 81*sa*sb*sc*sd - 3*sa*sb*sc*se*sf*sg*sh + 9*sa*sb*sc*se*sf*sg + 9*sa*sb*sc*se*sf*sh - 27*sa*sb*sc*se*sf + 9*sa*sb*sc*se*sg*sh - 27*sa*sb*sc*se*sg - 27*sa*sb*sc*se*sh + 81*sa*sb*sc*se + 9*sa*sb*sc*sf*sg*sh - 27*sa*sb*sc*sf*sg - 27*sa*sb*sc*sf*sh + 81*sa*sb*sc*sf - 27*sa*sb*sc*sg*sh + 81*sa*sb*sc*sg + 81*sa*sb*sc*sh - 243*sa*sb*sc - 3*sa*sb*sd*se*sf*sg*sh + 9*sa*sb*sd*se*sf*sg + 9*sa*sb*sd*se*sf*sh - 27*sa*sb*sd*se*sf + 9*sa*sb*sd*se*sg*sh - 27*sa*sb*sd*se*sg - 27*sa*sb*sd*se*sh + 81*sa*sb*sd*se + 9*sa*sb*sd*sf*sg*sh - 27*sa*sb*sd*sf*sg - 27*sa*sb*sd*sf*sh + 81*sa*sb*sd*sf - 27*sa*sb*sd*sg*sh + 81*sa*sb*sd*sg + 81*sa*sb*sd*sh - 243*sa*sb*sd + 9*sa*sb*se*sf*sg*sh - 27*sa*sb*se*sf*sg - 27*sa*sb*se*sf*sh + 81*sa*sb*se*sf - 27*sa*sb*se*sg*sh + 81*sa*sb*se*sg + 81*sa*sb*se*sh - 243*sa*sb*se - 27*sa*sb*sf*sg*sh + 81*sa*sb*sf*sg + 81*sa*sb*sf*sh - 243*sa*sb*sf + 81*sa*sb*sg*sh - 243*sa*sb*sg - 243*sa*sb*sh + 729*sa*sb - 3*sa*sc*sd*se*sf*sg*sh + 9*sa*sc*sd*se*sf*sg + 9*sa*sc*sd*se*sf*sh - 27*sa*sc*sd*se*sf + 9*sa*sc*sd*se*sg*sh - 27*sa*sc*sd*se*sg - 27*sa*sc*sd*se*sh + 81*sa*sc*sd*se + 9*sa*sc*sd*sf*sg*sh - 27*sa*sc*sd*sf*sg - 27*sa*sc*sd*sf*sh + 81*sa*sc*sd*sf - 27*sa*sc*sd*sg*sh + 81*sa*sc*sd*sg + 81*sa*sc*sd*sh - 243*sa*sc*sd + 9*sa*sc*se*sf*sg*sh - 27*sa*sc*se*sf*sg - 27*sa*sc*se*sf*sh + 81*sa*sc*se*sf - 27*sa*sc*se*sg*sh + 81*sa*sc*se*sg + 81*sa*sc*se*sh - 243*sa*sc*se - 27*sa*sc*sf*sg*sh + 81*sa*sc*sf*sg + 81*sa*sc*sf*sh - 243*sa*sc*sf + 81*sa*sc*sg*sh - 243*sa*sc*sg - 243*sa*sc*sh + 729*sa*sc + 9*sa*sd*se*sf*sg*sh - 27*sa*sd*se*sf*sg - 27*sa*sd*se*sf*sh + 81*sa*sd*se*sf - 27*sa*sd*se*sg*sh + 81*sa*sd*se*sg + 81*sa*sd*se*sh - 243*sa*sd*se - 27*sa*sd*sf*sg*sh + 81*sa*sd*sf*sg + 81*sa*sd*sf*sh - 243*sa*sd*sf + 81*sa*sd*sg*sh - 243*sa*sd*sg - 243*sa*sd*sh + 729*sa*sd - 27*sa*se*sf*sg*sh + 81*sa*se*sf*sg + 81*sa*se*sf*sh - 243*sa*se*sf + 81*sa*se*sg*sh - 243*sa*se*sg - 243*sa*se*sh + 729*sa*se + 81*sa*sf*sg*sh - 243*sa*sf*sg - 243*sa*sf*sh + 729*sa*sf - 243*sa*sg*sh + 729*sa*sg + 729*sa*sh - 2187*sa - 3*sb*sc*sd*se*sf*sg*sh + 9*sb*sc*sd*se*sf*sg + 9*sb*sc*sd*se*sf*sh - 27*sb*sc*sd*se*sf + 9*sb*sc*sd*se*sg*sh - 27*sb*sc*sd*se*sg - 27*sb*sc*sd*se*sh + 81*sb*sc*sd*se + 9*sb*sc*sd*sf*sg*sh - 27*sb*sc*sd*sf*sg - 27*sb*sc*sd*sf*sh + 81*sb*sc*sd*sf - 27*sb*sc*sd*sg*sh + 81*sb*sc*sd*sg + 81*sb*sc*sd*sh - 243*sb*sc*sd + 9*sb*sc*se*sf*sg*sh - 27*sb*sc*se*sf*sg - 27*sb*sc*se*sf*sh + 81*sb*sc*se*sf - 27*sb*sc*se*sg*sh + 81*sb*sc*se*sg + 81*sb*sc*se*sh - 243*sb*sc*se - 27*sb*sc*sf*sg*sh + 81*sb*sc*sf*sg + 81*sb*sc*sf*sh - 243*sb*sc*sf + 81*sb*sc*sg*sh - 243*sb*sc*sg - 243*sb*sc*sh + 729*sb*sc + 9*sb*sd*se*sf*sg*sh - 27*sb*sd*se*sf*sg - 27*sb*sd*se*sf*sh + 81*sb*sd*se*sf - 27*sb*sd*se*sg*sh + 81*sb*sd*se*sg + 81*sb*sd*se*sh - 243*sb*sd*se - 27*sb*sd*sf*sg*sh + 81*sb*sd*sf*sg + 81*sb*sd*sf*sh - 243*sb*sd*sf + 81*sb*sd*sg*sh - 243*sb*sd*sg - 243*sb*sd*sh + 729*sb*sd - 27*sb*se*sf*sg*sh + 81*sb*se*sf*sg + 81*sb*se*sf*sh - 243*sb*se*sf + 81*sb*se*sg*sh - 243*sb*se*sg - 243*sb*se*sh + 729*sb*se + 81*sb*sf*sg*sh - 243*sb*sf*sg - 243*sb*sf*sh + 729*sb*sf - 243*sb*sg*sh + 729*sb*sg + 729*sb*sh - 2187*sb + 9*sc*sd*se*sf*sg*sh - 27*sc*sd*se*sf*sg - 27*sc*sd*se*sf*sh + 81*sc*sd*se*sf - 27*sc*sd*se*sg*sh + 81*sc*sd*se*sg + 81*sc*sd*se*sh - 243*sc*sd*se - 27*sc*sd*sf*sg*sh + 81*sc*sd*sf*sg + 81*sc*sd*sf*sh - 243*sc*sd*sf + 81*sc*sd*sg*sh - 243*sc*sd*sg - 243*sc*sd*sh + 729*sc*sd - 27*sc*se*sf*sg*sh + 81*sc*se*sf*sg + 81*sc*se*sf*sh - 243*sc*se*sf + 81*sc*se*sg*sh - 243*sc*se*sg - 243*sc*se*sh + 729*sc*se + 81*sc*sf*sg*sh - 243*sc*sf*sg - 243*sc*sf*sh + 729*sc*sf - 243*sc*sg*sh + 729*sc*sg + 729*sc*sh - 2187*sc - 27*sd*se*sf*sg*sh + 81*sd*se*sf*sg + 81*sd*se*sf*sh - 243*sd*se*sf + 81*sd*se*sg*sh - 243*sd*se*sg - 243*sd*se*sh + 729*sd*se + 81*sd*sf*sg*sh - 243*sd*sf*sg - 243*sd*sf*sh + 729*sd*sf - 243*sd*sg*sh + 729*sd*sg + 729*sd*sh - 2187*sd + 81*se*sf*sg*sh - 243*se*sf*sg - 243*se*sf*sh + 729*se*sf - 243*se*sg*sh + 729*se*sg + 729*se*sh - 2187*se - 243*sf*sg*sh + 729*sf*sg + 729*sf*sh - 2187*sf + 729*sg*sh - 2187*sg - 2187*sh + 6561 == ___:
        _onl_()
        _onl_(t6)
        break
    elif (((((((((2)**a)**b)**c)**d)**e)**f)**g)**h)**i != ____:
        _onl_()
        _onl_(t7)
        break
# We can play...",
    else:
        _onl_()
        j = z
        while j:
            k = _i_(t8) if x == ____ else _i_(t9)
            nv1, nv2 = ("\u0061", "\u006a") if k == "\u0041\u0031" and a == ___ else ("\u0062", "\u006a") if k == "\u0041\u0032" and b == ___ else ("\u0063", "\u006a") if k == "\u0041\u0033" and c == ___ else ("\u0064", "\u006a") if k == "\u0042\u0031" and d == ___ else ("\u0065", "\u006a") if k == "\u0042\u0032" and e == ___ else ("\u0066", "\u006a") if k == "\u0042\u0033" and f == ___ else ("\u0067", "\u006a") if k == "\u0043\u0031" and g == ___ else ("\u0068", "\u006a") if k == "\u0043\u0032" and h == ___ else ("\u0069", "\u006a") if k == "\u0043\u0033" and i == ___ else BUG
            vars()[nv1], vars()[nv2] = x, y
# The player changes.
        x = ~x + ____