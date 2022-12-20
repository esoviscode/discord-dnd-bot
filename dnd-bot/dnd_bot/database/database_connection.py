from copy import deepcopy

from psycopg2 import connect

from dnd_bot.database.database_enums import DatabaseEnums


class DatabaseConnection:

    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        db_name = 'discord_bot'
        db_user = 'admin'
        db_password = 'admin'

        DatabaseConnection.connection = connect(database=db_name, user=db_user, password=db_password, host='25.74.173.113')

        DatabaseConnection.cursor = DatabaseConnection.connection.cursor()

    @staticmethod
    def connection_close():
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()

    @staticmethod
    def execute_query(query: str):
        DatabaseConnection.cursor.execute(query)
        DatabaseConnection.connection.commit()

    @staticmethod
    def add_game(token: str, id_host: int, id_campaign: int, game_state: str) -> int:

        DatabaseConnection.cursor.execute('INSERT INTO public."Game" (token, id_host, id_campaign, game_state) VALUES '
                                          '(%s, %s, %s, %s)',
                                          (token, id_host, id_campaign, game_state))
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')
        game_id = DatabaseConnection.cursor.fetchone()[0]
        DatabaseConnection.connection.commit()
        return game_id

    @staticmethod
    def add_user(id_game: int, discord_id: int) -> int:

        DatabaseConnection.cursor.execute('INSERT INTO public."User" (id_game, discord_id) VALUES (%s, %s)', (id_game, discord_id))
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')
        user_id = DatabaseConnection.cursor.fetchone()[0]
        DatabaseConnection.connection.commit()
        return user_id

    @staticmethod
    def find_game_by_token(token: str) -> dict:

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."Game" WHERE token = %s AND game_state = %s', (token, 'LOBBY'))
        game_tuple = DatabaseConnection.cursor.fetchone()

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."User" WHERE id_game = {game_tuple[0]}')
        users_tuples = DatabaseConnection.cursor.fetchall()

        users = [{'id_user': user_tuple[0], 'id_game': user_tuple[1], 'discord_id': user_tuple[2]}
                      for user_tuple in users_tuples]

        return {'id_game': game_tuple[0], 'token': game_tuple[1], 'id_host': game_tuple[2], 'id_campaign': game_tuple[3],
                'game_state': game_tuple[4], 'players': users}


