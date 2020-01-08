import tcod as libtcod
# import tcod.console as console

from enum import Enum
# from clubsandwich.ui import ScrollingTextView

from map_objects.map_colors import height_colors, height_colors_dark
from loader_functions.initialize_new_game import get_constants


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3
    PLAYER = 4


def render_all(con, UI, entities, player, game_map, fov_map, fov_recompute, fov_radius, message_log, game_time, screen_width, screen_height, colors):
    noise = libtcod.noise_new(1, 0.5, 2.0)
    fov_torchx = 2
    fov_torchx += 0.2
    tdx = [fov_torchx + 20.0]
    dx = libtcod.noise_get(noise, tdx, libtcod.NOISE_SIMPLEX) * 1.5
    tdx[0] += 30.0
    dy = libtcod.noise_get(noise, tdx, libtcod.NOISE_SIMPLEX) * 1.5
    di = 0.2 * libtcod.noise_get(noise, [fov_torchx], libtcod.NOISE_SIMPLEX)

    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].blocked
                if visible:
                    if wall:
                        light = height_colors(libtcod.heightmap_get_value(game_map.hm, x, y))
                        base = libtcod.color_lerp(colors.get('dark_wall'), height_colors(libtcod.heightmap_get_value(game_map.hm, x, y)), 0.3)
                    else:
                        libtcod.console_put_char_ex(con, x, y, 205, libtcod.white, libtcod.black)
                        light = height_colors_dark(libtcod.heightmap_get_value(game_map.hm, x, y))
                        base = libtcod.color_lerp(colors.get('dark_ground'), height_colors_dark(libtcod.heightmap_get_value(game_map.hm, x, y)), 0.3)
                    r = float(x - player.x + dx) * (x - player.x + dx) + \
                        (y - player.y + dy) * (y - player.y + dy)
                    if r < (fov_radius * fov_radius):
                        lp = ((fov_radius * fov_radius) - r) / (fov_radius * fov_radius) \
                            + di
                        if lp < 0.0:
                            lp = 0.0
                        elif lp > 1.0:
                            lp = 1.0
                        base = libtcod.color_lerp(base, light, lp)
                    libtcod.console_set_char_background(con, x, y, base, libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, libtcod.color_lerp(colors.get('dark_wall'), height_colors(libtcod.heightmap_get_value(game_map.hm, x, y)), 0.3), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, libtcod.color_lerp(colors.get('dark_ground'), height_colors_dark(libtcod.heightmap_get_value(game_map.hm, x, y)), 0.3), libtcod.BKGND_SET)
                        libtcod.console_put_char_ex(con, x, y, 205, libtcod.grey, libtcod.color_lerp(colors.get('dark_ground'), height_colors_dark(libtcod.heightmap_get_value(game_map.hm, x, y)), 0.3))

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

# UI rendering:
    libtcod.console_set_default_background(UI, libtcod.black)
    libtcod.console_clear(UI)
    # Drawing boarders:
    UI.draw_frame(0, 0, get_constants()['UI_width'], get_constants()['UI_height'], "", False, fg=libtcod.white, bg=libtcod.black)
    UI.draw_frame(1, 2, 63, get_constants()['UI_height'] - 3, "", False, fg=libtcod.white, bg=libtcod.black)
    UI.vline(get_constants()['UI_width'] - 55, 1, get_constants()['UI_height'] - 2)
    UI.vline(64, 1, get_constants()['UI_height'] - 2)
    # Print Static Tool Tips:
    UI.print(65, 1, "A:\nc:\nx:\nr:\nz:\nn:\nl:\nq:\nR:", fg=libtcod.green)
    UI.print(68, 1, "Announcements\nCrew\nSquads\nView Cabins\nStatus\nNobles/Admin.\nLook\nSet Task/Pref\nReports", fg=libtcod.white)
    UI.print(83, 1, "j/k:\nwasd:\ne:", fg=libtcod.green)
    UI.print(89, 1, "speed Up/Down\nChange Direction\nEMERGENCY Stop", fg=libtcod.white)
    UI.print(65, 17, "Space:", fg=libtcod.green)
    UI.print(72, 17, "Pause", fg=libtcod.white)
    UI.print(83, 17, ".:", fg=libtcod.green)
    UI.print(89, 17, "One Step", fg=libtcod.white)
    # Scrolling text placeholder:
    # lets_scroll = ScrollingTextView(UI_height - 5, 61)
    # Console.blit(con, 3, get_constants()['map_height'] + 3, 0, 0, 0, 0)
