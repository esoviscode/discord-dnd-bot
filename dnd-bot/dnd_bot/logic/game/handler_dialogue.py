class HandlerDialogue:

    @staticmethod
    async def handle_talk(player, target):
        """ handles giving loot for the player and removing the corpse from the world """

        return f"{target.name}: \"Hello, {player.name}!\""
