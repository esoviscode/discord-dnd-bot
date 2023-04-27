from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""

    def __init__(self, x=0, y=0, sprite: str = '', name: str = 'Creature', hp: int = 0, strength: int = 0,
                 dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 0, equipment: Equipment = None, drop_money = None,
                 game_token: str = '', look_direction: str = 'down', experience: int = 0,
                 creature_class: str = '', drops=None, ai=0):
        super().__init__(x=x, y=y, sprite=sprite, name=name, fragile=True, game_token=game_token, look_direction=look_direction)
        if drop_money is None:
            drop_money = []
        if drops is None:
            drops = []
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.perception = perception
        self.initiative = initiative
        self.action_points = action_points
        self.level = level
        self.equipment = equipment
        self.drop_money = drop_money
        self.initial_action_points = action_points
        self.experience = experience
        self.creature_class = creature_class
        self.drops = drops

        # TODO set ai function depending on ai argument
        self.ai = self.ai_simple_move

    def ai_action(self):
        self.action_points -= 1
        return self.ai()

    def ai_simple_move(self):
        return "Made simple move"
