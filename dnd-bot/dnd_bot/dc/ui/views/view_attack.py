import nextcord
from nextcord.ui import View, Button

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.handler_attack import HandlerAttack
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.ui.views.view_main import ViewMain


class ViewAttack(View):
    def __init__(self, token, enemies):
        super().__init__()
        self.value = None
        self.token = token
        self.enemies = enemies
        self.attack_enemy_buttons = [Button(label=str(x+1), style=nextcord.ButtonStyle.blurple)
                                     for x in range(10)]

        async def attack_enemy1(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 1"""
            await ViewAttack.attack(enemies[0], interaction.user.id, self.token, interaction)

        async def attack_enemy2(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 2"""
            await ViewAttack.attack(enemies[1], interaction.user.id, self.token, interaction)

        async def attack_enemy3(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 3"""
            await ViewAttack.attack(enemies[2], interaction.user.id, self.token, interaction)

        async def attack_enemy4(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 4"""
            await ViewAttack.attack(enemies[3], interaction.user.id, self.token, interaction)

        async def attack_enemy5(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 5"""
            await ViewAttack.attack(enemies[4], interaction.user.id, self.token, interaction)

        async def attack_enemy6(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 6"""
            await ViewAttack.attack(enemies[5], interaction.user.id, self.token, interaction)

        async def attack_enemy7(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 7"""
            await ViewAttack.attack(enemies[6], interaction.user.id, self.token, interaction)

        async def attack_enemy8(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 8"""
            await ViewAttack.attack(enemies[7], interaction.user.id, self.token, interaction)

        async def attack_enemy9(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 9"""
            await ViewAttack.attack(enemies[8], interaction.user.id, self.token, interaction)

        async def attack_enemy10(interaction: nextcord.Interaction):
            """callback function for button for attacking enemy number 10"""
            await ViewAttack.attack(enemies[9], interaction.user.id, self.token, interaction)

        self.attack_enemy_buttons[0].callback = attack_enemy1
        self.attack_enemy_buttons[1].callback = attack_enemy2
        self.attack_enemy_buttons[2].callback = attack_enemy3
        self.attack_enemy_buttons[3].callback = attack_enemy4
        self.attack_enemy_buttons[4].callback = attack_enemy5
        self.attack_enemy_buttons[5].callback = attack_enemy6
        self.attack_enemy_buttons[6].callback = attack_enemy7
        self.attack_enemy_buttons[7].callback = attack_enemy8
        self.attack_enemy_buttons[8].callback = attack_enemy9
        self.attack_enemy_buttons[9].callback = attack_enemy10

        for i in range(len(enemies)):
            self.add_item(self.attack_enemy_buttons[i])

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main manu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        map_view_message = MessageTemplates.map_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=map_view_message,
                                              view=ViewMain(self.token))

    @staticmethod
    async def attack(enemy, id_user, token, interaction: nextcord.Interaction):
        """attack enemy nr enemy_number from the available enemy list with the main weapon"""
        status, new_enemies, error_message = await HandlerAttack.handle_attack(enemy, id_user, token)

        if not status:
            await interaction.response.send_message(error_message)
            return

        map_view_message = MessageTemplates.map_view_template(token)
        enemies_list_embed = MessageTemplates.attack_view_message_template(new_enemies)
        lobby_players = Multiverse.get_game(token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=map_view_message,
                                                      embed=enemies_list_embed, view=ViewAttack(token, new_enemies))
            else:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=map_view_message)
