import tcod as libtcod


from loader_functions.initialize_new_game import get_constants


def biome_colors(x, y):
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


def height_colors(cellheight):
    constants = get_constants()
    if cellheight <= 2.5:
        return constants['colors'].get('blue')
    if cellheight <= 3:
        return constants['colors'].get('light_blue')
    if cellheight <= 3.5:
        return constants['colors'].get('light_yellow')
    if cellheight <= 6.7:
        return constants['colors'].get('green')
    if cellheight <= 9.9:
        return constants['colors'].get('light_green')
    if cellheight <= 13.1:
        return constants['colors'].get('desat_green')
    if cellheight <= 16.4:
        return constants['colors'].get('dark_green')
    if cellheight <= 19:
        return constants['colors'].get('grey')
    if cellheight <= 20:
        return constants['colors'].get('silver')
    else:
        return constants['colors'].get('debug')


def height_colors_dark(cellheight):
    constants = get_constants()
    if cellheight <= 3:
        return libtcod.Color(89, 38, 11)
    if cellheight <= 3.5:
        return libtcod.Color(204, 204, 50)
    if cellheight <= 6.7:
        return libtcod.Color(0, 204, 0)
    if cellheight <= 9.9:
        return libtcod.Color(50, 204, 50)
    if cellheight <= 13.1:
        return libtcod.Color(50, 102, 50)
    if cellheight <= 16.4:
        return libtcod.Color(0, 153, 0)
    if cellheight <= 19:
        return libtcod.Color(102, 102, 102)
    if cellheight <= 20:
        return libtcod.Color(162, 162, 162)
    else:
        return constants['colors'].get('debug')
