import asyncio
import multiprocessing

import nextcord
from nextcord.ui import View
from nextcord.ui import Button

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.message_holder import MessageHolder
from dnd_bot.logic.game.handler_skills import HandlerSkills
from dnd_bot.logic.game.handler_attack import HandlerAttack
from dnd_bot.logic.game.handler_movement import HandlerMovement
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.utils import get_player_view
from multiprocessing.pool import Pool

from threading import Lock

s_print_lock = Lock()


class ViewMain(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Attack', style=nextcord.ButtonStyle.blurple)
    async def attack(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening attack menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        # TODO adding enemies in players range to the list
        enemies = []

        enemies_list_embed = MessageTemplates.attack_view_message_template(enemies)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              embed=enemies_list_embed, view=ViewAttack(self.token, enemies))

    @nextcord.ui.button(label='Move', style=nextcord.ButtonStyle.blurple)
    async def move(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening move menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewMovement(self.token))

    @nextcord.ui.button(label='Skill', style=nextcord.ButtonStyle.blurple)
    async def skill(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening skill menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        skills_list_embed = MessageTemplates.skills_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              embed=skills_list_embed, view=ViewSkills(self.token, player.skills))

    @nextcord.ui.button(label='Character', style=nextcord.ButtonStyle.blurple)
    async def character(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening character menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewCharacter(self.token))

    @nextcord.ui.button(label='More actions', style=nextcord.ButtonStyle.danger)
    async def more_actions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening more actions menu"""
        pass

    @nextcord.ui.button(label='End turn', style=nextcord.ButtonStyle.danger)
    async def end_turn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for ending turn"""

        status, error_message = await HandlerMovement.handle_end_turn(interaction.user.id, self.token)
        if not status:
            await interaction.response.send_message(error_message)

        lobby_players = Multiverse.get_game(self.token).user_list

        next_active_player = Multiverse.get_game(self.token).creatures_queue[0]

        # send messages about successful start operation
        for user in lobby_players:
            player = Multiverse.get_game(self.token).get_player_by_id_user(user.discord_id)

            if player.discord_identity == next_active_player.discord_identity:
                turn_view_message = MessageTemplates.turn_view_template(self.token, next_active_player.name,
                                                                       player.action_points, True)
                await Messager.edit_last_user_message(user.discord_id, turn_view_message, view=ViewMain(self.token))
            else:
                turn_view_message = MessageTemplates.turn_view_template(self.token, next_active_player.name,
                                                                       player.action_points, False)
                await Messager.edit_last_user_message(user.discord_id, turn_view_message)

            error_data = MessageHolder.read_last_error_data(user.discord_id)
            if error_data is not None:
                MessageHolder.delete_last_error_data(user.discord_id)
                await Messager.delete_message(error_data[0], error_data[1])

        return


class ViewMovement(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label=' ', style=nextcord.ButtonStyle.blurple, row=0, disabled=True)
    async def empty_button_1(self):
        """placeholder button to create space"""
        pass

    @nextcord.ui.button(label='▲', style=nextcord.ButtonStyle.blurple, row=0)
    async def move_one_up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile up"""
        await ViewMovement.move_one_tile('up', interaction.user.id, self.token, interaction)

    @nextcord.ui.button(label=' ', style=nextcord.ButtonStyle.blurple, row=0, disabled=True)
    async def empty_button_2(self):
        """placeholder button to create space"""
        pass

    @nextcord.ui.button(label='◄', style=nextcord.ButtonStyle.blurple, row=1)
    async def move_one_left(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile left"""
        await ViewMovement.move_one_tile('left', interaction.user.id, self.token, interaction)

    @nextcord.ui.button(label='▼', style=nextcord.ButtonStyle.blurple, row=1)
    async def move_one_down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile down"""
        await ViewMovement.move_one_tile('down', interaction.user.id, self.token, interaction)

    @nextcord.ui.button(label='►', style=nextcord.ButtonStyle.blurple, row=1)
    async def move_one_right(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile right"""
        await ViewMovement.move_one_tile('right', interaction.user.id, self.token, interaction)

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewMain(self.token))

    @staticmethod
    async def move_one_tile(direction, id_user, token, interaction: nextcord.Interaction):
        """shared function to move by one tile for all directions"""
        status, error_message = await HandlerMovement.handle_movement(direction, 1, id_user, token)

        error_data = MessageHolder.read_last_error_data(id_user)
        if not status:
            if error_data is not None:
                await Messager.edit_message(error_data[0], error_data[1], f"**{error_message}**")
            else:
                await Messager.send_dm_message(id_user, f"**{error_message}**", error=True)
            return

        if error_data is not None:
            MessageHolder.delete_last_error_data(id_user)
            await Messager.delete_message(error_data[0], error_data[1])

        lobby_players = Multiverse.get_game(token).user_list

        for user in lobby_players:
            asyncio.create_task(ViewMovement.display_movement_for_player(token, user))

    @staticmethod
    async def display_movement_for_player(token, user):
        """sends message to a player that another player moved"""
        player = Multiverse.get_game(token).get_player_by_id_user(user.discord_id)
        player_view = get_player_view(Multiverse.get_game(token), player)

        if player.active:
            turn_view_message = MessageTemplates.turn_view_template(
                token, Multiverse.get_game(token).get_active_player().name, player.action_points, True)
            await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message,
                                                  view=ViewMovement(token), files=[player_view])
        else:
            turn_view_message = MessageTemplates.turn_view_template(
                token, Multiverse.get_game(token).get_active_player().name, player.action_points,
                False)
            await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message,
                                                  files=[player_view])


