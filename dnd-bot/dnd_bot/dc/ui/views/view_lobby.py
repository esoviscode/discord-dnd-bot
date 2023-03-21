import asyncio

import nextcord

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_character_creation import ViewCharacterCreationStart
from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.handler_game import HandlerGame
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.lobby.handler_ready import HandlerReady
from dnd_bot.logic.lobby.handler_start import HandlerStart
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.utils import get_player_view


class ViewLobby:
    @staticmethod
    async def join_button_handler(token, interaction: nextcord.Interaction):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        status, lobby_players, error_message = await HandlerJoin.join_lobby(token, interaction.user.id,
                                                                            interaction.user.dm_channel.id,
                                                                            interaction.user.name)

        if status:
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            lobby_view_embed = MessageTemplates.lobby_view_message_template(token, lobby_players)

            # send messages about successful join operation
            await Messager.send_dm_message(interaction.user.id,
                                           f"Welcome to lobby of game {token}.\nNumber of players in lob"
                                           f"by: **{len(lobby_players)}**", embed=lobby_view_embed,
                                           view=ReadyButton(token))
            for user in lobby_players:
                if interaction.user.name != user[0]:
                    if user[2]:
                        if user[1]:
                            if Multiverse.get_game(token).all_users_ready():
                                view = StartButton(token)
                            else:
                                view = HostButtonDisabled(token)
                        else:
                            view = HostButtons(token)
                    else:
                        if user[1]:
                            view = None
                        else:
                            view = ReadyButton(token)

                    await Messager.edit_last_user_message(user[3], embed=lobby_view_embed, view=view)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

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


class JoinButton(nextcord.ui.View):

    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Join", style=nextcord.ButtonStyle.green)
    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await ViewLobby.join_button_handler(self.token, interaction)


class StartButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Start", style=nextcord.ButtonStyle.blurple)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        status, lobby_players_identities, error_message =\
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
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class HostButtons(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green)
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await ReadyButton.ready(self, button, interaction)


class ReadyButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green)
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
