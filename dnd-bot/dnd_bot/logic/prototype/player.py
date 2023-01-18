import random

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment


class Player(Creature):
    """represents a player (which is controlled by a user)"""

    def __init__(self, entity_id: int = 0, x=0, y=0, sprite=None, name='Player', skill=None,
                 hp: int = 0, strength: int = 0, dexterity: int = 0,
                 intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 0,
                 discord_identity: int = 0, alignment: str = '', backstory: str = '', equipment: Equipment = None):

        super().__init__(entity_id, x, y, sprite, name, skill, hp, strength, dexterity, intelligence, charisma,
                         perception, initiative, action_points, level, drop_equipment=None, drop_money=0)
        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.equipment = equipment
        self.active = False
