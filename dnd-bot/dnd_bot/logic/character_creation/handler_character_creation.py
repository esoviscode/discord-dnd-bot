import json
import random

from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.message_holder import MessageHolder
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.prototype.character_class import CharacterClass
from dnd_bot.logic.prototype.character_race import CharacterRace
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.utils import string_to_character_class, string_to_character_race


class HandlerCharacterCreation:
    """Handles character creation process"""

    CAMPAIGN_JSON_PATH = 'dnd_bot/assets/campaigns/campaign.json'

    classes: list[CharacterClass] = []
    races: list[CharacterRace] = []

    @staticmethod
    async def start_character_creation(token, user_id):
        """Called when host clicks start in lobby
            :param token: game token
            :param user_id: id of the user who ran the command or the host that pressed the start button
            :return: status, (if start was successful, users list, optional error message)
            """
        HandlerCharacterCreation.load_character_creation_json_data()

        game = Multiverse.get_game(token)
        game_id = DatabaseGame.get_id_game_from_game_token(token)

        if game_id is None:
            return False, [], ":no_entry: Error creating game!"

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if not game.all_users_ready():
            return False, [], f':warning: Not all the players are ready!'

        if game.game_state == 'LOBBY':
            game.game_state = "STARTING"
            DatabaseGame.update_game_state(game_id, 'STARTING')

            if game_id is None:
                game.game_state = 'LOBBY'
                return False, [], ":warning: Error creating game!"
            for user in game.user_list:
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
        character_class = string_to_character_class(character['class'])
        character_race = string_to_character_race(character['race'])

        points_to_distribute_randomly = 15

        additional_strength = random.randint(0, 2)
        strength = character_class.base_strength() + character_race.base_strength() + additional_strength
        points_to_distribute_randomly -= additional_strength
        ChosenAttributes.chosen_attributes[user_id]['strength'] = strength

        additional_dexterity = random.randint(0, 2)
        dexterity = character_class.base_dexterity() + character_race.base_dexterity() + additional_dexterity
        points_to_distribute_randomly -= additional_dexterity
        ChosenAttributes.chosen_attributes[user_id]['dexterity'] = dexterity

        additional_intelligence = random.randint(0, 2)
        intelligence = character_class.base_intelligence() + character_race.base_intelligence() + additional_intelligence
        points_to_distribute_randomly -= additional_intelligence
        ChosenAttributes.chosen_attributes[user_id]['intelligence'] = intelligence

        additional_charisma = random.randint(0, 2)
        charisma = character_class.base_charisma() + character_race.base_charisma() + additional_charisma
        points_to_distribute_randomly -= additional_charisma
        ChosenAttributes.chosen_attributes[user_id]['charisma'] = charisma

        additional_perception = random.randint(0, 1)
        perception = character_class.base_perception() + character_race.base_perception() + additional_perception
        points_to_distribute_randomly -= additional_perception
        ChosenAttributes.chosen_attributes[user_id]['perception'] = perception

        additional_action_points = random.randint(0, 2)
        action_points = character_class.base_action_points() + character_race.base_action_points() + additional_action_points
        points_to_distribute_randomly -= additional_action_points
        ChosenAttributes.chosen_attributes[user_id]['action points'] = action_points

        additional_initiative = random.randint(0, 2)
        initiative = character_class.base_initiative() + character_race.base_initiative() + additional_initiative
        points_to_distribute_randomly -= additional_initiative
        ChosenAttributes.chosen_attributes[user_id]['initiative'] = initiative

        ChosenAttributes.chosen_attributes[user_id]['hp'] = character_class.base_hp() + character_race.base_hp() + points_to_distribute_randomly

    @staticmethod
    async def handle_character_creation_finished(user_id, token) -> (bool, bool, str):
        """handles finishing of character creation process; if all the players finished it the game is started
                        :param user_id: id of the user who finished character creation process
                        :param token: game token
                        :return: status, status of other players (if all of them are ready) optional error message
                        """
        game = Multiverse.get_game(token)
        game_id = DatabaseGame.get_id_game_from_game_token(token)

        if game is None:
            return False, False, f':warning: Game of provided token doesn\'t exist!'

        game.find_user(user_id).is_ready = True

        if game.all_users_ready():
            game.game_state = 'ACTIVE'
            DatabaseGame.update_game_state(game_id, 'ACTIVE')

            # delete any error message from character creation
            for user in game.user_list:
                error_data = MessageHolder.read_last_error_data(user.discord_id)
                if error_data is not None:
                    MessageHolder.delete_last_error_data(user.discord_id)
                    await Messager.delete_message(error_data[0], error_data[1])

            GameStart.start(token)
            await GameLoop.start_loop(token)

            return True, True, ''
        else:
            return True, False, ''

    @staticmethod
    def load_character_creation_json_data():
        """
        function loads information about classes and races in a campaign from a json
        """
        with open(HandlerCharacterCreation.CAMPAIGN_JSON_PATH) as file:
            json_dict = json.load(file)
            for character_race_or_class in [(CharacterClass, 'classes'), (CharacterRace, 'races')]:
                json_races_or_classes = json_dict[character_race_or_class[1]]
                for json_class in json_races_or_classes:
                    character_class = character_race_or_class[0](name=json_class)
                    character_class.emoji = json_races_or_classes[json_class]['emoji']
                    character_class.description = json_races_or_classes[json_class]['description']
                    character_class.long_description = json_races_or_classes[json_class]['long-description']
                    stats = json_races_or_classes[json_class]['stats']

                    if 'action-points' in stats:
                        character_class.base_action_points = stats['action-points']
                    if 'initiative' in stats:
                        character_class.base_initiative = stats['initiative']
                    if 'hp' in stats:
                        character_class.base_hp = stats['hp']
                    if 'strength' in stats:
                        character_class.base_strength = stats['strength']
                    if 'dexterity' in stats:
                        character_class.base_dexterity = stats['dexterity']
                    if 'intelligence' in stats:
                        character_class.base_intelligence = stats['intelligence']
                    if 'charisma' in stats:
                        character_class.base_charisma = stats['charisma']
                    if 'perception' in stats:
                        character_class.base_perception = stats['perception']

                    if character_race_or_class[1] == 'classes':
                        HandlerCharacterCreation.classes.append(character_class)
                    if character_race_or_class[1] == 'races':
                        HandlerCharacterCreation.races.append(character_class)
