import nextcord
from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_lobby import ViewJoin, ViewHost
from dnd_bot.logic.lobby.handler_create import HandlerCreate
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class CommandCreate(Cog):
    """command used to create a new game"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="create", description="Creates new lobby")
    async def create(self, interaction: nextcord.Interaction):
        try:
            token, user = await HandlerCreate.create_lobby(interaction.user.id, interaction.user.dm_channel,
                                                           interaction.user.name, interaction.channel_id)

            await Messager.send_dm_message(interaction.user.id, token,
                                           f'You have successfully created a lobby! Game token: `{token}`')

            view = ViewHost(interaction.user.id, token)
            await Messager.send_dm_message(user_id=interaction.user.id,
                                           token=token,
                                           content=None,
                                           embeds=[MessageTemplates.lobby_view_message_template(token, [user])],
                                           view=view)

            view = ViewJoin(interaction.user.id, token)
            await interaction.response.send_message(f"Hello {interaction.user.mention}!", view=view,
                                                    embed=MessageTemplates.lobby_creation_message(token))
        except DiscordDndBotException as e:
            await Messager.send_error_message(interaction.channel_id, content=str(e))


def setup(bot):
    bot.add_cog(CommandCreate(bot))
