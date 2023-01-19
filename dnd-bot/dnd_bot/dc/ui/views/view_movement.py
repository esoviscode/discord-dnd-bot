import nextcord
from nextcord.ui import View

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.handler_movement import HandlerMovement
from dnd_bot.logic.prototype.multiverse import Multiverse


class ViewMovement(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='◄', style=nextcord.ButtonStyle.blurple)
    async def move_one_left(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile left"""
        status, error_message = await ViewMovement.move_one_tile('left', interaction.user.id, self.token)
        if not status:
            await interaction.response.send_message(error_message)
            return

        map_view_message = MessageTemplates.map_view_template(self.token)
        lobby_players = Multiverse.get_game(self.token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.send_dm_message(user.discord_id, map_view_message, view=ViewMovement(self.token))
            else:
                await Messager.send_dm_message(user.discord_id, map_view_message)

        await interaction.response.send_message(map_view_message, view=ViewMovement(self.token))
        return

    @nextcord.ui.button(label='►', style=nextcord.ButtonStyle.blurple)
    async def move_one_right(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile right"""
        status, error_message = await ViewMovement.move_one_tile('right', interaction.user.id, self.token)
        if not status:
            await interaction.response.send_message(error_message)
            return

        map_view_message = MessageTemplates.map_view_template(self.token)
        lobby_players = Multiverse.get_game(self.token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.send_dm_message(user.discord_id, map_view_message, view=ViewMovement(self.token))
            else:
                await Messager.send_dm_message(user.discord_id, map_view_message)

        # await interaction.response.send_message(map_view_message, view=ViewMovement(self.token))
        return

    @nextcord.ui.button(label='▲', style=nextcord.ButtonStyle.blurple)
    async def move_one_up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile up"""
        status, error_message = await ViewMovement.move_one_tile('up', interaction.user.id, self.token)
        if not status:
            await interaction.response.send_message(error_message)
            return

        map_view_message = MessageTemplates.map_view_template(self.token)
        lobby_players = Multiverse.get_game(self.token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.send_dm_message(user.discord_id, map_view_message, view=ViewMovement(self.token))
            else:
                await Messager.send_dm_message(user.discord_id, map_view_message)

        #await interaction.response.send_message(map_view_message, view=ViewMovement(self.token))
        return

    @nextcord.ui.button(label='▼', style=nextcord.ButtonStyle.blurple)
    async def move_one_down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile down"""
        status, error_message = await ViewMovement.move_one_tile('down', interaction.user.id, self.token)
        if not status:
            await interaction.response.send_message(error_message)
            return

        map_view_message = MessageTemplates.map_view_template(self.token)
        lobby_players = Multiverse.get_game(self.token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.send_dm_message(user.discord_id, map_view_message, view=ViewMovement(self.token))
            else:
                await Messager.send_dm_message(user.discord_id, map_view_message)
        await interaction.response.send_message(map_view_message, view=ViewMovement(self.token))
        return

    @nextcord.ui.button(label='End turn', style=nextcord.ButtonStyle.danger)
    async def end_turn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        status = await HandlerMovement.handle_end_turn(interaction.user.id, self.token)

        lobby_players = Multiverse.get_game(self.token).user_list

        next_active_player = Multiverse.get_game(self.token).creatures_queue[0]

        # send messages about successful start operation
        for user in lobby_players:

            map_view_message = MessageTemplates.map_view_template(self.token)

            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)
            if player.discord_identity == next_active_player.discord_identity:
                await Messager.send_dm_message(user.discord_id, map_view_message, view=ViewMovement(self.token))
            else:
                await Messager.send_dm_message(user.discord_id, map_view_message)

        return

    @staticmethod
    async def move_one_tile(direction, id_user, token):
        """shared movement by one tile function for all directions"""
        return await HandlerMovement.handle_movement(direction, 1, id_user, token)
