from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.prototype.items.equipable import Equipable
from dnd_bot.logic.prototype.items.item import Item


class HandlerManageItems:
    """handler for managing items in equipment"""
    @staticmethod
    async def equip_item(player, index_of_item_in_backpack):
        """handles equipping an item"""
        item = player.backpack[index_of_item_in_backpack]

        def equip(to_be_equipped: Item):
            """ equips an item andchecks if an item of this category is
            already equipped and puts it in backpack"""
            del player.backpack[index_of_item_in_backpack]

            if to_be_equipped.equipable == Equipable.WEAPON:
                if player.equipment.right_hand:
                    player.backpack.append(player.equipment.right_hand)
                player.equipment.right_hand = to_be_equipped
            elif to_be_equipped.equipable == Equipable.HELMET:
                if player.equipment.helmet:
                    player.backpack.append(player.equipment.helmet)
                player.equipment.helmet = to_be_equipped
            elif to_be_equipped.equipable == Equipable.CHEST:
                if player.equipment.chest:
                    player.backpack.append(player.equipment.chest)
                player.equipment.chest = to_be_equipped
            elif to_be_equipped.equipable == Equipable.LEG_ARMOR:
                if player.equipment.leg_armor:
                    player.backpack.append(player.equipment.leg_armor)
                player.equipment.leg_armor = to_be_equipped
            elif to_be_equipped.equipable == Equipable.BOOTS:
                if player.equipment.boots:
                    player.backpack.append(player.equipment.boots)
                player.equipment.boots = to_be_equipped
            elif to_be_equipped.equipable == Equipable.ACCESSORY:
                if player.equipment.accessory:
                    player.backpack.append(player.equipment.accessory)
                player.equipment.accessory = to_be_equipped
            elif to_be_equipped.equipable == Equipable.OFF_HAND:
                if player.equipment.left_hand:
                    player.backpack.append(player.equipment.left_hand)
                player.equipment.left_hand = to_be_equipped

        if item.equipable == Equipable.NO:
            await Messager.send_dm_error_message(player.discord_identity, "You can't equip this item")
            return
        equip(item)

    @staticmethod
    async def remove_item(player, index_of_item_in_backapck):
        """handles removing an item"""
        pass