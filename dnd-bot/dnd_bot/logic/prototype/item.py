class Item:
    """represents an item in the player's inventory"""
    def __init__(self, id_item: int = 0, name: str = "", hp: int = 0, strength: int = 0, dexterity: int = 0,
                 intelligence: int = 0, charisma: int = 0, perception: int = 0, action_points: int = 0, effect=None):
        self.id = id_item
        self.name = name
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.perception = perception
        self.action_points = action_points
        self.effect = effect