# Changing text:
    libtcod.console_set_default_foreground(UI, libtcod.white)
    # Date/Time Placeholder
    libtcod.console_print_ex(UI, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, f'{game_time.days:02d} {game_time.month_name[int(game_time.months)][:3]} {game_time.years} | {game_time.twelve_hour_clock()}:{game_time.minutes:02d} {game_time.am_or_pm()} | 90 F')
    # Status
    libtcod.console_print_ex(UI, get_constants()['UI_width'] - 53, get_constants()['UI_height'] - 13, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Health: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))
    libtcod.console_print_ex(UI, get_constants()['UI_width'] - 53, get_constants()['UI_height'] - 12, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Status: {0:02}/{1:02}'.format(player.fighter.defense, player.fighter.max_defense))
    libtcod.console_print_ex(UI, get_constants()['UI_width'] - 53, get_constants()['UI_height'] - 11, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Fuel  :')
    libtcod.console_print_ex(UI, get_constants()['UI_width'] - 53, get_constants()['UI_height'] - 10, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Speed :')
    # PLayer Title, outline, and stats
    UI.print(get_constants()['UI_width'] - 53, 1, "Loco.", fg=libtcod.white)
    UI.print(get_constants()['UI_width'] - 53, 2, "<[   ]", fg=libtcod.white)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 51, 2, 219, libtcod.color_lerp(libtcod.red, libtcod.green, (player.fighter.hp / player.fighter.max_hp)), libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 50, 2, 219, libtcod.color_lerp(libtcod.red, libtcod.green, (player.fighter.defense / player.fighter.max_defense)), libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 49, 2, 230, libtcod.color_lerp(libtcod.red, libtcod.green, 1.0), libtcod.black)
    car_count(0, UI)
    car_selection(0, UI)
    # Messages:
    y = 3
    for message in message_log.messages:
        libtcod.console_set_default_foreground(UI, message.color)
        libtcod.console_print_ex(UI, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1
    UI.blit(con, 0, get_constants()['map_height'], 0, 0, 0, 0)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)


def car_count(number_of_cars, UI):
    if number_of_cars >= 1:
        UI.print(get_constants()['UI_width'] - 47, 1, "1")
        UI.print(get_constants()['UI_width'] - 47, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 46, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 45, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 44, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 2:
        UI.print(get_constants()['UI_width'] - 42, 1, "2")
        UI.print(get_constants()['UI_width'] - 42, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 41, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 40, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 39, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 3:
        UI.print(get_constants()['UI_width'] - 37, 1, "3")
        UI.print(get_constants()['UI_width'] - 37, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 36, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 35, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 34, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 4:
        UI.print(get_constants()['UI_width'] - 32, 1, "4")
        UI.print(get_constants()['UI_width'] - 32, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 31, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 30, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 29, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 5:
        UI.print(get_constants()['UI_width'] - 27, 1, "5")
        UI.print(get_constants()['UI_width'] - 27, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 26, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 25, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 24, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 6:
        UI.print(get_constants()['UI_width'] - 22, 1, "6")
        UI.print(get_constants()['UI_width'] - 22, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 21, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 20, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 19, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 7:
        UI.print(get_constants()['UI_width'] - 17, 1, "7")
        UI.print(get_constants()['UI_width'] - 17, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 16, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 15, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 14, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 8:
        UI.print(get_constants()['UI_width'] - 12, 1, "8")
        UI.print(get_constants()['UI_width'] - 12, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 11, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 10, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 9, 2, 7, libtcod.grey, libtcod.black)
    if number_of_cars >= 9:
        UI.print(get_constants()['UI_width'] - 7, 1, "9")
        UI.print(get_constants()['UI_width'] - 7, 2, "[   ]")
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 6, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 5, 2, 7, libtcod.grey, libtcod.black)
        libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 4, 2, 7, libtcod.grey, libtcod.black)


def car_selection(car_selected, UI):
    a = car_selected * 5
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 52 + a, 3, 192, libtcod.yellow, libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 51 + a, 3, 196, libtcod.yellow, libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 50 + a, 3, 196, libtcod.yellow, libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 49 + a, 3, 196, libtcod.yellow, libtcod.black)
    libtcod.console_put_char_ex(UI, get_constants()['UI_width'] - 48 + a, 3, 217, libtcod.yellow, libtcod.black)
