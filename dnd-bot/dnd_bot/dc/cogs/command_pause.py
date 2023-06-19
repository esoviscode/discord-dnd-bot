from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.handler_game import HandlerGame
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class CommandPause(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='pause', description='Pauses the game by providing a game token')
    async def pause(self, interaction, token: str):
        try:
            partial_msg = await interaction.response.send_message('Pausing in progress...', ephemeral=True)
            await HandlerGame.pause_game(token)
            await Messager.delete_last_user_message(interaction.user.id, token)

            msg = await partial_msg.fetch()
            await msg.delete()
            await Messager.send_dm_information_message(user_id=interaction.user.id, content='The game has been paused!',
                                                       token=token)

        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(user_id=interaction.user.id, content=str(e), token=token)


def setup(bot):
    bot.add_cog(CommandPause(bot))
