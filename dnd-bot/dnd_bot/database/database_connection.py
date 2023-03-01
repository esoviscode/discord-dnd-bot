import os
from sqlite3 import ProgrammingError

from psycopg2 import connect


class DatabaseConnection:
    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        """ establishes connection with the database using the provided ip address, credentials and port
        """
        db_address, db_name, db_user, db_passwords, db_port = DatabaseConnection.__connection_get_authentication__()

        print(f'db: attempting connection to {db_name} database at {db_address}:{db_port}')

        DatabaseConnection.connection = connect(database=db_name, user=db_user, password=db_passwords.pop(),
                                                host=db_address, port=db_port)

        # erase password in memory upon using it
        db_passwords.clear()

        DatabaseConnection.cursor = DatabaseConnection.connection.cursor()
        print(f'db: successfully connected')

    @staticmethod
    def __connection_get_authentication__():
        """extracts database credentials and others from environment variables passed to the app
        """
        passwords = []
        address = os.getenv('DB_ADDRESS')
        name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        passwords.append(os.getenv('DB_PASSWORD'))
        port = os.getenv('DB_PORT')

        if not user:
            user = 'admin'
        if passwords[0] is None:
            passwords.append('admin')
        if not port:
            port = 5432

        return address, name, user, passwords, port

    @staticmethod
    def connection_close():
        """closes connection to the database
        """
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()

    @staticmethod
    def execute_query(query: str):
        """deprecated - executes query as a string
        """
        DatabaseConnection.cursor.execute(query)
        DatabaseConnection.connection.commit()

    @staticmethod
    def add_user(id_game: int, discord_id: int) -> int | None:
        """add user to a game
        :param id_game: database game id
        :param discord_id: user discord id
        """

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
        """find game by token/password
        :param token: game token/password to find the game by
        :return: on success: dictionary containing game data - it's keys: 'id game' - database game id, 'token' - game token, 'id_host' -
        discord host id, 'id_campaign' - campaign id, 'game_state' - string enum, 'players' - list of players
        """

        DatabaseConnection.cursor.execute(f'SELECT * FROM public."Game" WHERE token = %s AND game_state != %s',
                                          (token, 'FINISHED'))
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
