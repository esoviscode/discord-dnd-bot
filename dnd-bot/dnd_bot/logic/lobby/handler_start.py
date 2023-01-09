from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.database.database_connection import DatabaseConnection


class HandlerStart:

    def __init__(self):
        pass

    @staticmethod
    async def start_game(token, user_id) -> (bool, list, str):
        game = Multiverse.get_game(token)
        game_id = DatabaseConnection.add_game(token, game.id_host, 0, "LOBBY")

        if game_id is None:
            return False, [], ":no_entry: Error creating game!"
        for user in game.user_list:
            DatabaseConnection.add_user(game_id, user.discord_id)

        if game is None:
            return False, [], f':no_entry: Game of provided token doesn\'t exist!'

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if game.game_state == 'LOBBY' or game.game_state == 'STARTING':
            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: The game has already started!'
