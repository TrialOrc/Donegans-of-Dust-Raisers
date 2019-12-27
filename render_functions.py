import tcod as libtcod


def render_all(con, entities, player, game_map, fov_map, fov_recompute, fov_radius, screen_width, screen_height, colors):
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
                        base = colors.get('dark_wall')
                        light = colors.get('light_wall')
                    else:
                        base = colors.get('dark_ground')
                        light = colors.get('light_ground')
                    r = float(x - player.x + dx) * (x - player.x + dx) + \
                        (y - player.y + dy) * (y - player.y + dy)
                    if r < (fov_radius * fov_radius):
                        l = ((fov_radius * fov_radius) - r) / (fov_radius * fov_radius) \
                            + di
                        if l < 0.0:
                            l = 0.0
                        elif l > 1.0:
                            l = 1.0
                        base = libtcod.color_lerp(base, light, l)
                    libtcod.console_set_char_background(con, x, y, base, libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map)

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
