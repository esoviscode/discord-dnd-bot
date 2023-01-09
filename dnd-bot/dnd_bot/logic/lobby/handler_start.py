from dnd_bot.database.database_connection import DatabaseConnection


class HandlerStart:

    def __init__(self):
        pass

    @staticmethod
    async def start_game(token, user_id) -> (bool, list, str):

        game_data = DatabaseConnection.find_game_by_token(token)
        if game_data is None:
            return False, [], f':no_entry: Game of provided token doesn\'t exist!'

        if user_id != game_data['id_host']:
            return False, [], f':warning: Only the host can start the game!'

        if game_data['game_state'] == 'LOBBY' or game_data['game_state'] == 'STARTING':
            DatabaseConnection.start_game(game_data['id_game'])

            users = [user['discord_id'] for user in game_data['players']]

            return True, users, ''
        else:
            return False, f':no_entry: The game has already started!'
