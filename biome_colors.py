import tcod as libtcod


def dark_land(x, y):
    if y < 0.2 and x < 0.9:
        libtcod.Color(213, 147, 79)
    elif y < 0.3 and y >= 0.2 and x < 0.4:
        libtcod.Color(176, 146, 71)
    elif y < 0.7 and y >= 0.3 and x < 0.4:
        libtcod.Color(41, 61, 26)
    elif y <= 1.0 and y >= 0.7 and x < 0.4:
        libtcod.Color(39, 87, 44)
    elif y < 0.3 and y >= 0.2 and x >= 0.4 and x < 0.7:
        libtcod.Color(167, 140, 47)
    elif y < 0.6 and y >= 0.3 and x >= 0.4 and x < 0.7:
        libtcod.Color(138, 121, 37)
    elif y < 0.8 and y >= 0.6 and x >= 0.4 and x < 0.6:
        libtcod.Color(99, 104, 44)
    elif y < 0.5 and y >= 0.2 and x >= 0.7 and x < 0.9:
        libtcod.Color(68, 118, 116)
    elif y < 0.3 and x >= 0.9:
        libtcod.Color(131, 128, 126)
    else:
        libtcod.Color(255, 0, 255)
