import tcod as libtcod
import tcod.bsp

from random import randint, choice
from scipy.spatial import KDTree

from map_objects.tile import Tile

from loader_functions.initialize_new_game import get_constants

from entity import Entity
from render_functions import RenderOrder

from components.fighter import Fighter
from components.ai import BasicMonster


class GameMap:
    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        self.tiles = self.initilize_tiles()
        self.constants = get_constants()

        self.connections = []
        self.bsp = libtcod.bsp_new_with_size(2, 2, self.width - 1, self.height - 1)

        noise = libtcod.noise.Noise(dimensions=2, algorithm=tcod.NOISE_PERLIN, implementation=tcod.noise.FBM, hurst=0.5, lacunarity=2.0, octaves=4.0)
        self.hm = libtcod.heightmap_new(self.width * 10, self.height * 10)
        libtcod.heightmap_add_fbm(self.hm, noise, 10.0, 10.0, 1.0, 1.0, 4.0, 10.0, 10.0)
        libtcod.heightmap_rain_erosion(self.hm, self.width * self.height, 0.4, 0.5)
        self.astar_map = self.hm.clip(0.1, 1.9)
        self.astar = libtcod.path.AStar(self.astar_map, 0)

    def initilize_tiles(self):
        tiles = [[Tile(True, False) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_nodes, depth, min_size, entities, max_monsters_per_room, fov_map, player):
        rooms = []
        num_connected = 0
        count = 0
        count2 = 1
        fail_count = 0

        for y in range(self.height):
            for x in range(self.width):
                if libtcod.heightmap_get_value(self.hm, x, y) <= 2.5:
                    libtcod.heightmap_set_value(self.astar_map, x, y, 5.0)

        libtcod.bsp_split_recursive(self.bsp, 0, depth, min_size, min_size, 1.5, 1.5)

        for node in self.bsp.inverted_level_order():
            if not node.children:
                minx = node.x
                maxx = node.x + node.w - 1
                miny = node.y
                maxy = node.y + node.w - 1

                if maxx == self.width:
                    maxx -= 1
                    if maxy == self.height:
                        maxy -= 1

                node.x = minx
                node.y = miny
                node.w = maxx - minx
                node.h = maxy - miny
                node.cx = randint(node.x, node.x + node.w)
                node.cy = randint(node.y, node.y + node.h)

                if node.cx >= 3 and node.cx <= self.width - 3 and node.cy >= 3 and node.cy <= self.height - 3:
                    self.tiles[node.cx][node.cy].blocked = False
                    self.tiles[node.cx][node.cy].block_sight = False

        for node in self.bsp.inverted_level_order():
            if not node.children:
                new_room = (node.cx, node.cy)

                rooms.append(new_room)

        # print('room count')
        # print(round(len(rooms) - 2))
        for node in self.bsp.inverted_level_order():
            if not node.children:
                continue
            while count2 != len(rooms) - 1:
                if fail_count == len(rooms) - 1:
                    break
                kdt = KDTree(rooms)         # Setting up KDTree
                # check if the current n1 is greater than last room
                if count > round(len(rooms) - 1):
                    # go to next nearest node. Restart n1 at first node.
                    # print(f'Count2 is: {count2}')
                    count2 += 1
                    fail_count = 0
                elif count2 == round(len(rooms) - 1):
                    break
                if count > round(len(rooms) - 1):
                    count = 0
                elif count2 == round(len(rooms) - 1):
                    break
                n1 = rooms[count]           # Grab room in rooms with index of count
                lc = round(len(rooms))    # lc is an integer of half total rooms in self.room
                dis, n2 = kdt.query(n1, k=lc)    # return distance(dis) and index(n2) of all rooms closest to n1 within half(lc) of all rooms.
                x2, y2 = rooms[n2[count2]]  # pull the (x, y) coordinates of room

                # create A* path from n1 to count2
                new_connect = self.astar.get_path(n1[0], n1[1], x2, y2)
                new_connect.append((x2, y2))
                new_connect.insert(0, (n1[0], n1[1]))

                # if this connection intersects another, break
                for other_connect in self.connections:
                    if len(new_connect) <= 2:
                        # print(f'Count {count} Failed: Empty connection')
                        count += 1  # Move to next n1 becuase this one won't work.
                        fail_count += 1
                        break
                    if self.out_of_bounds(new_connect) is True:
                        count += 1  # Move to next n1 becuase this one won't work.
                        fail_count += 1
                        break
                    if self.is_intersecting(new_connect[2:-2], other_connect[1:-1]) is True:
                        # print(f'Count {count} Failed: Intersects')
                        count += 1  # Move to next n1 becuase this one won't work.
                        fail_count += 1
                        break
                    if self.start_end_intersects(new_connect, other_connect) is True:
                        # print(f'Count {count} Failed: Destination and Origin already exists')
                        count += 1  # Move to next n1 becuase this one won't work.
                        fail_count += 1
                        break

                # If current n1 isn't > last n1
                # and If the connection doesn't intersect another
                # set this path as walkable.
                else:
                    # print(f'Count {count} Passed')
                    count += 1
                    fail_count = 0
                    for x, y in new_connect:
                        # print(new_connect)
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False
                # Add this connection to list of connections, and iterate number of connections.
                    self.connections.append(new_connect)

                    num_connected += 1

        player_room = choice(choice(self.connections))
        player.x = player_room[0]
        player.y = player_room[1]

        self.place_entities(self.connections, entities, max_monsters_per_room, fov_map, player)

    def is_intersecting(self, a, b):
        result = False
        for x in a:
            for y in b:
                if x == y:
                    result = True
                    return result
        return result

    def out_of_bounds(self, a):
        result = False
        for x, y in a:
            if x < 1 or x > self.width - 2:
                result = True
                return result
            if y < 1 or y > self.height - 2:
                result = True
                return result
        return result

    def start_end_intersects(self, a, b):
        c = [x for x in b if x != []]
        a = a[0], a[-1]
        c = c[0], c[-1]
        result = False
        crash = 0
        for y in c:
            for x in a:
                # print(x[0], x[-1], y[0], y[-1])
                if x[0] == y[0] and x[-1] == y[-1]:
                    crash += 1
                if x[0] == y[1] and x[-1] == y[0]:
                    crash += 1
                if x[-1] == y[1] and x[0] == y[0]:
                    crash += 1
                if x[-1] == y[0] and x[0] == y[-1]:
                    crash += 1
        if crash >= 4:
            # print(f'crash count is {crash}')
            result = True
            return result
        return result

    def place_entities(self, connections, entities, max_monsters_per_room, fov_map, player):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location
            monster_location = choice(choice(connections))
            if not libtcod.map_is_in_fov(fov_map, player.x, player.y):
                x = monster_location[0]
                y = monster_location[1]

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=30, defense=0, power=9)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'r', libtcod.desaturated_red, 'Raider', render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, speed=1)
                else:
                    fighter_component = Fighter(hp=48, defense=1, power=12)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'p', libtcod.darker_red, 'Pirate', render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, speed=2)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
