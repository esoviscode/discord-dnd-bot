import asyncio

import nextcord

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_character_creation import ViewCharacterCreationStart
from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.lobby.handler_ready import HandlerReady
from dnd_bot.logic.prototype.multiverse import Multiverse


class ViewLobby:
    """Class for helper methods used by multiple views"""

    @staticmethod
    async def resend_lobby_message(token, user, lobby_view_embed):
        """method used to send refreshed message to user (e.g. after clicking ready)"""
        if user.is_host:
            await Messager.edit_last_user_message(user_id=user.discord_id, embed=lobby_view_embed,
                                                  view=ViewHost(user.discord_id, token,
                                                                host_ready=user.is_ready,
                                                                ready_to_start=Multiverse.get_game(token).all_users_ready()))
        else:
            if user.is_ready:
                await Messager.edit_last_user_message(user_id=user.discord_id, embed=lobby_view_embed)
            else:
                await Messager.edit_last_user_message(user_id=user.discord_id, embed=lobby_view_embed,
                                                      view=ReadyButton(user.discord_id, token))


class ViewJoin(nextcord.ui.View):

    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token

    @nextcord.ui.button(label="Join", style=nextcord.ButtonStyle.green, custom_id='join-button')
    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            lobby_players = await HandlerJoin.join_lobby(self.token, interaction.user.id,
                                                         interaction.user.dm_channel.id, interaction.user.name)
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            # send messages about successful join operation
            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)
            await Messager.send_dm_message(interaction.user.id,
                                           f"Welcome to lobby of game {self.token}.\n"
                                           f"Number of players in lobby: **{len(lobby_players)}**",
                                           embed=lobby_view_embed,
                                           view=ReadyButton(self.user_id, self.token))

            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.resend_lobby_message(self.token, user, lobby_view_embed))
                     for user in lobby_players if user.discord_id != interaction.user.id]
            await asyncio.gather(*tasks)
            await q.join()

        except Exception as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_message(user_id=self.user_id, content=str(e), error=True)


class ViewHost(nextcord.ui.View):
    """View of host during lobby, buttons state depends on host_ready and ready_to_start attributes"""
    def __init__(self, user_id, token, host_ready=False, ready_to_start=False):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token

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
            ready_button.callback = self.ready_button
            self.add_item(ready_button)

    async def start_button(self, interaction: nextcord.Interaction):
        try:
            lobby_players = await HandlerCharacterCreation.start_character_creation(self.token, interaction.user.id)
            for user in lobby_players:
                await Messager.send_dm_message(user_id=user.discord_id,
                                               content=None,
                                               embed=MessageTemplates.character_creation_start_message_template(),
                                               view=ViewCharacterCreationStart(self.token))
        except Exception as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_message(user_id=self.user_id, content=str(e), error=True)

    async def ready_button(self, interaction: nextcord.Interaction):
        await ReadyButton.ready(self, self.user_id, self.token)


class ReadyButton(nextcord.ui.View):
    """Ready button view used by players in lobby"""
    def __init__(self, user_id, token):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.token = token

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green, custom_id='ready-button')
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        try:
            lobby_players = await HandlerReady.on_ready(self.token, self.user_id)
            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)
            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.resend_lobby_message(self.token, user, lobby_view_embed))
                     for user in lobby_players]
            await asyncio.gather(*tasks)
            await q.join()
        except Exception as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_message(user_id=self.user_id, content=str(e), error=True)
