import nextcord
from nextcord.ui import View

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.dc.ui.views.view_main import ViewMain


class ViewSkills(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              view=ViewMain(self.token))