from threading import Lock

import nextcord
from nextcord.ui import Button
from nextcord.ui import View

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.handler_views import HandlerViews
from dnd_bot.logic.game.handler_attack import HandlerAttack
from dnd_bot.logic.game.handler_loot_corpse import HandlerLootCorpse
from dnd_bot.logic.game.handler_manage_items import HandlerManageItems
from dnd_bot.logic.game.handler_movement import HandlerMovement
from dnd_bot.logic.game.handler_skills import HandlerSkills
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.exceptions import DiscordDndBotException
from dnd_bot.logic.utils.utils import get_player_view

s_print_lock = Lock()


class ViewGame(View):
    def __init__(self, token, user_discord_id):
        """
        :param token: game token
        :param user_discord_id: discord identity of user that this view is sent to
        """
        super().__init__(timeout=None)
        self.value = None
        self.token = token
        self.user_discord_id = user_discord_id
        self.game = Multiverse.get_game(token)

    async def cancel(self, interaction: nextcord.Interaction, files=None):
        """button for moving back to main menu"""

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)

        self.game.players_views[self.user_discord_id] = (ViewMain, [])
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[turn_view_embed],
                                              view=ViewMain(self.token, interaction.user.id),
                                              files=files)

    async def character_view_options(self, interaction: nextcord.Interaction):
        """shared handler for character view"""

        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)

        active_creature = Multiverse.get_game(self.token).get_active_creature()

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)

        self.game.players_views[self.user_discord_id] = (ViewCharacterNonActive, [])

        if isinstance(active_creature, Player) and player.discord_identity == active_creature.discord_identity:
            await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[turn_view_embed],
                                                  view=ViewCharacter(self.token, interaction.user.id))
        else:
            await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[turn_view_embed],
                                                  view=ViewCharacterNonActive(self.token, interaction.user.id))

    async def character_view_equipment(self, interaction: nextcord.Interaction):
        """shared handler for equipment view"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)

        equipment_embed = MessageTemplates.equipment_message_template(player)
        self.game.players_views[self.user_discord_id] = (ViewEquipment, [equipment_embed])
        await Messager.edit_last_user_message(user_id=interaction.user.id,
                                              embeds=[turn_view_embed, equipment_embed],
                                              view=ViewEquipment(self.token, interaction.user.id))

    async def character_view_stats(self, interaction: nextcord.Interaction):
        """shared handler for stats view"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)

        stats_embed = MessageTemplates.stats_message_template(player)
        self.game.players_views[self.user_discord_id] = (ViewStats, [stats_embed])
        await Messager.edit_last_user_message(user_id=interaction.user.id,
                                              embeds=[turn_view_embed, stats_embed],
                                              view=ViewStats(self.token, interaction.user.id))

    async def character_view_skills(self, interaction: nextcord.Interaction):
        """shared handler for character view"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)

        skills_embed = MessageTemplates.skills_message_template(player)
        self.game.players_views[self.user_discord_id] = (ViewSkills, [skills_embed])
        await Messager.edit_last_user_message(user_id=interaction.user.id,
                                              embeds=[turn_view_embed, skills_embed],
                                              view=ViewCharacterSkills(self.token, interaction.user.id))


class ViewMain(ViewGame):

    @nextcord.ui.button(label='Attack', style=nextcord.ButtonStyle.blurple, custom_id='attack-main-button')
    async def attack(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening attack menu"""
        game = Multiverse.get_game(self.token)
        player = game.get_player_by_id_user(interaction.user.id)
        player.attack_mode = True

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)
        self.game.players_views[self.user_discord_id] = (ViewAttack, [])
        await Messager.edit_last_user_message(user_id=interaction.user.id,
                                              embeds=[turn_view_embed],
                                              view=ViewAttack(self.token, self.user_discord_id),
                                              files=[get_player_view(game, player, True)])

    @nextcord.ui.button(label='Move', style=nextcord.ButtonStyle.blurple, custom_id='move-main-button')
    async def move(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening move menu"""
        game = Multiverse.get_game(self.token)

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[turn_view_embed],
                                              view=ViewMovement(self.token, interaction.user.id))
        game.players_views[str(interaction.user.id)] = (ViewMovement, [])

    @nextcord.ui.button(label='Skill', style=nextcord.ButtonStyle.blurple, custom_id='skill-main-button')
    async def skill(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening skill menu"""
        player = Multiverse.get_game(self.token).get_player_by_id_user(interaction.user.id)

        turn_view_embed = await MessageTemplates.creature_turn_embed(self.token, interaction.user.id)
        skills_list_embed = MessageTemplates.skills_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id,
                                              embeds=[turn_view_embed, skills_list_embed],
                                              view=ViewSkills(self.token, self.user_discord_id))

    @nextcord.ui.button(label='Character', style=nextcord.ButtonStyle.blurple, custom_id='character-main-button')
    async def character(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening character menu"""
        await super().character_view_options(interaction)

    @nextcord.ui.button(label='More actions', style=nextcord.ButtonStyle.danger, custom_id='more-main-button')
    async def more_actions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening more actions menu"""
        game = Multiverse.get_game(self.token)

        embed = MessageTemplates.more_actions_template()
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[embed],
                                              view=ViewMoreActions(self.token, interaction.user.id))
        game.players_views[str(interaction.user.id)] = (ViewMoreActions, [])

    @nextcord.ui.button(label='End turn', style=nextcord.ButtonStyle.danger, custom_id='end-turn-main-button')
    async def end_turn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for ending turn"""
        try:
            await HandlerMovement.handle_end_turn(interaction.user.id, self.token)
            from dnd_bot.logic.game.handler_game import HandlerGame
            await HandlerGame.end_turn(self.token)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(user_id=interaction.user.id, content=str(e))


class ViewMovement(ViewGame):

    @nextcord.ui.button(label='‎‎', style=nextcord.ButtonStyle.blurple, row=0, disabled=True,
                        custom_id='move-empty-1')
    async def empty_button_1(self):
        """placeholder button to create space"""
        pass

    @nextcord.ui.button(label='▲', style=nextcord.ButtonStyle.blurple, row=0, custom_id='move-up')
    async def move_one_up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile up"""
        await ViewMovement.move_one_tile('up', interaction.user.id, self.token)

    @nextcord.ui.button(label='‎‎', style=nextcord.ButtonStyle.blurple, row=0, disabled=True,
                        custom_id='move-empty-2')
    async def empty_button_2(self):
        """placeholder button to create space"""
        pass

    @nextcord.ui.button(label='◄', style=nextcord.ButtonStyle.blurple, row=1, custom_id='move-left')
    async def move_one_left(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile left"""
        await ViewMovement.move_one_tile('left', interaction.user.id, self.token)

    @nextcord.ui.button(label='▼', style=nextcord.ButtonStyle.blurple, row=1, custom_id='move-down')
    async def move_one_down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile down"""
        await ViewMovement.move_one_tile('down', interaction.user.id, self.token)

    @nextcord.ui.button(label='►', style=nextcord.ButtonStyle.blurple, row=1, custom_id='move-right')
    async def move_one_right(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving one tile right"""
        await ViewMovement.move_one_tile('right', interaction.user.id, self.token)

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='move-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().cancel(interaction)

    @staticmethod
    async def move_one_tile(direction, id_user, token):
        """shared function to move by one tile for all directions"""
        try:
            await HandlerMovement.handle_movement(direction, 1, id_user, token)

            Multiverse.get_game(token).players_views[id_user] = (ViewMovement, [])

            await Messager.delete_last_user_error_message(id_user)

            active_player = Multiverse.get_game(token).active_creature
            recent_action = f'{active_player.name} has moved to ({active_player.x},{active_player.y})'
            await HandlerViews.display_views_for_users(token, recent_action)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(id_user, f"**{e}**")


class ViewMoreActions(ViewGame):
    def __init__(self, token, user_discord_id):
        super().__init__(token, user_discord_id)

        loot_corpse_button = Button(label='Loot corpse', style=nextcord.ButtonStyle.blurple, row=0,
                                    custom_id='more-actions-loot')
        loot_corpse_button.callback = self.loot_corpse

        cancel_button = Button(label='Cancel', style=nextcord.ButtonStyle.red, row=1,
                               custom_id='more-actions-cancel')
        cancel_button.callback = self.cancel

        game: Game = Multiverse.get_game(token)
        self.player = game.get_player_by_id_user(user_discord_id)
        # determine if looting corpses is available
        if self.player.can_loot_corpse:
            self.add_item(loot_corpse_button)

        self.add_item(cancel_button)

    async def loot_corpse(self, interaction: nextcord.Interaction):
        """ button callback for looting the corpse"""
        try:
            await HandlerLootCorpse.handle_loot_corpse(self.player)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(interaction.user.id, f"**{e}**")

    async def cancel(self, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().cancel(interaction)


class ViewAttack(ViewGame):
    def __init__(self, token, user_discord_id):
        super().__init__(token, user_discord_id)
        game = Multiverse.get_game(token)
        self.enemies = game.get_attackable_enemies_for_player(game.get_player_by_id_user(user_discord_id))
        enemies_select_options = []
        self.enemies_to_attack = len(self.enemies)

        if self.enemies_to_attack > 0:
            for enemy in self.enemies:
                enemies_select_options.append(nextcord.SelectOption(
                    label=f"{enemy.name} ({enemy.hp}HP) at ({enemy.x}, {enemy.y})",
                    value=enemy.id
                ))
            self.select_enemy_to_attack_list = nextcord.ui.Select(
                placeholder="Choose an enemy to attack",
                options=enemies_select_options,
                row=0
            )

            self.add_item(self.select_enemy_to_attack_list)

        attack_button = Button(label='Attack', style=nextcord.ButtonStyle.green, row=1,
                               custom_id='attack-action-button')
        attack_button.callback = self.attack_button
        attack_button.disabled = self.enemies_to_attack == 0
        self.add_item(attack_button)

        cancel_button = Button(label='Cancel', style=nextcord.ButtonStyle.red, row=1, custom_id='attack-cancel-button')
        cancel_button.callback = self.cancel
        self.add_item(cancel_button)

    async def attack_button(self, interaction: nextcord.Interaction):
        if self.enemies_to_attack == 0:
            return
        if self.select_enemy_to_attack_list.values:
            await ViewAttack.attack(self.select_enemy_to_attack_list.values[0],
                                    interaction.user.id, self.token, interaction)

    async def cancel(self, interaction: nextcord.Interaction):
        player = self.game.get_player_by_id_user(interaction.user.id)
        await super().cancel(interaction, [get_player_view(self.game, player)])

    @staticmethod
    async def attack(target_id, id_user, token, interaction: nextcord.Interaction):
        """attack enemy nr enemy_number from the available enemy list with the main weapon"""
        try:
            game = Multiverse.get_game(token)
            player = game.get_player_by_id_user(id_user)
            target = game.get_entity_by_id(target_id)

            message = await HandlerAttack.handle_attack(player, target, token)

            await HandlerViews.display_views_for_users(token, message)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(id_user, f"**{e}**")


class ViewCharacter(ViewGame):

    @nextcord.ui.button(label='Equipment', style=nextcord.ButtonStyle.blurple, custom_id='character-equipment')
    async def character_view_equipment(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening equipment menu"""
        await super().character_view_equipment(interaction)

    @nextcord.ui.button(label='Stats', style=nextcord.ButtonStyle.blurple, custom_id='character-stats')
    async def character_view_stats(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        await super().character_view_stats(interaction)

    @nextcord.ui.button(label='Skills', style=nextcord.ButtonStyle.blurple, custom_id='character-skills')
    async def show_skills(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        await super().character_view_skills(interaction)

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='character-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().cancel(interaction)


class ViewCharacterNonActive(ViewGame):

    @nextcord.ui.button(label='Equipment', style=nextcord.ButtonStyle.blurple, custom_id='nonactive-equipment')
    async def character_view_equipment(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening equipment menu"""
        await super().character_view_equipment(interaction)

    @nextcord.ui.button(label='Stats', style=nextcord.ButtonStyle.blurple, custom_id='nonactive-stats')
    async def character_view_stats(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening stats menu"""
        await super().character_view_stats(interaction)

    @nextcord.ui.button(label='Skills', style=nextcord.ButtonStyle.blurple, custom_id='nonactive-skills')
    async def character_view_skills(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for opening skills menu"""
        await super().character_view_skills(interaction)


class ViewManageItems(ViewGame):
    """ view for managing player's equipment"""
    def __init__(self, token, user_discord_id):
        super().__init__(token, user_discord_id)

        self.player = Multiverse.get_game(token).get_player_by_id_user(user_discord_id)

        if len(self.player.backpack) > 0:
            item_select_options = []

            for count, item in enumerate(self.player.backpack):
                item_select_options.append(nextcord.SelectOption(
                    label=f"{item.name}",
                    value=str(count)  # TODO should be item.id, but for now database is not functioning properly
                ))
            self.select_list = nextcord.ui.Select(
                placeholder="Choose an item to manage",
                options=item_select_options,
                row=0
            )

            self.add_item(self.select_list)

            equip_button = Button(label='Equip item', style=nextcord.ButtonStyle.blurple, custom_id='manage-items-equip'
                                                                                                    '-button')
            equip_button.callback = self.equip
            self.add_item(equip_button)

            remove_button = Button(label='Remove item', style=nextcord.ButtonStyle.blurple,
                                   custom_id='manage-items-remove-button')
            remove_button.callback = self.remove
            self.add_item(remove_button)

        cancel_button = Button(label='Cancel', style=nextcord.ButtonStyle.red, row=1, custom_id='attack-cancel-button')
        cancel_button.callback = self.cancel
        self.add_item(cancel_button)

    async def equip(self, interaction: nextcord.Interaction):
        await HandlerManageItems.equip_item(self.player, int(self.select_list.values[0]))
        embed = MessageTemplates.equipment_message_template(self.player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[embed],
                                              view=ViewManageItems(self.token, interaction.user.id))

    async def remove(self, interaction: nextcord.Interaction):
        await HandlerManageItems.remove_item(self.player, int(self.select_list.values[0]))
        embed = MessageTemplates.equipment_message_template(self.player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[embed],
                                              view=ViewManageItems(self.token, interaction.user.id))

    async def cancel(self, interaction: nextcord.Interaction):
        await super().cancel(interaction, [get_player_view(self.game, self.player)])


class ViewEquipment(ViewGame):

    @nextcord.ui.button(label='Manage items', style=nextcord.ButtonStyle.blurple, custom_id='equipment-manage-items')
    async def manage_items(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for managing items"""
        game = Multiverse.get_game(self.token)
        player = game.get_player_by_id_user(interaction.user.id)
        embed = MessageTemplates.equipment_message_template(player)
        await Messager.edit_last_user_message(user_id=interaction.user.id, embeds=[embed],
                                              view=ViewManageItems(self.token, interaction.user.id))
        game.players_views[str(interaction.user.id)] = (ViewManageItems, [])

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='equipment-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().character_view_options(interaction)


class ViewStats(ViewGame):

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='stats-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to character view"""
        await super().character_view_options(interaction)


class ViewCharacterSkills(ViewGame):

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='stats-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().character_view_options(interaction)


class ViewSkills(ViewGame):
    def __init__(self, token, user_discord_id):
        super().__init__(token, user_discord_id)
        self.skills = []  # TODO no way to check the available skills for now
        self.use_skill_buttons = [Button(label=str(x + 1), style=nextcord.ButtonStyle.blurple,
                                         custom_id=f'use-skill-button-{x}')
                                  for x in range(10)]

        async def use_skill1(interaction: nextcord.Interaction):
            """callback function for button for using skill number 1"""
            await ViewSkills.use_skill(self.skills[0], interaction.user.id, self.token, interaction)

        async def use_skill2(interaction: nextcord.Interaction):
            """callback function for button for using skill number 2"""
            await ViewSkills.use_skill(self.skills[1], interaction.user.id, self.token, interaction)

        async def use_skill3(interaction: nextcord.Interaction):
            """callback function for button for using skill number 3"""
            await ViewSkills.use_skill(self.skills[2], interaction.user.id, self.token, interaction)

        async def use_skill4(interaction: nextcord.Interaction):
            """callback function for button for using skill number 4"""
            await ViewSkills.use_skill(self.skills[3], interaction.user.id, self.token, interaction)

        async def use_skill5(interaction: nextcord.Interaction):
            """callback function for button for using skill number 5"""
            await ViewSkills.use_skill(self.skills[4], interaction.user.id, self.token, interaction)

        async def use_skill6(interaction: nextcord.Interaction):
            """callback function for button for using skill number 6"""
            await ViewSkills.use_skill(self.skills[5], interaction.user.id, self.token, interaction)

        async def use_skill7(interaction: nextcord.Interaction):
            """callback function for button for using skill number 7"""
            await ViewSkills.use_skill(self.skills[6], interaction.user.id, self.token, interaction)

        async def use_skill8(interaction: nextcord.Interaction):
            """callback function for button for using skill number 8"""
            await ViewSkills.use_skill(self.skills[7], interaction.user.id, self.token, interaction)

        async def use_skill9(interaction: nextcord.Interaction):
            """callback function for button for using skill number 9"""
            await ViewSkills.use_skill(self.skills[8], interaction.user.id, self.token, interaction)

        async def use_skill10(interaction: nextcord.Interaction):
            """callback function for button for using skill number 10"""
            await ViewSkills.use_skill(self.skills[9], interaction.user.id, self.token, interaction)

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

        for i in range(len(self.skills)):
            self.add_item(self.use_skill_buttons[i])

    @nextcord.ui.button(label='Cancel', style=nextcord.ButtonStyle.red, custom_id='skills-cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """button for moving back to main menu"""
        await super().cancel(interaction)

    @staticmethod
    async def use_skill(skill, id_user, token, interaction: nextcord.Interaction):
        """attack enemy nr enemy_number from the available enemy list with the main weapon"""
        try:
            message = await HandlerSkills.handle_use_skill(skill, id_user, token)
            await HandlerViews.display_views_for_users(token, message)
        except DiscordDndBotException as e:
            await Messager.send_dm_error_message(id_user, f"**{e}**")
