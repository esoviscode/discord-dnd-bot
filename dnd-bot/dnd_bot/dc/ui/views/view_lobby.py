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
    @staticmethod
    async def lobby_readiness_handler(token, user, lobby_view_embed):
        if user[2]:
            if user[1]:
                if Multiverse.get_game(token).all_users_ready():
                    await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                          view=StartButton(token))
                else:
                    await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                          view=HostButtonDisabled(token))
            else:
                await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                      view=HostButtons(token))
        else:
            if user[1]:
                await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed)
            else:
                await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                      view=ReadyButton(token))


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
                                           view=ReadyButton(self.token))

            for user in lobby_players:
                if interaction.user.id == user.discord_id:
                    continue
                if user.is_host:
                    if user.is_ready:
                        if Multiverse.get_game(self.token).all_users_ready():
                            view = StartButton(self.token)
                        else:
                            view = HostButtonDisabled(self.token)
                    else:
                        view = HostButtons(self.token)
                else:
                    if user.is_ready:
                        view = None
                    else:
                        view = ReadyButton(self.token)

                await Messager.edit_last_user_message(user.discord_id, embed=lobby_view_embed, view=view)

        except Exception as e:
            await Messager.delete_last_user_error_message(self.user_id)
            await Messager.send_dm_message(user_id=self.user_id, content=str(e), error=True)


class StartButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__(timeout=None)
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Start", style=nextcord.ButtonStyle.blurple, custom_id='start-button')
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        status, lobby_players_identities, error_message = \
            await HandlerCharacterCreation.start_character_creation(self.token, interaction.user.id)

        if status:
            for user_id in lobby_players_identities:
                await Messager.send_dm_message(user_id=user_id,
                                               content=None,
                                               embed=MessageTemplates.character_creation_start_message_template(),
                                               view=ViewCharacterCreationStart(self.token))

        else:
            await interaction.response.send_message(error_message, ephemeral=True)


class HostButtonDisabled(nextcord.ui.View):
    def __init__(self, token):
        super().__init__(timeout=None)
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.blurple, disabled=True,
                        custom_id='disabled-start-button')
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class HostButtons(nextcord.ui.View):
    def __init__(self, token):
        super().__init__(timeout=None)
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.blurple, disabled=True, custom_id='host-start-button')
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green, custom_id='host-ready-button')
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await ReadyButton.ready(self, button, interaction)


class ReadyButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__(timeout=None)
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green, custom_id='ready-button')
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """ready button"""

        status, lobby_players, error_message = await HandlerReady.on_ready(self.token, interaction.user.id)
        lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

        if status:
            q = asyncio.Queue()
            tasks = [asyncio.create_task(ViewLobby.lobby_readiness_handler(self.token, user, lobby_view_embed))
                     for user in lobby_players]
            await asyncio.gather(*tasks)
            await q.join()

        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        self.value = False
