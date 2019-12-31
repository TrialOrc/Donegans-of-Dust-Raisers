import tcod as libtcod


def get_constants():
    window_title = 'Donegans of Dust-Raisers'

    screen_width = 160
    screen_height = 100
    map_width = 160
    map_height = 80
    UI_width = screen_width
    UI_height = screen_height - map_height
    message_x = 2
    message_y = 17
    message_width = 61
    message_height = UI_height - 5

    room_max_size = 1
    room_min_size = 1
    max_rooms = 10
    depth = 5
    min_size = 10
    full_rooms = False

    fov_algorithm = 2
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 20

    player_speed = 2
    default_speed = 8
    defult_attack_speed = 20

    colors = {
        'dark_wall': libtcod.Color(0, 0, 50),  # dark_land?
        'dark_ground': libtcod.Color(25, 25, 75),  # dark_track?
        'light_wall': libtcod.Color(130, 110, 50),  # light_land?
        'light_ground': libtcod.Color(200, 180, 50),
        'debug': libtcod.Color(255, 0, 255),
        'black': libtcod.Color(0, 0, 0),
        'blue': libtcod.Color(0, 0, 255),
        'light_blue': libtcod.Color(63, 63, 255),
        'light_yellow': libtcod.Color(255, 255, 63),
        'green': libtcod.Color(0, 255, 0),
        'light_green': libtcod.Color(63, 255, 63),
        'desat_green': libtcod.Color(63, 127, 63),
        'dark_green': libtcod.Color(0, 191, 0),
        'grey': libtcod.Color(127, 127, 127),
        'silver': libtcod.Color(203, 203, 203)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'UI_width': UI_width,
        'UI_height': UI_height,
        'message_x': message_x,
        'message_y': message_y,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'depth': depth,
        'min_size': min_size,
        'full_rooms': full_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        # 'max_items_per_room': max_items_per_room,
        'player_speed': player_speed,
        'default_speed': default_speed,
        'default_attack_speed': defult_attack_speed,
        'colors': colors
    }

    return constants
