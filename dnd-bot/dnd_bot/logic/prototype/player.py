import random

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment


class Player(Creature):
    """represents a player (which is controlled by a user)"""

    def __init__(self, entity_id=0, x=0, y=0, sprite=None, name='Player', hp=0, strength=0, dexterity=0,
                 intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 1,
                 discord_identity: int = 0, alignment: str = '', backstory: str = '', equipment: Equipment = None):

        # TODO remove this - it generates some random values for now
        hp = random.randint(15, 30)
        strength = random.randint(1, 5)
        dexterity = random.randint(1, 5)
        intelligence = random.randint(1, 5)
        charisma = random.randint(1, 5)
        perception = random.randint(1, 5)
        initiative = random.randint(1, 5)
        action_points = random.randint(1, 5)
        # TODO remove above

        super().__init__(x=x, y=y, sprite=sprite, name=name, hp=hp, strength=strength, dexterity=dexterity,
                         intelligence=intelligence, charisma=charisma, perception=perception, initiative=initiative,
                         action_points=action_points, level=level)

        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.equipment = equipment
        self.active = False
