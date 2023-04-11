import asyncio

import nextcord

from dnd_bot.dc.init import on_error
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_character_creation import ViewCharacterCreationStart
from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.lobby.handler_ready import HandlerReady
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class ViewLobby(nextcord.ui.View):
    """Class for helper methods used by multiple views"""

    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.on_error = on_error
        self.user_id = user_id
        self.token = token

    @staticmethod
    async def resend_lobby_message(token, user, lobby_view_embed):
        """method used to send refreshed message to user (e.g. after clicking ready)"""
        if user.is_host:
            await Messager.edit_last_user_message(user_id=user.discord_id, embeds=[lobby_view_embed],
                                                  view=ViewHost(user.discord_id, token,
                                                                host_ready=user.is_ready,
                                                                ready_to_start=Multiverse.get_game(token).
                                                                all_users_ready()))
        else:
            if user.is_ready:
                await Messager.edit_last_user_message(user_id=user.discord_id, embeds=[lobby_view_embed])
            else:
                await Messager.edit_last_user_message(user_id=user.discord_id, embeds=[lobby_view_embed],
                                                      view=ViewPlayer(user.discord_id, token))

    async def ready(self, interaction: nextcord.Interaction):
        """Callback to ready button (in host and player views)"""
        print(interaction.bot.name)
        try:
            lobby_players = await HandlerReady.on_ready(self.token, self.user_id)
            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)
            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.resend_lobby_message(self.token, user, lobby_view_embed))
                     for user in lobby_players]
            await asyncio.gather(*tasks)
            await q.join()
        except DiscordDndBotException as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_error_message(user_id=self.user_id, content=str(e))


class ViewJoin(ViewLobby):

    @nextcord.ui.button(label="Join", style=nextcord.ButtonStyle.green, custom_id='join-button')
    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            if interaction.user.dm_channel is None:
                await interaction.user.create_dm()

            lobby_players = await HandlerJoin.join_lobby(self.token, interaction.user.id,
                                                         interaction.user.dm_channel.id, interaction.user.name)
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            # send messages about successful join operation
            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)
            await Messager.send_dm_message(interaction.user.id,
                                           f"Welcome to lobby of game {self.token}.\n"
                                           f"Number of players in lobby: **{len(lobby_players)}**",
                                           embeds=[lobby_view_embed],
                                           view=ViewPlayer(self.user_id, self.token))

            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.resend_lobby_message(self.token, user, lobby_view_embed))
                     for user in lobby_players if user.discord_id != interaction.user.id]
            await asyncio.gather(*tasks)
            await q.join()

        except DiscordDndBotException as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_error_message(user_id=self.user_id, content=str(e))


class ViewHost(ViewLobby):
    """View of host during lobby, buttons state depends on host_ready and ready_to_start attributes"""
    def __init__(self, user_id, token, host_ready=False, ready_to_start=False):
        super().__init__(user_id, token)

        # add start button (disabled or not, depending on readiness of players)
        start_button = nextcord.ui.Button(label='Start', style=nextcord.ButtonStyle.blurple,
                                          custom_id='host-start-button')
        start_button.callback = self.start_button
        start_button.disabled = not ready_to_start
        self.add_item(start_button)

        # add ready button if host has not clicked it yet
        if not host_ready:
            ready_button = nextcord.ui.Button(label='Ready', style=nextcord.ButtonStyle.green,
                                              custom_id='host-ready-button')
            ready_button.callback = self.ready
            self.add_item(ready_button)

    async def start_button(self, interaction: nextcord.Interaction):
        try:
            lobby_players = await HandlerCharacterCreation.start_character_creation(self.token, interaction.user.id)
            for user in lobby_players:
                await Messager.send_dm_message(user_id=user.discord_id,
                                               content=None,
                                               embeds=[MessageTemplates.character_creation_start_message_template()],
                                               view=ViewCharacterCreationStart(self.token))
        except DiscordDndBotException as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_error_message(user_id=self.user_id, content=str(e))


class ViewPlayer(ViewLobby):
    """Ready button view used by players in lobby"""

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green, custom_id='ready-button')
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.ready(interaction)
