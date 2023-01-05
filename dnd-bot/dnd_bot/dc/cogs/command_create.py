import time

from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command
import nextcord
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.logic.lobby.handler_create import HandlerCreate
from dnd_bot.dc.ui.message_templates import MessageTemplates
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
            await Messager.send_dm_message(interaction.user.id,
                                           f'You have successfully created a lobby! Game token: {token}')
            host_name = await get_user_name_by_id(interaction.user.id)
            await Messager.send_dm_message(user_id=interaction.user.id,
                                           content=None,
                                           embed=MessageTemplates.lobby_view_message_template(token, [(host_name, False, True)]))

            
            view = JoinButton(token)
            await interaction.response.send_message(f"Hello {interaction.user.mention}!\n"
                                                              f"A fresh game for you and your team has been created! Make sure "
                                                              f"that everyone who wants to play is in this server!\n\n"
                                                              f"Game token: `{token}`")

            await view.wait()

            if view.value is None:
                return

        else:
            await interaction.response.send_message(f"Something went wrong while creating the lobby! :(")


def setup(bot):
    bot.add_cog(CommandCreate(bot))
