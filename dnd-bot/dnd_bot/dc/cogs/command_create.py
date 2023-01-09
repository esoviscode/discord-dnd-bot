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

        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        status, lobby_players, error_message = await HandlerJoin.join_lobby(self.token, interaction.user.id, interaction.user.dm_channel.id, interaction.user.name)

        if status:
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

            # send messages about successful join operation
            await Messager.send_dm_message(interaction.user.id,
                                           f"Welcome to lobby of game {self.token}.\nNumber of players in lob"
                                           f"by: **{len(lobby_players)}**", embed=lobby_view_embed)
            for user in lobby_players:
                if interaction.user.name != user[0]:
                    await Messager.send_dm_message(user[3],
                                                   f"\n**{await get_user_name_by_id(interaction.user.id)}** has joined the lobby! Current number of "
                                                   f"players: **{len(lobby_players)}**", embed=lobby_view_embed)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        self.value = False


class CommandCreate(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="create", description="Creates new lobby")
    async def create(self, interaction):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        status, token, error_message = await HandlerCreate.create_lobby(interaction.user.id, interaction.user.dm_channel
                                                                        , interaction.user.name)

        if status:
            await Messager.send_dm_message(interaction.user.id,
                                           f'You have successfully created a lobby! Game token: `{token}`')
            host_name = await get_user_name_by_id(interaction.user.id)
            await Messager.send_dm_message(user_id=interaction.user.id,
                                           content=None,
                                           embed=MessageTemplates.lobby_view_message_template(token, [(host_name, False, True)]))

            view = JoinButton(token)
            await interaction.response.send_message(f"Hello {interaction.user.mention}!", view=view, embed=MessageTemplates.lobby_creation_message(token))

            await view.wait()

            if view.value is None:
                return

        else:
            # TODO error message
            await interaction.response.send_message(f"Something went wrong while creating the lobby! :(")


def setup(bot):
    bot.add_cog(CommandCreate(bot))
