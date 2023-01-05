import os
from copy import deepcopy

from psycopg2 import connect, ProgrammingError


class DatabaseConnection:
    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        db_address, db_name, db_user, db_password, db_port = DatabaseConnection.__connection_get_authentication__()

        print(f'DB: attempting connection to {db_name} database at {db_address}:{db_port} {db_user}:{db_password}')

        DatabaseConnection.connection = connect(database=db_name, user=db_user, password=db_password,
                                                host=db_address, port=db_port)

        DatabaseConnection.cursor = DatabaseConnection.connection.cursor()
        print(f'DB: successfully connected')

    @staticmethod
    def __connection_get_authentication__():
        address = os.getenv('DB_ADDRESS')
        name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')

        if not user:
            user = 'admin'
        if not password:
            password = 'admin'
        if not port:
            port = 5432

        return address, name, user, password, port

    @staticmethod
    def connection_close():
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()

    @staticmethod
    def execute_query(query: str):
        DatabaseConnection.cursor.execute(query)
        DatabaseConnection.connection.commit()

    @staticmethod
    def add_game(token: str, id_host: int, id_campaign: int, game_state: str) -> int | None:

        DatabaseConnection.cursor.execute('INSERT INTO public."Game" (token, id_host, id_campaign, game_state) VALUES '
                                          '(%s, %s, %s, %s)',
                                          (token, id_host, id_campaign, game_state))
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')

        try:
            game_id = DatabaseConnection.cursor.fetchone()[0]
        except ProgrammingError as err:
            print(f"db: error adding game {err}")
            return None

        DatabaseConnection.connection.commit()
        return game_id

    @staticmethod
    def add_user(id_game: int, discord_id: int) -> int | None:

        DatabaseConnection.cursor.execute('INSERT INTO public."User" (id_game, discord_id) VALUES (%s, %s)',
                                          (id_game, discord_id))
        DatabaseConnection.cursor.execute('SELECT LASTVAL()')

        try:
            user_id = DatabaseConnection.cursor.fetchone()[0]
        except ProgrammingError as err:
            print(f"db: error adding user {err}")
            return None

        DatabaseConnection.connection.commit()
        return user_id

    @staticmethod
    def find_game_by_token(token: str) -> dict | None:

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."Game" WHERE token = %s AND game_state = %s',
                                          (token, 'LOBBY'))
        game_tuple = DatabaseConnection.cursor.fetchone()

        if not game_tuple:
            return None

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."User" WHERE id_game = {game_tuple[0]}')
        users_tuples = DatabaseConnection.cursor.fetchall()

        users = [{'id_user': user_tuple[0], 'id_game': user_tuple[1], 'discord_id': user_tuple[2]}
                 for user_tuple in users_tuples]

        return {'id_game': game_tuple[0], 'token': game_tuple[1], 'id_host': game_tuple[2],
                'id_campaign': game_tuple[3],
                'game_state': game_tuple[4], 'players': users}

    @staticmethod
    def update_game_state(id_game: int, game_state: str) -> None:
        DatabaseConnection.cursor.execute('UPDATE public."Game" SET game_state = %s WHERE id_game = %s',
                                          (game_state, id_game))

        DatabaseConnection.connection.commit()
