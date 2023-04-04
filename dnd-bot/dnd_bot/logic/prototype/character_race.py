from abc import abstractmethod


class CharacterRace:
    """Abstract interface defining methods which must be overriden by classes defining particular character races"""

    def __init__(self, name: str = ''):
        self.name = name
        self.description = ''
        self.long_description = ''

        self.emoji = ''
        self.base_hp = 0
        self.base_strength = 0
        self.base_dexterity = 0
        self.base_intelligence = 0
        self.base_charisma = 0
        self.base_perception = 0
        self.base_action_points = 0
        self.base_initiative = 0
