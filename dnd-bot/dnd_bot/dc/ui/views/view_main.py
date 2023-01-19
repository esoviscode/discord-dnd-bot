import nextcord
from nextcord.ui import View

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.dc.ui.views.view_attack import ViewAttack
from dnd_bot.dc.ui.views.view_movement import ViewMovement
from dnd_bot.dc.ui.views.view_character import ViewCharacter


class ViewMain(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Attack', style=nextcord.ButtonStyle.blurple)
    async def attack(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening attack menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        # TODO adding enemies in players range to the list
        enemies = []

        enemies_list_embed = MessageTemplates.attack_view_message_template(enemies)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              embed=enemies_list_embed, view=ViewAttack(self.token, enemies))

    @nextcord.ui.button(label='Move', style=nextcord.ButtonStyle.blurple)
    async def move(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening move menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              view=ViewMovement(self.token))

    @nextcord.ui.button(label='Skill', style=nextcord.ButtonStyle.blurple)
    async def skill(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening skill menu"""
        pass

    @nextcord.ui.button(label='Character', style=nextcord.ButtonStyle.blurple)
    async def character(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening character menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              view=ViewCharacter(self.token))

    @nextcord.ui.button(label='More actions', style=nextcord.ButtonStyle.danger)
    async def more_actions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening more actions menu"""
        pass
