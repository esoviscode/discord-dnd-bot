from dnd_bot.dc.utils.handler_views import HandlerViews


class HandlerDialogue:

    @staticmethod
    async def handle_talk(player):
        """ handles giving loot for the player and removing the corpse from the world """

        await HandlerViews.display_views_for_users(player.game_token, "")
