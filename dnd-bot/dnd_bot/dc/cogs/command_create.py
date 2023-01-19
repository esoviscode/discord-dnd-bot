from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_lobby import HostButtons, JoinButton
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.logic.lobby.handler_create import HandlerCreate


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

            view = HostButtons(token)
            await Messager.send_dm_message(user_id=interaction.user.id,
                                           content=None,
                                           embed=MessageTemplates.lobby_view_message_template(token, [
                                               (host_name, False, True)]), view=view)

            view = JoinButton(token)
            await interaction.response.send_message(f"Hello {interaction.user.mention}!", view=view,
                                                    embed=MessageTemplates.lobby_creation_message(token))

            await view.wait()

            if view.value is None:
                return

        else:
            # TODO error message
            await interaction.response.send_message(f"Something went wrong while creating the lobby! :(")


def setup(bot):
    bot.add_cog(CommandCreate(bot))
