import tcod as libtcod
import tcod.console as console

from components.fighter import Fighter
from input_handlers import handle_keys
from loader_functions.initialize_new_game import get_constants
from map_objects.game_map import GameMap
from render_functions import render_all, clear_all, RenderOrder
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from entity import Entity, get_entities_in_melee_range, rail_check, path_change, dead_end
from death_functions import kill_player, kill_monster
from game_messages import MessageLog


def main():
    constants = get_constants()

    fighter_component = Fighter(hp=100, defense=10, power=16)
    player = Entity(0, 0, '@', libtcod.white, 'Player', render_order=RenderOrder.PLAYER, fighter=fighter_component, speed=2)
    entities = [player]

    libtcod.console_set_custom_font('cp437_10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False, libtcod.sys_set_renderer(libtcod.RENDERER_GLSL), 'F')
    # libtcod.sys_set_renderer(libtcod.RENDERER_GLSL)
    # libtcod.sys_set_fps(24)

    con = console.Console(constants['screen_width'], constants['screen_height'])
    UI = console.Console(get_constants()['screen_width'], get_constants()['UI_height'])

    game_map = GameMap(constants['map_width'], constants['map_height'])

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_map.make_map(constants['max_rooms'], constants['depth'], constants['min_size'], entities, constants['max_monsters_per_room'], fov_map, player)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    prev = []

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'],
                          constants['fov_light_walls'], constants['fov_algorithm'])

        render_all(con, UI, entities, player, game_map, fov_map, fov_recompute,
                   constants['fov_radius'], message_log, constants['screen_width'], constants['screen_height'], constants['colors'])

        libtcod.console_flush()

        fov_recompute = False

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if game_state == GameStates.PLAYERS_TURN:
            if len(prev) == 0:
                game_state = GameStates.MOVE

            else:
                prevx, prevy = prev[0]
                if rail_check(player, prevx, prevy, game_map) is True:
                    game_state = GameStates.MOVE

                else:
                    prevx, prevy = prev[0]
                    dx = player.x - prevx
                    dy = player.y - prevy

                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    prev.append((player.x, player.y))
                    del prev[0]

                    if not game_map.is_blocked(destination_x, destination_y):
                        player.move(dx, dy)

                        target = get_entities_in_melee_range(entities, player)

                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)

                        fov_recompute = True

                        # player.wait = player.speed

                        game_state = GameStates.ENEMY_TURN

                    elif game_map.is_blocked(destination_x, destination_y):
                        if rail_check(player, prevx, prevy, game_map) is False:
                            if path_change(player, prevx, prevy, game_map) is not None:
                                (destination_x, destination_y) = path_change(player, prevx, prevy, game_map)
                                dx = destination_x - player.x
                                dy = destination_y - player.y
                                prev.append((player.x, player.y))
                                player.move(dx, dy)
                                del prev[0]

                            else:
                                destination_x, destination_y = dead_end(player, game_map)
                                dx = destination_x - player.x
                                dy = destination_y - player.y
                                prev.append((player.x, player.y))
                                player.move(dx, dy)
                                del prev[0]

                            game_state = GameStates.ENEMY_TURN

                        else:
                            game_state = GameStates.MOVE

        if move and game_state == GameStates.MOVE:
            dx, dy = move
            if not len(prev) == 0:
                prevx, prevy = prev[0]
                if prevx == player.x + dx and prevy == player.y + dy:
                    print('Invalid Move')
                else:
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    prev.append((player.x, player.y))

                    if not game_map.is_blocked(destination_x, destination_y):
                        player.move(dx, dy)
                        if len(prev) > 1:
                            del prev[0]

                        target = get_entities_in_melee_range(entities, player)

                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)

                        fov_recompute = True

                        game_state = GameStates.ENEMY_TURN
            else:
                destination_x = player.x + dx
                destination_y = player.y + dy
                prev.append((player.x, player.y))

                if not game_map.is_blocked(destination_x, destination_y):
                    player.move(dx, dy)
                    if len(prev) > 1:
                        del prev[0]

                    target = get_entities_in_melee_range(entities, player)

                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                    fov_recompute = True

                    game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, gamestate = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
