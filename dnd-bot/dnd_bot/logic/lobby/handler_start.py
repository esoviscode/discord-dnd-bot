from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.database.database_connection import DatabaseConnection


class HandlerStart:

    def __init__(self):
        pass

    @staticmethod
    async def start_game(token, user_id) -> (bool, list, str):
        game = Multiverse.get_game(token)
        if game is None:
            return False, [], f':warning: Game of provided token doesn\'t exist!'

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if not game.all_users_ready():
            return False, [], f':warning: Not all the players are ready!'

        if game.game_state == 'LOBBY':
            game.game_state = "STARTING"
            game_id = DatabaseConnection.add_game(token, game.id_host, 0, "STARTING")

            if game_id is None:
                game.game_state = 'LOBBY'
                return False, [], ":warning: Error creating game!"
            for user in game.user_list:
                DatabaseConnection.add_user(game_id, user.discord_id)

            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: This game has already started!'
