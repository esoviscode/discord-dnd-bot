import nextcord
from nextcord import slash_command
from nextcord.ext.commands import Cog, Bot

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_movement import ViewMovement
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.lobby.handler_create import HandlerCreate
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.lobby.handler_ready import HandlerReady
from dnd_bot.logic.lobby.handler_start import HandlerStart
from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


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

                    await Messager.send_dm_message(user[3],
                                                   f"\n**{await get_user_name_by_id(interaction.user.id)}** has "
                                                   f"joined the lobby! Current number of "
                                                   f"players: **{len(lobby_players)}**",
                                                   embed=lobby_view_embed, view=view)
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

                map_view_message = MessageTemplates.map_view_template(self.token)

                await Messager.send_dm_message(user, map_view_message, view=ViewMovement(self.token))
        else:
            await interaction.response.send_message(error_message, ephemeral=True)


class HostButtonDisabled(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.gray, disabled=True)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class HostButtons(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Start', style=nextcord.ButtonStyle.gray, disabled=True)
    async def start(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green)
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        lobby_players = await HandlerReady.on_ready(self.token, interaction.user.id)
        lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

        for user in lobby_players:
            if user[2]:
                if user[1]:
                    if Multiverse.get_game(self.token).all_users_ready():
                        await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=StartButton(self.token))
                    else:
                        await Messager.send_dm_message(user[3], "", embed=lobby_view_embed,
                                                       view=HostButtonDisabled(self.token))
                else:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=HostButtons(self.token))
            else:
                if user[1]:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=None)
                else:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=ReadyButton(self.token))

        self.value = False


class ReadyButton(nextcord.ui.View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label="Ready", style=nextcord.ButtonStyle.green)
    async def ready(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        lobby_players = await HandlerReady.on_ready(self.token, interaction.user.id)
        lobby_view_embed = MessageTemplates.lobby_view_message_template(self.token, lobby_players)

        for user in lobby_players:
            if user[2]:
                if user[1]:
                    if Multiverse.get_game(self.token).all_users_ready():
                        await Messager.send_dm_message(user[3], "", embed=lobby_view_embed,
                                                       view=StartButton(self.token))
                    else:
                        await Messager.send_dm_message(user[3], "", embed=lobby_view_embed,
                                                       view=HostButtonDisabled(self.token))
                else:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=HostButtons(self.token))
            else:
                if user[1]:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=None)
                else:
                    await Messager.send_dm_message(user[3], "", embed=lobby_view_embed, view=ReadyButton(self.token))

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
