class Equipment:
    def __init__(self, id_equipment, helmet=None, chest=None, leg_armor=None, boots=None, left_hand=None,
                 right_hand=None, item_list=None, accessory=None):
        self.id = id_equipment
        self.helmet = helmet
        self.chest = chest
        self.leg_armor = leg_armor
        self.boots = boots
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.item_list = item_list
        self.accessory = accessory
