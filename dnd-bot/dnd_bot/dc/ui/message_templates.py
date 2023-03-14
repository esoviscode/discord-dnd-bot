import nextcord

from dnd_bot.dc.utils.utils import get_user_by_id
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.prototype.item import Item
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


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
    def equipment_message_template(player: Player):
        """message segment that shows the equipment of the player"""
        desc = ''
        desc = "🛡️ Equipped items:\n\n"
        desc += f'Helmet: {MessageTemplates.item_to_string_template(player.equipment.helmet)}\n'
        desc += f'Chest: {MessageTemplates.item_to_string_template(player.equipment.chest)}\n'
        desc += f'Leg Armor: {MessageTemplates.item_to_string_template(player.equipment.leg_armor)}\n'
        desc += f'Boots: {MessageTemplates.item_to_string_template(player.equipment.boots)}\n'
        desc += f'Left Hand: {MessageTemplates.item_to_string_template(player.equipment.left_hand)}\n'
        desc += f'Right Hand: {MessageTemplates.item_to_string_template(player.equipment.right_hand)}\n'
        desc += f'Accessory: {MessageTemplates.item_to_string_template(player.equipment.accessory)}\n'
        #
        # desc = "\n\n Your Items:\n"
        # for i, item in enumerate(player.items):
        #     desc += f'{i+1}. {item.name}'
        #
        embed = nextcord.Embed(title='Your equipment:', description=desc)
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
                                     f'HP: {player.hp}/{player.hp}', description=recent_action)
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
                                     f'HP: {player.hp}/{player.hp}', description=recent_action)
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

        embed.add_field(name="Lawful Good",
                        value="A lawful good character typically acts with compassion and always with honor and a "
                              "sense of duty. However, lawful good characters will often regret taking any action "
                              "they fear would violate their code, even if they recognize such action as being good.")

        embed.add_field(name="Neutral good",
                        value="A neutral good character typically acts altruistically, without regard for or against "
                              "lawful precepts such as rules or tradition. A neutral good character has no problems "
                              "with cooperating with lawful officials, but does not feel beholden to them. In the "
                              "event that doing the right thing requires the bending or breaking of rules, "
                              "they do not suffer the same inner conflict that a lawful good character would.")

        embed.add_field(name="Chaotic good",
                        value="A chaotic good character does what is necessary to bring about change for the better, "
                              "disdains bureaucratic organizations that get in the way of social improvement, "
                              "and places a high value on personal freedom, not only for oneself, but for others as "
                              "well. Chaotic good characters usually intend to do the right thing, but their methods "
                              "are generally disorganized and often out of sync with the rest of society.")

        embed.add_field(name="Lawful neutral",
                        value="A lawful neutral character typically believes strongly in lawful concepts such as "
                              "honor, order, rules, and tradition, but often follows a personal code in addition to, "
                              "or even in preference to, one set down by a benevolent authority.")

        embed.add_field(name="True neutral",
                        value="A neutral character (also called \"true neutral\") is neutral on both axes and tends "
                              "not to feel strongly towards any alignment, or actively seeks their balance.")

        embed.add_field(name="Chaotic neutral",
                        value="A chaotic neutral character is an individualist who follows their own heart and "
                              "generally shirks rules and traditions. Although chaotic neutral characters promote the "
                              "ideals of freedom, it is their own freedom that comes first; good and evil come second "
                              "to their need to be free.")

        embed.add_field(name="Lawful evil",
                        value="A lawful evil character sees a well-ordered system as being easier to exploit than to "
                              "necessarily follow.")

        embed.add_field(name="Neutral evil",
                        value="A neutral evil character is typically selfish and has no qualms about turning on "
                              "allies-of-the-moment, and usually makes allies primarily to further their own goals. A "
                              "neutral evil character has no compunctions about harming others to get what they want, "
                              "but neither will they go out of their way to cause carnage or mayhem when they see no "
                              "direct benefit for themselves. Another valid interpretation of neutral evil holds up "
                              "evil as an ideal, doing evil for evil's sake and trying to spread its influence.")

        embed.add_field(name="Chaotic evil",
                        value="A chaotic evil character tends to have no respect for rules, other people's lives, "
                              "or anything but their own desires, which are typically selfish and cruel. They set a "
                              "high value on personal freedom, but do not have much regard for the lives or freedom "
                              "of other people. Chaotic evil characters do not work well in groups because they "
                              "resent being given orders and usually do not behave themselves unless there is no "
                              "alternative.")

        return embed

    @staticmethod
    def class_form_view_message_template():
        """embed in character creation explaining classes"""

        desc = "A character class is a fundamental part of the identity and nature of characters.\n" \
               "Their capabilities, strengths, and weaknesses are largely defined by their class\n\n "

        desc += "Available classes are described below: \n"

        embed = nextcord.Embed(title=f'Class Form', description=desc)

        embed.add_field(name="Warrior ⚔",
                        value="Warriors share an unparalleled mastery with weapons and armor, and a thorough "
                              "knowledge of the skills of combat. They are well acquainted with death, both meting it "
                              "out and staring it defiantly in the face.")

        embed.add_field(name="Mage 🧙",
                        value="Mages are supreme magic-users, defined and united as a class by the spells they cast. "
                              "Drawing on the subtle weave of magic that permeates the cosmos, mages cast spells of "
                              "explosive fire, arcing lightning, subtle deception, brute-force mind control, "
                              "and much more.")

        embed.add_field(name="Ranger 🏹",
                        value="Far from the bustle of cities and towns, past the hedges that shelter the most distant "
                              "farms from the terrors of the wild, amid the dense-packed trees of trackless forests "
                              "and across wide and empty plains, rangers keep their unending watch.")

        return embed

    @staticmethod
    def race_form_view_message_template():
        """embed in character creation explaining races"""

        desc = "Each race has a distinct appearance, behavior and often range of statistics associated with it.\n\n "

        desc += "Available races are described below: \n"

        embed = nextcord.Embed(title=f'Race Form', description=desc)

        embed.add_field(name="Human 👨",
                        value="In the reckonings of most worlds, humans are the youngest of the common races, "
                              "late to arrive on the world scene and short-lived in comparison to dwarves, elves, "
                              "and dragons. Perhaps it is because of their shorter lives that they strive to achieve "
                              "as much as they can in the years they are given. Or maybe they feel they have "
                              "something to prove to the elder races, and that's why they build their mighty empires "
                              "on the foundation of conquest and trade. Whatever drives them, humans are the "
                              "innovators, the achievers, and the pioneers of the worlds.")

        embed.add_field(name="Elf 🧝",
                        value="Elves are a magical people of otherworldly grace, living in places of ethereal beauty, "
                              "in the midst of ancient forests or in silvery spires glittering with faerie light, "
                              "where soft music drifts through the air and gentle fragrances waft on the breeze. Elves "
                              "love nature and magic, art and artistry, music and poetry.")

        embed.add_field(name="Dwarf 🤏",
                        value="Kingdoms rich in ancient grandeur, halls carved into the roots of mountains, "
                              "the echoing of picks and hammers in deep mines and blazing forges, a commitment to "
                              "clan and tradition, and a burning hatred of goblins and orcs – these common threads "
                              "unite all dwarves.")

        return embed

    @staticmethod
    def stats_retrospective_form_view_message_template(user_id):
        """embed showing created character and his stats"""

        character = ChosenAttributes.chosen_attributes[user_id]

        embed = nextcord.Embed(title=f'Your Character')

        embed.add_field(name="Name",
                        value=character['name'],
                        inline=False)

        embed.add_field(name="Backstory",
                        value=character['backstory'],
                        inline=False)

        embed.add_field(name="Alignment",
                        value='-'.join(character['alignment']),
                        inline=False)

        embed.add_field(name="Class",
                        value=character['class'],
                        inline=False)

        embed.add_field(name="Race",
                        value=character['race'],
                        inline=False)

        embed.add_field(name="Stats",
                        value=f"HP: {character['hp']} \n"
                              f"Strength: {character['strength']}\n"
                              f"Dexterity: {character['dexterity']}\n"
                              f"Intelligence: {character['intelligence']}\n"
                              f"Charisma: {character['charisma']}\n"
                              f"Perception: {character['perception']}\n"
                              f"Initiative: {character['initiative']}\n"
                              f"Action points: {character['action points']}\n",
                        inline=False)

        return embed
