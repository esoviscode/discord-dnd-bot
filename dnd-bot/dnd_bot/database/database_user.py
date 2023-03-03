from sqlite3 import ProgrammingError

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseUser:

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
    def get_user(discord_id: int = 0) -> dict | None:
        pass
