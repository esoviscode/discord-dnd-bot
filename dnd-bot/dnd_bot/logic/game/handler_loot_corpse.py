from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.utils.handler_views import HandlerViews
from dnd_bot.logic.prototype.entities.misc.corpse import Corpse
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import LootCorpseException


class HandlerLootCorpse:

    @staticmethod
    async def handle_loot_corpse(player):
        """ handles giving loot for the player and removing the corpse from the world """
        corpse: Corpse = None
        for entity in player.get_entities_around(cross_only=True):
            if isinstance(entity, Corpse):
                corpse = entity
                break
        if not corpse:
            raise Exception("Player tried to loot the corpse when there is not one nearby!")

        money = corpse.dropped_money
        items = corpse.dropped_items
        corpse_name = corpse.creature_name

        game: Game = Multiverse.get_game(player.game_token)
        game.delete_entity(corpse.id)

        player.money += money
        player.backpack += items

        await HandlerViews.display_views_for_users(player.game_token,
                                                   MessageTemplates.loot_corpse_action(
                                                              player.name, corpse_name, money, items))

