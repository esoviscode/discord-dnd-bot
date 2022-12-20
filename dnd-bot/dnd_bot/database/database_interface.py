import psycopg2
from database_connection import DatabaseConnection
from dnd_bot.database.database_enums import DatabaseEnums


class DatabaseInterface:





    @staticmethod
    def add_user(id_user: int, id_game: int, discord_id: int):
        cursor = DatabaseConnection.cursor

        cursor.execute('INSERT INTO User (id_user, id_game, discord_id) VALUES (%s, %s, %s)', id_user, id_game, discord_id)

        DatabaseConnection.connection.commit()