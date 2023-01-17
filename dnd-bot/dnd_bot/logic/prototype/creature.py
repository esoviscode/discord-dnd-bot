from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""
    def __init__(self, entity_id: int, x: int, y: int, sprite, name: str, skill, hp: int, strength: int, dexterity: int,
                 intelligence: int, charisma: int, perception: int, initiative: int, action_points: int, level: int,
                 drop_equipment: Equipment, drop_money: int, items=None):
        super().__init__(entity_id, x, y, sprite, name, skill)
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
