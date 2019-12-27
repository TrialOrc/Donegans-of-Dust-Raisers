class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


def get_entities_in_melee_range(entities, player):
    x = player.x - 1, player.x, player.x + 1
    y = player.y - 1, player.y, player.y + 1
    for entity in entities:
        if entity != player:
            for a in x:
                for b in y:
                    if entity.x == a and entity.y == player.y or entity.y == b and entity.x == player.x:
                        return entity

    return None
