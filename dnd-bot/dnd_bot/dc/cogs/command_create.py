import time

from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command
import nextcord
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.lobby.handler_create import HandlerCreate
from dnd_bot.logic.lobby.handler_join import HandlerJoin


class JoinButton(nextcord.ui.View):

    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Join", style=nextcord.ButtonStyle.green)
    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Check direct message!", ephemeral=True)
        await HandlerJoin.join_lobby(str(self.token), interaction.user.id, interaction.user.name)
        self.value = True
        self.stop()


class CommandCreate(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="create", description="Creates new lobby")
    async def create(self, interaction):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()
        status, token = await HandlerCreate.create_lobby(interaction.user.id)

        if status:
            view = JoinButton(token)
            await Messager.send_dm_message(interaction.user.id, f"Welcome to **{token}** lobby!")
            await interaction.response.send_message(f"Hello {interaction.user.mention}!\n "
                                                              f"A fresh game for you and your team has been created! Make sure "
                                                              f"that everyone who wants to play is in this server!\n "
                                                              f"Game token: ||{token}||", view=view)

            await view.wait()

            if view.value is None:
                return

        else:
            await interaction.response.send_message(f"Something went wrong while creating the lobby! :(")


def setup(bot):
    bot.add_cog(CommandCreate(bot))
