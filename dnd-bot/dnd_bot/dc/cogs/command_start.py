from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.lobby.handler_start import HandlerStart


class CommandStart(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="start", description="Exits from lobby and starts game")
    async def start(self, interaction, token: str):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        # TODO HandlerStart class with start_game static method
        status, lobby_players_identities, error_message = await HandlerStart.start_game(token, interaction.user.id)

        if status:
            # send messages about successful start operation
            for user in lobby_players_identities:
                await Messager.send_dm_message(user,
                                               "Game has successfully started!\n")
        else:
            await interaction.response.send_message(error_message, ephemeral=True)


def setup(bot):
    bot.add_cog(CommandStart(bot))
