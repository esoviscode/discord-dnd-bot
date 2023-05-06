import nextcord

from dnd_bot.dc.utils.utils import get_user_by_id
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.utils import string_to_character_class, string_to_character_race


class MessageTemplates:
    """Defines message templates, used mainly with discord embeds"""

    color_emojis = ["🔴", "🔵", "🟢", "🟡", "🟠", "🟣"]

    @staticmethod
    def basic_embed(title="", description="", footer=""):
        """ returns simple embed """
        embed = nextcord.Embed(title=title, description=description)
        embed.set_footer(text=footer)
        return embed

    @staticmethod
    def lobby_view_message_template(lobby_token, players, campaign="📜 Storm King's Thunder\n\n"):
        """message template that is sent to each player, showing the current state of the lobby"""

        desc = f'\nCampaign: {campaign}'

        for i, player in enumerate(players):
            if player.is_host:
                desc += f'{MessageTemplates.color_emojis[i]} {player.username} 👑'
            else:
                desc += f'{MessageTemplates.color_emojis[i]} {player.username}'
            readiness = " :white_check_mark:" if player.is_ready else " :x:"
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
    def equipment_message_template(player: Player):
        """message segment that shows the equipment of the player"""

        eq = f'Helmet: *{MessageTemplates.item_to_string_template(player.equipment.helmet)}⠀*\n'
        eq += f'Chest: *{MessageTemplates.item_to_string_template(player.equipment.chest)}⠀*\n'
        eq += f'Leg Armor: *{MessageTemplates.item_to_string_template(player.equipment.leg_armor)}⠀*\n'
        eq += f'Boots: *{MessageTemplates.item_to_string_template(player.equipment.boots)}⠀*\n'
        eq += f'Left Hand: *{MessageTemplates.item_to_string_template(player.equipment.left_hand)}⠀*\n'
        eq += f'Right Hand: *{MessageTemplates.item_to_string_template(player.equipment.right_hand)}⠀*\n'
        eq += f'Accessory: *{MessageTemplates.item_to_string_template(player.equipment.accessory)}⠀*\n'

        backpack = f"⠀\n:school_satchel: **Backpack:**"

        backpack += "" if len(player.backpack) == 0 else "⠀\n"

        for item in player.backpack:
            backpack += f"*{item.name}*\n"

        embed = nextcord.Embed(title='Your equipment:', description="")
        embed.add_field(name="🛡️ **Equipment:**", value=eq, inline=True)
        embed.add_field(name=f":moneybag: **Money: {player.money}**", value=backpack, inline=True)
        return embed

    @staticmethod
    def item_to_string_template(item: Item):
        if item is None:
            return ''

        ret = f'{item.name} '

        if item.strength > 0:
            ret += f' - str 💪: {item.strength}'
        if item.intelligence > 0:
            ret += f' - int 🎓: {item.intelligence}'
        if item.dexterity > 0:
            ret += f' - dex 💨: {item.dexterity}'
        return ret

    @staticmethod
    def stats_message_template(player):
        """message segment that shows the stats of the player"""

        desc = f'Strength: {player.strength}\n'
        desc += f'Dexterity: {player.dexterity}\n'
        desc += f'Max HP: {player.max_hp}\n'
        desc += f'Intelligence: {player.intelligence}\n'
        desc += f'Charisma: {player.charisma}\n'
        desc += f'Perception: {player.perception}\n'
        desc += f'Initiative: {player.initiative}\n'
        desc += f'Action Points: {player.action_points}\n'

        embed = nextcord.Embed(title="Your Stats:", description=desc)
        return embed

    @staticmethod
    def skills_message_template(player):
        """message segment that shows the skills of the player"""
        desc = ""
        for i, skill in enumerate(player.skills):
            desc += f'{i + 1}. {skill.name}\n'

        embed = nextcord.Embed(title="Your Skills:",
                               description=desc)
        return embed

    @staticmethod
    async def creature_turn_embed(token, user_id, recent_action=''):
        """message embed representing the active creature's actions and the player's stats"""
        player = Multiverse.get_game(token).get_player_by_id_user(user_id)

        active_creature = Multiverse.get_game(token).get_active_creature()

        embed = nextcord.Embed(title=f'Position: ({player.x}, {player.y}) | Action points: {player.action_points}/'
                                     f'{player.initial_action_points} | '
                                     f'HP: {player.hp}/{player.max_hp}', description=recent_action)
        if isinstance(active_creature, Player):
            active_user = await get_user_by_id(active_creature.discord_identity)
            active_user_icon = active_user.display_avatar.url
            embed.set_footer(text=f'{active_creature.name}\'s turn', icon_url=active_user_icon)
        else:
            embed.set_footer(text=f'{active_creature.name}\'s turn')

        return embed

    @staticmethod
    def player_turn_embed(player: Player, active_player: Player, active_user_icon=None, recent_action=''):
        """message embed representing the active player actions and the player's stats"""
        embed = nextcord.Embed(title=f'Position: ({player.x}, {player.y}) | Action points: {player.action_points}/'
                                     f'{player.initial_action_points} | '
                                     f'HP: {player.hp}/{player.max_hp}', description=recent_action)
        embed.set_footer(text=f'{active_player.name}\'s turn', icon_url=active_user_icon)

        return embed

    @staticmethod
    def end_turn_recent_action_message(ending_creature):
        return f"{ending_creature.name} has ended their turn"

    @staticmethod
    def character_creation_start_message_template():
        """embed at the beginning of character creation process"""

        desc = "In the following forms you will be able to create the character for this game.\n\n" \
               " Some of the attributes like name, backstory and alignment are just for you in order to immerse" \
               " better with your character. \n\n" \
               "The other ones: especially race and class can have a direct impact on" \
               " your future interactions and attributes "

        embed = nextcord.Embed(title=f'Character Creation', description=desc)

        return embed

    @staticmethod
    def alignment_form_view_message_template():
        """embed in character creation explaining alignment"""

        desc = "Alignment is a categorization of the ethical and moral perspective of your character.\n\n"
        desc += "The nine alignments can be described as follows: \n"

        embed = nextcord.Embed(title=f'Alignment Form', description=desc)

        embed.add_field(name="🏛️👼 Lawful Good",
                        value="Believes in the value of order, rules, and justice. Strives to help others and do the "
                              "right thing.")

        embed.add_field(name="🕊️💕 Neutral good",
                        value="Values freedom, fairness, and compassion. Tries to do good without necessarily "
                              "following strict codes or laws.")

        embed.add_field(name="🗽👥 Chaotic good",
                        value="Values personal freedom and autonomy, and sees themselves as a champion for the "
                              "oppressed or underdog.")

        embed.add_field(name="📜⚖️ Lawful neutral",
                        value="Values order and structure above all else, and seeks to maintain a balanced society, "
                              "regardless of personal feelings or beliefs.")

        embed.add_field(name="🤔💭 True neutral",
                        value="Has no strong moral compass, and values balance above all else, sometimes to the point "
                              "of indecision or neutrality in difficult situations.")

        embed.add_field(name="🌪️😜 Chaotic neutral",
                        value="Values personal freedom and individuality above all else, often at the expense of "
                              "others or social order.")

        embed.add_field(name="💼💰 Lawful evil",
                        value="Values power and order above all else, and is willing to commit evil acts in service "
                              "of their own goals or to maintain their own power.")

        embed.add_field(name="💀😈 Neutral evil",
                        value="Values personal gain above all else, and will do whatever it takes to achieve it, "
                              "regardless of the consequences or harm to others.")

        embed.add_field(name="🔥👹Chaotic evil",
                        value="Values personal freedom and individuality above all else, and seeks to destroy order "
                              "and sow chaos wherever they go, often through violent and destructive means.")

        return embed

    @staticmethod
    def class_form_view_message_template():
        """embed in character creation explaining classes"""

        desc = "A character class is a fundamental part of the identity and nature of characters.\n" \
               "Their capabilities, strengths, and weaknesses are largely defined by their class\n\n "

        desc += "Available classes are described below: \n"

        embed = nextcord.Embed(title=f'Class Form', description=desc)

        from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
        for character_class in HandlerCharacterCreation.classes:
            MessageTemplates.add_class_or_race_field(character_class, embed)

        return embed

    @staticmethod
    def race_form_view_message_template():
        """embed in character creation explaining races"""

        desc = "Each race has a distinct appearance, behavior and often range of statistics associated with it.\n\n "

        desc += "Available races are described below: \n"

        embed = nextcord.Embed(title=f'Race Form', description=desc)

        from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
        for character_race in HandlerCharacterCreation.races:
            MessageTemplates.add_class_or_race_field(character_race, embed)

        return embed

    @staticmethod
    def add_class_or_race_field(character_class_or_race, embed):
        """Function adding fields describing character class
            :param character_class_or_race: python class of the character class or race
            :param embed: embed to which the fields are appended"""

        embed.add_field(name=f"{character_class_or_race.name} {character_class_or_race.emoji}",
                        value=character_class_or_race.long_description,
                        inline=True)

        class_stats_description = ""
        if character_class_or_race.base_hp > 0:
            class_stats_description += f"{'💖'}  hp:  {character_class_or_race.base_hp}\n\n"
        if character_class_or_race.base_strength > 0:
            class_stats_description += f"{'💪'}  strength:  {character_class_or_race.base_strength}\n\n"
        if character_class_or_race.base_dexterity > 0:
            class_stats_description += f"{'👋'}  dexterity:  {character_class_or_race.base_dexterity}\n\n"
        if character_class_or_race.base_intelligence > 0:
            class_stats_description += f"{'🧠'}  intelligence:  {character_class_or_race.base_intelligence}\n\n"
        if character_class_or_race.base_charisma > 0:
            class_stats_description += f"{'😎‍'}  charisma:  {character_class_or_race.base_charisma}\n\n"
        if character_class_or_race.base_perception > 0:
            class_stats_description += f"{'👀'}  perception:  {character_class_or_race.base_perception}\n\n"
        if character_class_or_race.base_action_points > 0:
            class_stats_description += f"{'✊'}  action points:  {character_class_or_race.base_action_points}\n\n"
        if character_class_or_race.base_initiative > 0:
            class_stats_description += f"{'✨'}  initiative:  {character_class_or_race.base_initiative}\n\n"

        embed.add_field(name="",
                        value=class_stats_description,
                        inline=True)

        embed.add_field(name="",
                        value="\n\u200b",
                        inline=False)

    @staticmethod
    def stats_retrospective_form_view_message_template(user_id, token):
        """embed showing created character and his stats"""

        character = ChosenAttributes.chosen_attributes[(user_id, token)]
        character_class = string_to_character_class(character['class'])
        character_race = string_to_character_race(character['race'])

        embed = nextcord.Embed(title=f'Your Character')

        embed.add_field(name="Name",
                        value=f"{character['name']}",
                        inline=False)

        embed.add_field(name="Backstory",
                        value=f"{character['backstory']}",
                        inline=False)

        embed.add_field(name="Alignment",
                        value=f"{'-'.join(character['alignment'])}",
                        inline=False)

        embed.add_field(name="Class",
                        value=f"{character_class.emoji} {character['class']}",
                        inline=True)

        embed.add_field(name="Race",
                        value=f"{character_race.emoji} {character['race']}",
                        inline=True)

        embed.add_field(name="Stats",
                        value=f"{'💖'} HP: {character['hp']}"
                              f" ({character_class.base_hp + character_race.base_hp} + "
                              f"{character['hp'] - character_class.base_hp - character_race.base_hp}) \n\n"
                              
                              f"{'💪'} Strength: {character['strength']}"
                              f" ({character_class.base_strength + character_race.base_strength} + "
                              f"{character['strength'] - character_class.base_strength - character_race.base_strength}) \n\n "
                              
                              f"{'👋'} Dexterity: {character['dexterity']}"
                              f" ({character_class.base_dexterity + character_race.base_dexterity} + "
                              f"{character['dexterity'] - character_class.base_dexterity - character_race.base_dexterity}) \n\n "
                              
                              f"{'🧠'} Intelligence: {character['intelligence']}"
                              f" ({character_class.base_intelligence + character_race.base_intelligence} + "
                              f"{character['intelligence'] - character_class.base_intelligence - character_race.base_intelligence}) \n\n "
                              
                              f"{'😎‍'} Charisma: {character['charisma']}"
                              f" ({character_class.base_charisma + character_race.base_charisma} + "
                              f"{character['charisma'] - character_class.base_charisma - character_race.base_charisma}) \n\n "
                              
                              f"{'👀'} Perception: {character['perception']}"
                              f" ({character_class.base_perception + character_race.base_perception} + "
                              f"{character['perception'] - character_class.base_perception - character_race.base_perception}) \n\n "
                              
                              f"{'✊'} Initiative: {character['initiative']}"
                              f" ({character_class.base_initiative + character_race.base_initiative} + "
                              f"{character['initiative'] - character_class.base_initiative - character_race.base_initiative}) \n\n "
                              
                              f"{'✨'} Action points: {character['action points']}"
                              f" ({character_class.base_action_points + character_race.base_action_points} + "
                              f"{character['action points'] - character_class.base_action_points - character_race.base_action_points}) \n\n ",
                        inline=False)

        return embed

    @staticmethod
    def more_actions_template():
        """ returns embed for more actions menu"""
        title = "More actions"
        description = "If available, here you can find more actions"
        embed = nextcord.Embed(title=title, description=description)
        return embed

    @staticmethod
    def loot_corpse_action(player_name="", name="", money="", items=None):
        """ returns message template for recent action after looting the corpse """
        if items is None:
            items = []
        message = f"{player_name} found **{money}** coin{'' if money == 1 else 's'} :coin: while looting {name}!\n"
        if len(items) > 0:
            message += f"\nThey also found:\n"
            for item in items:
                message += f"ㅤ- *{item.name}*\n"
        return message
