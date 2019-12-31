import tcod as libtcod

from loader_functions.initialize_new_game import get_constants


def Noise(type):

    constants = get_constants()

    noise = libtcod.noise_new(2)
    for y in range(2 * constants['map_width']):
        for x in range(2 * constants['map_width']):
            f = [1.0 * x / (2 * constants['map_width']) + 0.01,
                 1.0 * y / (2 * constants['map_width']) + 0.01]
    # Simplex FBM
    if type == 0:
        S_FBM = libtcod.noise_get_fbm(noise, f, 4.0, libtcod.NOISE_SIMPLEX)
        return S_FBM
    # Perlin FBM
    elif type == 1:
        P_FBM = libtcod.noise_get_fbm(noise, f, 4.0, libtcod.NOISE_PERLIN)
        return P_FBM


def biome(self, con, game_map):
    x = [[Noise(0)]]
    y = [[Noise(1)]] / x
    for x in range(0, game_map.width):
        for y in range(0, game_map.height):
            libtcod.getPoint(x, y)
            libtcod.console_set_char_background(con, x, y, libtcod.blue, libtcod.BKGND_SET)


def heightmap(map):
    hght_noise = libtcod.noise.Noise(2, 1, 2, 0.9, 1.0, 2.0)
    constants = get_constants()
    hght_map = libtcod.heightmap_new(constants['map_width'], constants['map_height'])
    libtcod.heightmap_add_fbm(hght_map, hght_noise, 100.0, 100.0, 10.0, 10.0, 8.0, 2.0, 2.0)
    return hght_map
