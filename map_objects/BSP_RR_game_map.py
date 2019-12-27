import tcod as libtcod
import numpy as np
import math
import collections

from map_objects.tile import Tile
# from map_objects.node import Node
from random import randint, choice
from loader_functions.initialize_new_game import get_constants
from scipy.spatial import KDTree


class GameMap:
    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        self.tiles = self.initilize_tiles()
        self.constants = get_constants()
        self.rooms = []
        self.connections = []

    def initilize_tiles(self):
        tiles = [[Tile(True, False) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_nodes, depth, min_size, player):
        self.rooms = []
        bsp = libtcod.bsp_new_with_size(3, 3, self.constants['map_width'] - 3, self.constants['map_height'] - 3)

        libtcod.bsp_split_recursive(bsp, 0, depth, min_size + 1, min_size + 1, 1.5, 1.5)

        libtcod.bsp_traverse_inverted_level_order(bsp, self.traverse_node)

        # player_room = choice(rooms)
        # rooms.remove(player_room)
        # player.x = player_room[0]
        # player.y = player_room[1]

    def traverse_node(self, node, dat):
        num_connected = 0

        path_map = libtcod.map_new(self.constants['map_width'] - 3, self.constants['map_height'] - 3)
        astar = libtcod.path.AStar(path_map, 0)

        full_rooms = True

        if libtcod.bsp_is_leaf(node):
            minx = node.x + 1
            maxx = node.x + node.w - 1
            miny = node.y + 1
            maxy = node.y + node.w - 1

            if maxx == self.constants['map_width'] - 3:
                maxx -= 1
            if maxy == self.constants['map_height'] - 3:
                maxy -= 1

            if full_rooms is False:
                minx = randint(minx, maxx - self.constants['min_size'] + 2)
                miny = randint(miny, maxy - self.constants['min_size'] + 2)
                maxx = randint(minx + self.constants['min_size'] - 1, maxx)
                maxy = randint(miny + self.constants['min_size'] - 1, maxy)

            node.x = minx
            node.y = miny
            node.w = maxx - minx + 1
            node.h = maxy - miny + 1
            node.cx = randint(node.x, node.x + node.w)
            node.cy = randint(node.y, node.y + node.h)

            if node.cx > 3 and node.cx <= self.constants['map_width'] - 3 and node.cy > 3 and node.cy <= self.constants['map_height'] - 3:
                self.tiles[node.cx][node.cy].blocked = False
                self.tiles[node.cx][node.cy].block_sight = False

            new_room = (node.cx, node.cy)

            self.rooms.append(new_room)

        else:
            for r in range(len(self.rooms) * 2):
                # Choose a random node.
                kdt = KDTree(self.rooms)
                n1 = choice(self.rooms)
                lc = int(len(self.rooms) / 2)
                idx, n2 = kdt.query(n1, k=lc)
                x2, y2 = self.rooms[n2[1]]
                x3, y3 = self.rooms[n2[2]]
                x4, y4 = self.rooms[n2[3]]
                xl, yl = self.rooms[n2[-1]]

                # A* a path between k=2 node
                for x in range(self.constants['map_width']):
                    for y in range(self.constants['map_height']):
                        libtcod.map_set_properties(path_map, x, y, True, True)
                new_connect = astar.get_path(n1[0], n1[1], x2, y2)
                new_connect2 = astar.get_path(n1[0], n1[1], x3, y3)
                new_connect3 = astar.get_path(n1[0], n1[1], x4, y4)
                new_connectl = astar.get_path(n1[0], n1[1], xl, yl)

                # if this connection intersects another, break
                for other_connect in self.connections:
                    if collections.Counter(new_connect) & collections.Counter(other_connect) != collections.Counter():
                        break
                    elif collections.Counter(new_connect2) & collections.Counter(other_connect[1:-1]) != collections.Counter():
                        break
                    elif collections.Counter(new_connect3) & collections.Counter(other_connect[1:-1]) != collections.Counter():
                        break
                    elif collections.Counter(new_connectl[1:-1]) & collections.Counter(other_connect[1:-1]) != collections.Counter():
                        break

                else:
                    # Make all tiles in path walkable
                    for x, y in new_connect:
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False
                    self.connections.append(new_connect)
                    num_connected += 1

                    for x, y in new_connect2:
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False
                    self.connections.append(new_connect)
                    num_connected += 1

                    for x, y in new_connect3:
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False
                    self.connections.append(new_connect)
                    num_connected += 1

                    for x, y in new_connectl:
                        self.tiles[x][y].blocked = False
                        self.tiles[x][y].block_sight = False
                    self.connections.append(new_connect)
                    num_connected += 1
            libtcod.path_delete(path_map)
            libtcod.path_delete(astar)

    def create_node(self, room):
        # go through the tiles in the node and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def get_dist(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def closest_point(self, points, target):
        tx, ty = target
        return min(points, key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
