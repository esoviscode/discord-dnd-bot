class Item:

    def __init__(self, id_item: int, name: str, hp: int, strength: int, dexterity: int, intelligence: int,
                 charisma: int, perception: int, action_points: int, effect=None):
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
