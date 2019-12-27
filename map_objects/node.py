class Node:
    # "Node" is a 1x1 spot that is randomly placed for rails("tunnel") to connect to.
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x + 1
        self.y2 = y + 1

    def center(self):
        center_x = self.x1
        center_y = self.y1
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y2)
