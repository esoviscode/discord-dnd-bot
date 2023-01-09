from dnd_bot.logic.prototype.entity import Entity


class Creature(Entity):

    def __init__(self, entity_id: int, x: int, y: int, sprite, name: str, skill, hp: int, strength: int, dexterity: int,
                 intelligence: int, charisma: int, perception: int, initiative: int, action_points: int, level: int):
        super().__init__(entity_id, x, y, sprite, name, skill)
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.perception = perception
        self.initiative = initiative
        self.action_points = action_points
        self.level = level
