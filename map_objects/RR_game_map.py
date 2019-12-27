import tcod as libtcod
import collections
import math

from map_objects.tile import Tile
from map_objects.node import Node
from random import randint, choice


class GameMap:
    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height
        self.tiles = self.initilize_tiles()
        # self.nodes = data if not data is None else []

    def initilize_tiles(self):
        tiles = [[Tile(True, False) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_nodes, map_width, map_height, player):
        path_map = libtcod.map_new(map_width, map_height)
        path = libtcod.path_new_using_map(path_map, 0)
        astar = libtcod.path.AStar(path_map, 0)

        nodes = []
        num_nodes = 0

        connections = []
        num_connected = 0

        # Change node section (lines 34 - 59) to use bsp to create better spaced nodes
        for r in range(max_nodes):
            # rand pos w/out going outside boundaries of map
            x = randint(0, map_width - 1)
            y = randint(0, map_height - 1)

            new_node = Node(x, y)

            for other_node in nodes:
                if new_node.intersect(other_node):
                    break

            else:
                self.create_node(new_node)

                (new_x, new_y) = new_node.center()

            if num_nodes == 0:
                player.x = new_x
                player.y = new_y
            else:
                (prev_x, prev_y) = nodes[num_nodes - 1].center()
                print(prev_x, prev_y)

            nodes.append(new_node)
            num_nodes += 1

        for r in range(max_nodes * 10):
            # Choose 2 random nodes.
            (n1x, n1y) = choice(nodes).center()
            (n2x, n2y) = choice(nodes).center()
            # Find a way to make (n2x, n2y) the closest node. This should probably be its own function.
            for other_node in nodes:
                (x2, y2) = other_node.center()
            if n1x == n2x and n1y == n2y:
                break

            # A* a path between two nodes
            for x in range(map_width):
                for y in range(map_height):
                    libtcod.map_set_properties(path_map, x, y, True, True)
            new_connect = astar.get_path(n1x, n1y, n2x, n2y)

            # if this connection intersects another, break
            for other_connect in connections:
                if collections.Counter(new_connect) & collections.Counter(other_connect) != collections.Counter():
                    break

            else:
                # Make all tiles in path walkable
                for x, y in new_connect:
                    # libtcod.path_get(new_connect, libtcod.path_size(new_connect))
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False

            connections.append(new_connect)
            num_connected += 1
        libtcod.path_delete(path)

    def create_node(self, room):
        # go through the tiles in the node and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
