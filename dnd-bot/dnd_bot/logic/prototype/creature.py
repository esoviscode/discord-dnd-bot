from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""
    def __init__(self, entity_id: int=0, x: int=0, y: int=0, sprite=None, name: str='Creature', skill=None, hp: int=0, strength: int=0, dexterity: int=0,
                 intelligence: int=0, charisma: int=0, perception: int=0, initiative: int=0, action_points: int=0, level: int=0,
                 drop_equipment: Equipment=None, drop_money: int=0, items=None):
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
