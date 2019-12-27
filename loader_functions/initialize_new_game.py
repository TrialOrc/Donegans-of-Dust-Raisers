import tcod as libtcod


def get_constants():
    window_title = 'Trainz'

    screen_width = 160
    screen_height = 90
    map_width = 160
    map_height = 80

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
        'dark_wall': libtcod.Color(0, 0, 100),  # dark_land?
        'dark_ground': libtcod.Color(50, 50, 150),  # dark_track?
        'light_wall': libtcod.Color(130, 110, 50),  # light_land?
        'light_ground': libtcod.Color(200, 180, 50),
        'debug': libtcod.Color(255, 0, 255)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        # 'bar_width': bar_width,
        # 'panel_height': panel_height,
        # 'panel_y': panel_y,
        # 'message_x': message_x,
        # 'message_width': message_width,
        # 'message_height': message_height,
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
