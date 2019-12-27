import tcod as libtcod


def handle_keys(key):
    # movement
    if key.c == 119:  # w
        return {'move': (0, -1)}
    elif key.c == 115:  # s
        return {'move': (0, 1)}
    elif key.c == 97:  # a
        return {'move': (-1, 0)}
    elif key.c == 100:  # d
        return {'move': (1, 0)}
    elif key.vk == libtcod.KEY_UP:
        return {'move': (0, 0)}

    # speed
    if key.c == 85:  # u
        return {'speed': (+ 1)}
    elif key.c == 74:  # j
        return {'speed': (- 1)}

    # emergency stop/ahead
    if key.c == 82:  # r
        return {'e_stop': True}
    elif key.c == 69:  # e
        return {'e_ahead': True}

    # Pause
    if key.vk == libtcod.KEY_SPACE:
        return {'Pause': True}

    # add '.' for step

    if key.vk == libtcod.KEY_F11:
        # fullscreen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key pressed
    return {}
