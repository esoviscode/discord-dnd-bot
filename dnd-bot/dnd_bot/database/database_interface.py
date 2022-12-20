import psycopg2
from database_connection import DatabaseConnection


class DbInterface:

    @staticmethod
    def add_game(password, id_host, id_campaign, game_state):
        cursor = DatabaseConnection.cursor

        cursor.execute('INSERT INTO Game (password, id_host, id_campaign, game_state) VALUES (%s, %s, %s, %s)',
                       password, id_host, id_campaign, game_state)

        DatabaseConnection.connection.commit()
