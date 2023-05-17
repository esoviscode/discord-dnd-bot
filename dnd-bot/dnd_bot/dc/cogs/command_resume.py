from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.handler_game import HandlerGame
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class CommandResume(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='resume', description='Resumes a game by providing a game token')
    async def resume(self, interaction, token: str):
        try:
            await HandlerGame.resume_game(token)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(user_id=interaction.user.id, content=str(e), token=token)

        await interaction.response.send_message('ℹ️ Resuming the game!', ephemeral=True)


def setup(bot):
    bot.add_cog(CommandResume(bot))
