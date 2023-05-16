from dnd_bot.database.database_equipment import DatabaseEquipment
from dnd_bot.logic.prototype.database_object import DatabaseObject
from dnd_bot.logic.prototype.items.item import Item


class Equipment(DatabaseObject):
    """represents the player's equipped items"""

    def __init__(self, helmet: Item = None, chest: Item = None, leg_armor: Item = None, boots: Item = None,
                 left_hand: Item = None, right_hand: Item = None, accessory: Item = None):
        super().__init__(
            DatabaseEquipment.add_equipment(helmet=helmet.id if helmet is not None else None,
                                            chest=chest.id if chest is not None else None,
                                            leg_armor=leg_armor.id if leg_armor is not None else None,
                                            boots=boots.id if boots is not None else None,
                                            left_hand=left_hand.id if left_hand is not None else None,
                                            right_hand=right_hand.id if right_hand is not None else None,
                                            accessory=accessory.id if accessory is not None else None))
        self.helmet = helmet
        self.chest = chest
        self.leg_armor = leg_armor
        self.boots = boots
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.accessory = accessory
