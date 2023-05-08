import json
import random

from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.prototype.character_class import CharacterClass
from dnd_bot.logic.prototype.character_race import CharacterRace
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import StartCharacterCreationException
from dnd_bot.logic.utils.utils import string_to_character_class, string_to_character_race, campaign_name_to_path


class HandlerCharacterCreation:
    """Handles character creation process"""

    campaigns: dict[str, dict[str, list[CharacterClass] | list[CharacterRace]]] = {}

    @staticmethod
    async def start_character_creation(token, user_id):
        """Called when host clicks start in lobby
            :param token: game token
            :param user_id: id of the user who ran the command or the host that pressed the start button
            :return: user list
            """
        game = Multiverse.get_game(token)
        game_id = DatabaseGame.get_id_game_from_game_token(token)

        if game.campaign_name not in HandlerCharacterCreation.campaigns:
            HandlerCharacterCreation.load_character_creation_json_data(game.campaign_name)

        if game_id is None:
            raise StartCharacterCreationException(":no_entry: Error creating game!")

        if user_id != game.id_host:
            raise StartCharacterCreationException(":warning: Only the host can start the game!")

        if not game.all_users_ready():
            raise StartCharacterCreationException(":warning: Not all the players are ready!")

        if game.game_state != 'LOBBY':
            raise StartCharacterCreationException(":no_entry: This game has already started!")

        game.game_state = 'STARTING'
        DatabaseGame.update_game_state(game_id, 'STARTING')

        for user in game.user_list:
            ChosenAttributes.add_empty_user(user.discord_id, token)
            game.find_user(user.discord_id).is_ready = False

        return game.user_list

    @staticmethod
    async def assign_attribute_values(token, user_id):
        """Called to choose attribute values based on the user's choices in character creation process
            :param token: game token
            :param user_id: id of the user who finished character creation"""

        character = ChosenAttributes.chosen_attributes[(user_id, token)]
        character_class = string_to_character_class(character['class'], token)
        character_race = string_to_character_race(character['race'], token)

        points_to_distribute_randomly = 15

        additional_strength = random.randint(0, 2)
        strength = character_class.base_strength + character_race.base_strength + additional_strength
        points_to_distribute_randomly -= additional_strength
        ChosenAttributes.chosen_attributes[(user_id, token)]['strength'] = strength

        additional_dexterity = random.randint(0, 2)
        dexterity = character_class.base_dexterity + character_race.base_dexterity + additional_dexterity
        points_to_distribute_randomly -= additional_dexterity
        ChosenAttributes.chosen_attributes[(user_id, token)]['dexterity'] = dexterity

        additional_intelligence = random.randint(0, 2)
        intelligence = character_class.base_intelligence + character_race.base_intelligence + additional_intelligence
        points_to_distribute_randomly -= additional_intelligence
        ChosenAttributes.chosen_attributes[(user_id, token)]['intelligence'] = intelligence

        additional_charisma = random.randint(0, 2)
        charisma = character_class.base_charisma + character_race.base_charisma + additional_charisma
        points_to_distribute_randomly -= additional_charisma
        ChosenAttributes.chosen_attributes[(user_id, token)]['charisma'] = charisma

        additional_perception = random.randint(0, 1)
        perception = character_class.base_perception + character_race.base_perception + additional_perception
        points_to_distribute_randomly -= additional_perception
        ChosenAttributes.chosen_attributes[(user_id, token)]['perception'] = perception

        additional_action_points = random.randint(0, 2)
        action_points = character_class.base_action_points + character_race.base_action_points + additional_action_points
        points_to_distribute_randomly -= additional_action_points
        ChosenAttributes.chosen_attributes[(user_id, token)]['action points'] = action_points

        additional_initiative = random.randint(0, 2)
        initiative = character_class.base_initiative + character_race.base_initiative + additional_initiative
        points_to_distribute_randomly -= additional_initiative
        ChosenAttributes.chosen_attributes[(user_id, token)]['initiative'] = initiative

        ChosenAttributes.chosen_attributes[(user_id, token)]['hp'] = character_class.base_hp + character_race.base_hp + points_to_distribute_randomly

    @staticmethod
    def load_character_creation_json_data(campaign_name: str = ""):
        """
        function loads information about classes and races in a campaign from a json
        """

        HandlerCharacterCreation.campaigns[campaign_name] = {"classes": [], "races": []}

        with open(campaign_name_to_path(campaign_name)) as file:
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
                        HandlerCharacterCreation.campaigns[campaign_name]["classes"].append(character_class)
                    if character_race_or_class[1] == 'races':
                        HandlerCharacterCreation.campaigns[campaign_name]["races"].append(character_class)
