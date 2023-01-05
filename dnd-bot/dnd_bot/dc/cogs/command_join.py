from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.logic.lobby.handler_join import HandlerJoin


class CommandJoin(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="join", description="Joins to the lobby by its id")
    async def join(self, interaction, token: str):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        status, lobby_players, error_message = await HandlerJoin.join_lobby(token, interaction.user.id, interaction.user.name)
        print(f'{status}, {interaction.user.name}')

        if status:
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            lobby_view_embed = MessageTemplates.lobby_view_message_template(token, lobby_players)

            # send messages about successful join operation
            await Messager.send_dm_message(interaction.user.id, f"Welcome to lobby of game {token}.\nNumber of players in lob"
                                                    f"by: **{len(lobby_players)}**", embed=lobby_view_embed)
            for user in lobby_players:
                if interaction.user.name != user[0]:
                    await Messager.send_dm_message(user[3],
                                                   f"\n**{await get_user_name_by_id(interaction.user.id) }** has joined the lobby! Current number of "
                                                   f"players: **{len(lobby_players)}**", embed=lobby_view_embed)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)


def setup(bot):
    bot.add_cog(CommandJoin(bot))
