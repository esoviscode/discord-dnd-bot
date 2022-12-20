from copy import deepcopy

from psycopg2 import connect

from dnd_bot.database.database_enums import DatabaseEnums


class DatabaseConnection:

    connection = None
    cursor = None

    @staticmethod
    def connection_establish():
        db_name = 'postgres'
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
    def add_game(password: str, id_host: int, id_campaign: int, game_state: str):

        id_game = 2

        DatabaseConnection.cursor.execute('INSERT INTO public."Game" (id_game, password, id_host, id_campaign, game_state) VALUES (%s, %s, %s, %s, %s)',
                                          (id_game, password, id_host, id_campaign, game_state))
        DatabaseConnection.connection.commit()
