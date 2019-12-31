import tcod as libtcod

from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.max_defense = defense
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        if self.defense > 0:
            self.defense -= amount
            if self.defense < 0:
                self.defense = 0
        elif self.defense == 0:
            self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []
        damage = self.power

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} damage.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
