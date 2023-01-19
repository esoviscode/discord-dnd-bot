import nextcord

from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


class MessageTemplates:
    """Defines message templates, used mainly with discord embeds"""

    color_emojis = ["🔴", "🔵", "🟢", "🟡", "🟠", "🟣"]

    @staticmethod
    def lobby_view_message_template(lobby_token, players, campaign="📜 Storm King's Thunder\n\n"):

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

        embed.set_footer(text="The game will start when all the players are ready!")

        return embed

    @staticmethod
    def lobby_creation_message(token):
        desc = f"A fresh game for you and your team has been created! \n" \
               f"Make sure that everyone who wants to play is in " \
               f"this server!\n\n" \
               f"You can join by pressing the *Join* button or by using the `/join` command\n" \
               f"\n Game token: **`{token}`** "

        embed = nextcord.Embed(title=f"New Dungeons&Dragons :dragon: Lobby!", description=desc)
        embed.set_footer(text=None)

        return embed

    @staticmethod
    def map_view_template(token, active_player_name, action_points, is_players_turn):
        """message segment that shows the current state of the map"""
        map_view = '```'
        game = Multiverse.get_game(token)
        for entity_row in game.entities:
            for entity in entity_row:
                if entity is None:
                    map_view += '⬜'
                else:
                    if isinstance(entity, Rock):
                        map_view += '🪨'
                    elif isinstance(entity, Hole):
                        map_view += '🕳️'
                    elif isinstance(entity, Player):
                        map_view += '👨‍🦯'
            map_view += '\n'
        map_view += '```'

        if is_players_turn:
            map_view += f'{active_player_name}\'s turn | your action points: {action_points}\n'
        else:
            map_view += f'{active_player_name}\'s turn'

        return map_view

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
        """message segment that shows the equipment of the player"""
        desc = "Equipped items:\n"
        desc += f'Helmet: {player.equipment.helmet}\n'
        desc += f'Chest: {player.equipment.chest}\n'
        desc += f'Leg Armor: {player.equipment.leg_armor}\n'
        desc += f'Boots: {player.equipment.boots}\n'
        desc += f'Left Hand: {player.equipment.left_hand}\n'
        desc += f'Right Hand: {player.equipment.right_hand}\n'
        desc += f'Accessory: {player.equipment.accessory}\n'

        desc = "\n\n Your Items:\n"
        for i, item in enumerate(player.items):
            desc += f'{i+1}. {item.name}'

        embed = nextcord.Embed(title="Your equipment:",
                               description=desc)
        return embed


