import json

from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.logic.prototype.database_object import DatabaseObject
from dnd_bot.logic.prototype.items.equipable import Equipable


class Item(DatabaseObject):
    """represents an item in the player's inventory"""

    def __init__(self, id_item: int = 0, name: str = "", effect: str = ""):
        ## TODO super().__init__(DatabaseItem.add_item(name,hp,strength, dexterity, intelligence, charisma, perception,
        ##                                       action_points, effect, base_price))

        self.id = id_item
        self.name = name

        self.damage = (0, 0)
        self.base_price = 0
        self.use_range = 0
        self.effect = effect

        self.hp = 0
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0
        self.charisma = 0
        self.perception = 0
        self.action_points = 0
        self.equipable: Equipable = Equipable.NO

        self.load_attributes_from_json()

    def load_attributes_from_json(self):
        """
        loads item stats from json based on self.name
        """
        with open('dnd_bot/assets/campaigns/campaign.json') as file:
            items = json.load(file)['items']

            for item_type in items.keys():
                if self.name in items[item_type]:  # items without a subtype
                    pass
                item_subtype_dict = items[item_type]
                for item_subtype in item_subtype_dict:
                    if self.name in item_subtype_dict[item_subtype]:  # items with a subtype

                        if item_type == "weapons":
                            self.equipable = Equipable.WEAPON
                        elif item_type == "armors":
                            if item_subtype == "helmets":
                                self.equipable = Equipable.HELMET
                            elif item_subtype == "chestplates":
                                self.equipable = Equipable.CHEST
                            elif item_subtype == "leg armors":
                                self.equipable = Equipable.LEG_ARMOR
                            elif item_subtype == "boots":
                                self.equipable = Equipable.BOOTS
                        elif item_type == "off-hands":
                            self.equipable = Equipable.OFF_HAND
                        elif item_type == "accessories":
                            self.equipable = Equipable.ACCESSORY

                        item = item_subtype_dict[item_subtype][self.name]
                        if item:
                            if 'damage' in item:
                                self.damage = (item['damage'][0], item['damage'][1])
                            if 'range' in item:
                                self.use_range = item['range']
                            if 'base-price' in item:
                                self.base_price = item['base-price']
                            if 'action-points' in item:
                                self.action_points = item['action-points']
                            if 'effect' in item:
                                self.effect = item['effect']

                            if 'hp' in item:
                                self.hp = item['hp']
                            if 'strength' in item:
                                self.strength = item['strength']
                            if 'dexterity' in item:
                                self.dexterity = item['dexterity']
                            if 'intelligence' in item:
                                self.intelligence = item['intelligence']
                            if 'charisma' in item:
                                self.charisma = item['charisma']
                            if 'perception' in item:
                                self.perception = item['perception']
