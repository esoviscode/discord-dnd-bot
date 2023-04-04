from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.logic.game.handler_game import HandlerGame


class CommandResume(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='resume', description='Resumes a game by providing a game token')
    async def resume(self, interaction, token: str):
        try:
            await HandlerGame.resume_game(token)
        except Exception as e:
            await interaction.response.send_message(f'⚠️ {e}')


def setup(bot):
    bot.add_cog(CommandResume(bot))
