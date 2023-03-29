from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.logic.game.handler_game import HandlerGame


class CommandPause(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='pause', description='Pauses the game by providing a game token')
    async def pause(self, interaction, token: str):
        try:
            await HandlerGame.pause_game(token)
        except Exception as e:
            await interaction.response.send_message(f'⚠️ {e}')


def setup(bot):
    bot.add_cog(CommandPause(bot))
