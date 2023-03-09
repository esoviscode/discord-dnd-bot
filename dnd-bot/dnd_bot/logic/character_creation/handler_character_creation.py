from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.ui.views.view_character_creation import ViewCharacterCreationStart
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
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

            for user in game.user_list:
                ChosenAttributes.add_empty_user(user.discord_id)

            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: This game has already started!'

    @staticmethod
    async def assign_attribute_values(user_id):
        """Called to choose attribute values based on the user's choices in character creation process
            :param user_id: id of the user who finished character creation"""

        character = ChosenAttributes.chosen_attributes[user_id]
        # TODO assign attribute values based on class and race of the character with some random factor


