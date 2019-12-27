import tcod as libtcod
from biome_colors import dark_land


class Noise:
    def __init__(self, game_map, type):

        noise = libtcod.noise_new(2)
        for y in range(2 * game_map.height):
            for x in range(2 * game_map.width):
                f = [1.0 * x / (2 * game_map.width) + 0.01,
                     1.0 * y / (2 * game_map.height) + 0.01]
        # Simplex FBM
        if self.type == 0:
            value = libtcod.noise_get_fbm(noise, f, 4.0, libtcod.NOISE_SIMPLEX)
        # Perlin FBM
        elif self.type == 1:
            value = libtcod.noise_get_fbm(noise, f, 4.0, libtcod.NOISE_PERLIN)

    def biome(self, con, game_map):
        x = [[Noise(0)]]
        y = [[Noise(1)]] / x
        for x in range(0, game_map.width):
            for y in range(0, game_map.height):
                libtcod.getPoint(x, y)
                libtcod.console_set_char_background(con, x, y, dark_land(x, y), libtcod.BKGND_SET)
