from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment


class Enemy(Creature):

    def __init__(self, entity_id: int, x: int, y: int, sprite, name: str, skill, hp: int, strength: int, dexterity: int,
                 intelligence: int, charisma: int, perception: int, initiative: int, action_points: int, level: int,
                 drop_equipment: Equipment, drop_money: int):
        super().__init__(entity_id, x, y, sprite, name, skill, hp, strength, dexterity, intelligence, charisma,
                         perception, initiative, action_points, level)
        self.drop_equipment = drop_equipment
        self.drop_money = drop_money