class ViewAttack(View):
    def __init__(self, token, enemies):
        super().__init__()
        self.value = None
        self.token = token
        self.enemies = enemies
        self.attack_enemy_buttons = [Button(label=str(x + 1), style=nextcord.ButtonStyle.blurple)
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
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewMain(self.token))

    @staticmethod
    async def attack(enemy, id_user, token, interaction: nextcord.Interaction):
        """attack enemy nr enemy_number from the available enemy list with the main weapon"""
        status, new_enemies, error_message = await HandlerAttack.handle_attack(enemy, id_user, token)

        if not status:
            await interaction.response.send_message(error_message)
            return

        turn_view_message = MessageTemplates.turn_view_template(token)
        enemies_list_embed = MessageTemplates.attack_view_message_template(new_enemies)

        lobby_players = Multiverse.get_game(token).user_list

        for user in lobby_players:
            player = Multiverse.get_game(token).get_player_by_id_user(user.discord_id)
            player_view = get_player_view(Multiverse.get_game(token), player)

            if player.active:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message,
                                                      embed=enemies_list_embed, view=ViewAttack(token, new_enemies),
                                                      files=[player_view])
            else:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message,
                                                      files=[player_view])


class ViewCharacter(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Equipment', style=nextcord.ButtonStyle.blurple)
    async def show_equipment(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening equipment menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        equipment_embed = MessageTemplates.equipment_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              embed=equipment_embed, view=ViewEquipment(self.token))

    @nextcord.ui.button(label='Stats', style=nextcord.ButtonStyle.blurple)
    async def show_stats(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        stats_embed = MessageTemplates.stats_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              embed=stats_embed, view=ViewStats(self.token))

    @nextcord.ui.button(label='Skills', style=nextcord.ButtonStyle.blurple)
    async def show_skills(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        skills_embed = MessageTemplates.skills_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              embed=skills_embed, view=ViewCharacterSkills(self.token))

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewMain(self.token))


class ViewEquipment(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewCharacter(self.token))


class ViewStats(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewCharacter(self.token))


class ViewCharacterSkills(View):
    def __init__(self, token):
        super().__init__()
        self.value = None
        self.token = token

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewCharacter(self.token))


