import asyncio

import nextcord
from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.dc.ui.views.view_lobby import ViewPlayer, ViewLobby
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class CommandJoin(Cog):
    """handles join command"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="join", description="Joins to the lobby by its id")
    async def join(self, interaction: nextcord.Interaction, token: str):
        try:
            if interaction.user.dm_channel is None:
                await interaction.user.create_dm()

            lobby_players = await HandlerJoin.join_lobby(token, interaction.user.id,
                                                         interaction.user.dm_channel.id, interaction.user.name)
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            # send messages about successful join operation
            lobby_view_embed = MessageTemplates.lobby_view_message_template(token, lobby_players)
            await Messager.send_dm_message(interaction.user.id, token,
                                           f"Welcome to lobby of game {token}.\n"
                                           f"Number of players in lobby: **{len(lobby_players)}**",
                                           embeds=[lobby_view_embed],
                                           view=ViewPlayer(interaction.user.discord_id, token))

            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.resend_lobby_message(token, user, lobby_view_embed))
                     for user in lobby_players if user.discord_id != interaction.user.id]
            await asyncio.gather(*tasks)
            await q.join()

        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(user_id=interaction.user.discord_id, token=token, content=str(e))


def setup(bot):
    bot.add_cog(CommandJoin(bot))
