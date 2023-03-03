from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.logic.prototype.database_object import DatabaseObject


class Item(DatabaseObject):
    """represents an item in the player's inventory"""

    def __init__(self, id_item: int = 0, name: str = "", hp: int = 0, strength: int = 0, dexterity: int = 0,
                 intelligence: int = 0, charisma: int = 0, perception: int = 0, action_points: int = 0,
                 effect: str = "", base_price: int = 0):
        ## TODO super().__init__(DatabaseItem.add_item(name,hp,strength, dexterity, intelligence, charisma, perception,
        ##                                       action_points, effect, base_price))
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
        self.base_price = base_price
