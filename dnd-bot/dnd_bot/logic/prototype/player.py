from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment


class Player(Creature):

    def __init__(self, entity_id: int, x: int, y: int, sprite, name: str, skill, hp: int, strength: int, dexterity: int,
                 intelligence: int, charisma: int, perception: int, initiative: int, action_points: int, level: int,
                 discord_identity, alignment: str, backstory: str, equipment: Equipment):

        super().__init__(entity_id, x, y, sprite, name, skill, hp, strength, dexterity, intelligence, charisma,
                         perception, initiative, action_points, level)
        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.equipment = equipment
