import random

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerCharacterCreation:
    """Handles character creation process"""

    @staticmethod
    async def start_character_creation(token, user_id):
        """Called when host clicks start in lobby
            :param token: game token
            :param user_id: id of the user who ran the command or the host that pressed the start button
            :return: status, (if start was successful, users list, optional error message)
            """
        game = Multiverse.get_game(token)
        game_id = DatabaseConnection.get_id_game_from_game_token(token)

        if game_id is None:
            return False, [], ":no_entry: Error creating game!"

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if not game.all_users_ready():
            return False, [], f':warning: Not all the players are ready!'

        if game.game_state == 'LOBBY':
            game.game_state = "STARTING"
            DatabaseConnection.update_game_state(game_id, 'STARTING')

            if game_id is None:
                game.game_state = 'LOBBY'
                return False, [], ":warning: Error creating game!"
            for user in game.user_list:
                DatabaseConnection.add_user(game_id, user.discord_id)
                ChosenAttributes.add_empty_user(user.discord_id)
                game.find_user(user.discord_id).is_ready = False

            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: This game has already started!'

    @staticmethod
    async def assign_attribute_values(user_id):
        """Called to choose attribute values based on the user's choices in character creation process
            :param user_id: id of the user who finished character creation"""

        character = ChosenAttributes.chosen_attributes[user_id]
        character_class = str.lower(character['class'])
        character_race = str.lower(character['race'])

        # TODO make new classes: Class and Warrior to keep following information about base attribute values
        base_hp = {'human': 15, 'elf': 10, 'dwarf': 20}
        base_strength = {'human': 6, 'elf': 3, 'dwarf': 10}
        base_dexterity = {'human': 6, 'elf': 10, 'dwarf': 3}
        base_intelligence = {'human': 10, 'elf': 6, 'dwarf': 3}
        base_charisma = {'human': 6, 'elf': 3, 'dwarf': 10}
        base_perception = {'human': 2, 'elf': 3, 'dwarf': 1}
        base_action_points = {'human': 10, 'elf': 6, 'dwarf': 3}

        base_initiative = {'warrior': 6, 'mage': 3, 'ranger': 10}

        points_to_distribute_randomly = 10

        additional_strength = random.randint(0, 2)
        strength = base_strength[character_race] + additional_strength
        points_to_distribute_randomly -= additional_strength
        ChosenAttributes.chosen_attributes[user_id]['strength'] = strength

        additional_dexterity = random.randint(0, 2)
        dexterity = base_dexterity[character_race] + additional_dexterity
        points_to_distribute_randomly -= additional_dexterity
        ChosenAttributes.chosen_attributes[user_id]['dexterity'] = dexterity

        additional_intelligence = random.randint(0, 2)
        intelligence = base_intelligence[character_race] + additional_intelligence
        points_to_distribute_randomly -= additional_intelligence
        ChosenAttributes.chosen_attributes[user_id]['intelligence'] = intelligence

        additional_charisma = random.randint(0, 2)
        charisma = base_charisma[character_race] + additional_charisma
        points_to_distribute_randomly -= additional_charisma
        ChosenAttributes.chosen_attributes[user_id]['charisma'] = charisma

        additional_perception = random.randint(0, 1)
        perception = base_perception[character_race] + additional_perception
        points_to_distribute_randomly -= additional_perception
        ChosenAttributes.chosen_attributes[user_id]['perception'] = perception

        additional_action_points = random.randint(0, 2)
        action_points = base_action_points[character_race] + additional_action_points
        points_to_distribute_randomly -= additional_action_points
        ChosenAttributes.chosen_attributes[user_id]['action points'] = action_points

        additional_initiative = random.randint(0, 2)
        initiative = base_initiative[character_class] + additional_initiative
        points_to_distribute_randomly -= additional_initiative
        ChosenAttributes.chosen_attributes[user_id]['initiative'] = initiative

        ChosenAttributes.chosen_attributes[user_id]['hp'] = base_hp[character_race] + points_to_distribute_randomly

    @staticmethod
    async def handle_character_creation_finished(user_id, token) -> (bool, bool, str):
        """handles finishing of character creation process; if all the players finished it the game is started
                        :param user_id: id of the user who finished character creation process
                        :param token: game token
                        :return: status, status of other players (if all of them are ready) optional error message)
                        """
        game = Multiverse.get_game(token)
        game_id = DatabaseConnection.get_id_game_from_game_token(token)

        if game is None:
            return False, False, f':warning: Game of provided token doesn\'t exist!'

        game.find_user(user_id).is_ready = True

        if game.all_users_ready():
            game.game_state = 'ACTIVE'
            DatabaseConnection.update_game_state(game_id, 'ACTIVE')
            GameStart.start(token)
            await GameLoop.start_loop(token)

            return True, True, ''
        else:
            return True, False, ''





