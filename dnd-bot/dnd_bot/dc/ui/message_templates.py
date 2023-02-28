import nextcord

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.user import User


class MessageTemplates:
    """Defines message templates, used mainly with discord embeds"""

    color_emojis = ["🔴", "🔵", "🟢", "🟡", "🟠", "🟣"]

    @staticmethod
    def lobby_view_message_template(lobby_token, players, campaign="📜 Storm King's Thunder\n\n"):
        """message template that is sent to each player, showing the current state of the lobby"""

        desc = f'\nCampaign: {campaign}'

        for i, player in enumerate(players):
            if player[2]:
                desc += f'{MessageTemplates.color_emojis[i]} {player[0]} 👑'
            else:
                desc += f'{MessageTemplates.color_emojis[i]} {player[0]}'
            readiness = " :white_check_mark:" if player[1] else " :x:"
            desc += readiness + "\n\n"

        embed = nextcord.Embed(title=f'Dungeons&Dragons 🐉 Lobby #{lobby_token}',
                               description=desc)

        if Multiverse.get_game(lobby_token).all_users_ready():
            embed.set_footer(text='Ready to start the game!')
        else:
            embed.set_footer(text="The game can start when all the players are ready!")

        return embed

    @staticmethod
    def lobby_creation_message(token):
        """message template that shows up when a host creates a game"""
        desc = f"A fresh game for you and your team has been created! \n" \
               f"Make sure that everyone who wants to play is in " \
               f"this server!\n\n" \
               f"You can join by pressing the *Join* button or by using the `/join` command\n" \
               f"\n Game token: **`{token}`** "

        embed = nextcord.Embed(title=f"New Dungeons&Dragons :dragon: Lobby!", description=desc)
        embed.set_footer(text=None)

        return embed

    @staticmethod
    def turn_view_template(token, active_player_name, action_points, is_players_turn):
        """message segment that shows the current state of players turn"""
        if is_players_turn:
            turn_view = f'{active_player_name}\'s turn | your action points: {action_points}\n'
        else:
            turn_view = f'{active_player_name}\'s turn'

        return turn_view

    @staticmethod
    def attack_view_message_template(enemies):
        """message segment that shows the list of enemies to attack"""
        desc = ""
        for i, enemy in enumerate(enemies):
            desc += f'{i}. {enemy.name} ({enemy.hp}HP) at ({enemy.x}, {enemy.y})\n'

        embed = nextcord.Embed(title="Select enemy:",
                               description=desc)

        embed.set_footer(text="Choose the enemy you want to attack!")

        return embed

    @staticmethod
    def equipment_message_template(player):
        # TODO uncomment when player equipment is ready
        """message segment that shows the equipment of the player"""
        # desc = "Equipped items:\n"
        # desc += f'Helmet: {player.equipment.helmet}\n'
        # desc += f'Chest: {player.equipment.chest}\n'
        # desc += f'Leg Armor: {player.equipment.leg_armor}\n'
        # desc += f'Boots: {player.equipment.boots}\n'
        # desc += f'Left Hand: {player.equipment.left_hand}\n'
        # desc += f'Right Hand: {player.equipment.right_hand}\n'
        # desc += f'Accessory: {player.equipment.accessory}\n'
        #
        # desc = "\n\n Your Items:\n"
        # for i, item in enumerate(player.items):
        #     desc += f'{i+1}. {item.name}'
        #
        # embed = nextcord.Embed(title="Your equipment:",
        #                        description=desc)
        embed = nextcord.Embed(title='Your equipment:', description='')
        return embed

    @staticmethod
    def stats_message_template(player):
        """message segment that shows the stats of the player"""
        desc = ""
        desc += f'Strength: {player.strength}\n'
        desc += f'Dexterity: {player.dexterity}\n'
        desc += f'Max HP: {player.hp}\n'
        desc += f'Intelligence: {player.intelligence}\n'
        desc += f'Charisma: {player.charisma}\n'
        desc += f'Perception: {player.perception}\n'
        desc += f'Initiative: {player.initiative}\n'
        desc += f'Action Points: {player.action_points}\n'

        embed = nextcord.Embed(title="Your Stats:",
                               description=desc)
        return embed

    @staticmethod
    def skills_message_template(player):
        """message segment that shows the skills of the player"""
        desc = ""
        for i, skill in enumerate(player.skills):
            desc += f'{i+1}. {skill.name}\n'

        embed = nextcord.Embed(title="Your Skills:",
                               description=desc)
        return embed

    """this method is based on player_turn_embed which will be probably removed"""
    @staticmethod
    def creature_turn_embed(player: Player, active_creature: Creature, active_user_icon=None, recent_action=''):
        """message embed representing the active player actions and the player's stats"""
        embed = nextcord.Embed(title=f'Position: ({player.x}, {player.y}) | Action points: {player.action_points}/'
                                     f'{player.initial_action_points} | '
                                     f'HP: {player.hp}/{player.hp}', description=recent_action)
        embed.set_footer(text=f'{active_creature.name}\'s turn', icon_url=active_user_icon)

        return embed

    @staticmethod
    def player_turn_embed(player: Player, active_player: Player, active_user_icon=None, recent_action=''):
        """message embed representing the active player actions and the player's stats"""
        embed = nextcord.Embed(title=f'Position: ({player.x}, {player.y}) | Action points: {player.action_points}/'
                                     f'{player.initial_action_points} | '
                                     f'HP: {player.hp}/{player.hp}', description=recent_action)
        embed.set_footer(text=f'{active_player.name}\'s turn', icon_url=active_user_icon)

        return embed

