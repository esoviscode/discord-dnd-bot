class HandlerDialogue:

    @staticmethod
    async def handle_talk(player, target):
        """ handles a conversation between player and target"""

        return f"{target.name}: \"Hello, {player.name}!\""
