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
    def map_view_template(token, active_player_name, action_points):
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

        if active_player_name is None:
            map_view += f'Initial map view'
        else:
            map_view += f'\n{active_player_name}\'s turn | your action points: {action_points}'

        return map_view


