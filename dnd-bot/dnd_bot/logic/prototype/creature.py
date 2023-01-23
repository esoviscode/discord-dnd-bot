from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""

    def __init__(self, x=0, y=0, sprite=None, name='Creature', hp=0, strength=0, dexterity=0,
                 intelligence=0, charisma=0, perception=0, initiative=0, action_points=0,
                 level=0, drop_equipment: Equipment = None, drop_money=0, items=None, game_token='', look_direction='down'):
        super().__init__(x=x, y=y, sprite=sprite, name=name, fragile=True, game_token=game_token, look_direction=look_direction)
        if items is None:
            items = []
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.perception = perception
        self.initiative = initiative
        self.action_points = action_points
        self.level = level
        self.drop_equipment = drop_equipment
        self.drop_money = drop_money
        self.items = items
