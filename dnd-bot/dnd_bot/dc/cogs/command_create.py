from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.dc.ui.send_message import Messager
from dnd_bot.logic.lobby.handler_create import HandlerCreate


class CommandCreate(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="create", description="Creates new lobby")
    async def create(self, interaction):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()
        status, token = await HandlerCreate.create_lobby(interaction.user.id)

        if status:
            await Messager.send_dm_message(interaction.user.id, f"Welcome to **{token}** lobby!")
            await interaction.response.send_message(f"Hello {interaction.user.mention}!\n "
                                                    f"A fresh game for you and your team has been created! Make sure "
                                                    f"that everyone who wants to play is in this server!\n "
                                                    f"Game token: ||{token}||")
        else:
            await interaction.response.send_message(f"Something went wrong while creating the lobby! :(")


def setup(bot):
    bot.add_cog(CommandCreate(bot))
