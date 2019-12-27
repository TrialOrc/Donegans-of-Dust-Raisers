import tcod as libtcod

from input_handlers import handle_keys
from loader_functions.initialize_new_game import get_constants
# from map_objects.game_map import GameMap
from map_objects.BSP_RR_game_map_test import GameMap
from render_functions import render_all, clear_all
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from entity import Entity, get_entities_in_melee_range


def main():
    constants = get_constants()

    player = Entity(0, 0, '@', libtcod.white, 'Player')
    entities = [player]

    libtcod.console_set_custom_font('cp437_10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)
    libtcod.sys_set_renderer(libtcod.RENDERER_GLSL)
    # libtcod.sys_set_fps(24)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])

    game_map = GameMap(constants['map_width'], constants['map_height'])
    fov_recompute = True

    fov_map = initialize_fov(game_map)
    # game_map
    # game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'],
    #                  constants['map_height'], player, entities, constants['max_monsters_per_room'])
    game_map.make_map(constants['max_rooms'], constants['depth'], constants['min_size'], entities, constants['max_monsters_per_room'], fov_map, player)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'],
                          constants['fov_light_walls'], constants['fov_algorithm'])

        render_all(con, entities, player, game_map, fov_map, fov_recompute,
                   constants['fov_radius'], constants['screen_width'], constants['screen_height'], constants['colors'])

        libtcod.console_flush()

        fov_recompute = False

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move

            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                player.move(dx, dy)
                target = get_entities_in_melee_range(entities, player)
                if target:
                    print(f'You kick the {target.name} in the shins, much to its annoyance!')

                fov_recompute = True

                player.wait = player.speed

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print(f'The {entity.name} waits.')
                entity.wait = entity.speed

            game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
