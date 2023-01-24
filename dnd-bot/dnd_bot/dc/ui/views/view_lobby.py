import nextcord

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_game import ViewMain, ViewCharacter, ViewCharacterNonActive
from dnd_bot.dc.utils.utils import get_user_name_by_id, get_user_by_id
from dnd_bot.logic.game.handler_game import HandlerGame
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.lobby.handler_ready import HandlerReady
from dnd_bot.logic.lobby.handler_start import HandlerStart
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.utils import get_player_view


class JoinButton(nextcord.ui.View):

    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Join", style=nextcord.ButtonStyle.green)
    async def join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()

        status, lobby_players, error_message = await HandlerJoin.join_lobby(self.token, interaction.user.id,
                                                                            interaction.user.dm_channel.id,
                                                                            interaction.user.name)

        if status:
            await interaction.response.send_message("Check direct message!", ephemeral=True)

            lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

            # send messages about successful join operation
            await Messager.send_dm_message(interaction.user.id,
                                           f"Welcome to lobby of game {self.token}.\nNumber of players in lob"
                                           f"by: **{len(lobby_players)}**", embed=lobby_view_embed,
                                           view=ReadyButton(self.token))
            for user in lobby_players:
                if interaction.user.name != user[0]:
                    if user[2]:
                        if user[1]:
                            if Multiverse.get_game(self.token).all_users_ready():
                                view = StartButton(self.token)
                            else:
                                view = HostButtonDisabled(self.token)
                        else:
                            view = HostButtons(self.token)
                    else:
                        if user[1]:
                            view = None
                        else:
                            view = ReadyButton(self.token)

                    await Messager.edit_last_user_message(user[3], embed=lobby_view_embed, view=view)
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        self.value = False


class StartButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Start", style=nextcord.ButtonStyle.blurple)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        status, lobby_players_identities, error_message = await HandlerStart.start_game(self.token, interaction.user.id)

        if status:
            await interaction.response.send_message('Starting the game!', ephemeral=True)

            # send messages about successful start operation
            for user in lobby_players_identities:
                await Messager.send_dm_message(user, "Game has started successfully!\n")

                player = Multiverse.get_game(self.token).get_player_by_id_user(user)
                player_view = get_player_view(Multiverse.get_game(self.token), player)

                if player.active:
                    active_player = Multiverse.get_game(self.token).get_active_player()
                    active_user = await get_user_by_id(active_player.discord_identity)
                    turn_view_embed = MessageTemplates.player_turn_embed(
                        player, active_player,
                        active_user_icon=active_user.display_avatar.url)
                    await Messager.send_dm_message(user, content='', embed=turn_view_embed, view=ViewMain(self.token),
                                                   files=[player_view])
                else:
                    active_player = Multiverse.get_game(self.token).get_active_player()
                    active_user = await get_user_by_id(active_player.discord_identity)
                    turn_view_embed = MessageTemplates.player_turn_embed(
                        player, active_player,
                        active_user_icon=active_user.display_avatar.url)
                    await Messager.send_dm_message(user, content='', embed=turn_view_embed, files=[player_view],
                                                   view=ViewCharacterNonActive(self.token))

            HandlerGame.handle_game(self.token)

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
        """host ready button"""

        status, lobby_players, error_message = await HandlerReady.on_ready(self.token, interaction.user.id)
        lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

        if status:
            for user in lobby_players:
                if user[2]:
                    if user[1]:
                        if Multiverse.get_game(self.token).all_users_ready():
                            await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                                  view=StartButton(self.token))
                        else:
                            await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                                  view=HostButtonDisabled(self.token))
                    else:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                              view=HostButtons(self.token))
                else:
                    if user[1]:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed)
                    else:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                              view=ReadyButton(self.token))
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        self.value = False


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
            for user in lobby_players:
                if user[2]:
                    if user[1]:
                        if Multiverse.get_game(self.token).all_users_ready():
                            await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                                  view=StartButton(self.token))
                        else:
                            await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                                  view=HostButtonDisabled(self.token))
                    else:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                              view=HostButtons(self.token))
                else:
                    if user[1]:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed)
                    else:
                        await Messager.edit_last_user_message(user_id=user[3], embed=lobby_view_embed,
                                                              view=ReadyButton(self.token))
        else:
            await interaction.response.send_message(error_message, ephemeral=True)

        self.value = False
