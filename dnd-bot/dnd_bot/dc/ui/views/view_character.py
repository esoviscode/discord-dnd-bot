import nextcord
from nextcord.ui import View

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.dc.ui.views.view_attack import ViewAttack
from dnd_bot.dc.ui.views.view_movement import ViewMovement


class ViewCharacter(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Equipment', style=nextcord.ButtonStyle.blurple)
    async def show_equipment(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening equipment menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        equipment_embed = MessageTemplates.equipment_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              embed=equipment_embed, view=ViewEquipment(self.token))

    @nextcord.ui.button(label='Stats', style=nextcord.ButtonStyle.blurple)
    async def show_stats(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        stats_embed = MessageTemplates.equipment_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              embed=stats_embed, view=ViewStats(self.token))