class ViewSkills(View):
    def __init__(self, token, skills):
        super().__init__()
        self.value = None
        self.token = token
        self.skills = skills
        self.use_skill_buttons = [Button(label=str(x + 1), style=nextcord.ButtonStyle.blurple)
                                  for x in range(10)]

        async def use_skill1(interaction: nextcord.Interaction):
            """callback function for button for using skill number 1"""
            await ViewSkills.use_skill(skills[0], interaction.user.id, self.token, interaction)

        async def use_skill2(interaction: nextcord.Interaction):
            """callback function for button for using skill number 2"""
            await ViewSkills.use_skill(skills[1], interaction.user.id, self.token, interaction)

        async def use_skill3(interaction: nextcord.Interaction):
            """callback function for button for using skill number 3"""
            await ViewSkills.use_skill(skills[2], interaction.user.id, self.token, interaction)

        async def use_skill4(interaction: nextcord.Interaction):
            """callback function for button for using skill number 4"""
            await ViewSkills.use_skill(skills[3], interaction.user.id, self.token, interaction)

        async def use_skill5(interaction: nextcord.Interaction):
            """callback function for button for using skill number 5"""
            await ViewSkills.use_skill(skills[4], interaction.user.id, self.token, interaction)

        async def use_skill6(interaction: nextcord.Interaction):
            """callback function for button for using skill number 6"""
            await ViewSkills.use_skill(skills[5], interaction.user.id, self.token, interaction)

        async def use_skill7(interaction: nextcord.Interaction):
            """callback function for button for using skill number 7"""
            await ViewSkills.use_skill(skills[6], interaction.user.id, self.token, interaction)

        async def use_skill8(interaction: nextcord.Interaction):
            """callback function for button for using skill number 8"""
            await ViewSkills.use_skill(skills[7], interaction.user.id, self.token, interaction)

        async def use_skill9(interaction: nextcord.Interaction):
            """callback function for button for using skill number 9"""
            await ViewSkills.use_skill(skills[8], interaction.user.id, self.token, interaction)

        async def use_skill10(interaction: nextcord.Interaction):
            """callback function for button for using skill number 10"""
            await ViewSkills.use_skill(skills[9], interaction.user.id, self.token, interaction)

        self.use_skill_buttons[0].callback = use_skill1
        self.use_skill_buttons[1].callback = use_skill2
        self.use_skill_buttons[2].callback = use_skill3
        self.use_skill_buttons[3].callback = use_skill4
        self.use_skill_buttons[4].callback = use_skill5
        self.use_skill_buttons[5].callback = use_skill6
        self.use_skill_buttons[6].callback = use_skill7
        self.use_skill_buttons[7].callback = use_skill8
        self.use_skill_buttons[8].callback = use_skill9
        self.use_skill_buttons[9].callback = use_skill10

        for i in range(len(skills)):
            self.add_item(self.use_skill_buttons[i])

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)
        turn_view_message = MessageTemplates.turn_view_template(
            self.token, Multiverse.get_game(self.token).get_active_player().name, player.action_points, True)

        await Messager.edit_last_user_message(user_id=interaction.user.id, content=turn_view_message,
                                              view=ViewMain(self.token))

    @staticmethod
    async def use_skill(skill, id_user, token, interaction: nextcord.Interaction):
        """attack enemy nr enemy_number from the available enemy list with the main weapon"""
        status, error_message = await HandlerSkills.handle_use_skill(skill, id_user, token)

        if not status:
            await interaction.response.send_message(error_message)
            return

        turn_view_message = MessageTemplates.turn_view_template(token)

        player = Multiverse.get_game(token).get_player_by_id_user(interaction.user.id)
        skills_list_embed = MessageTemplates.skills_message_template(player)
        lobby_players = Multiverse.get_game(token).user_list
        for user in lobby_players:
            player = Multiverse.get_game(token).get_player_by_id_user(user.discord_id)
            if player.active:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message,
                                                      embed=skills_list_embed, view=ViewSkills(token, player.skills))
            else:
                await Messager.edit_last_user_message(user_id=user.discord_id, content=turn_view_message)
