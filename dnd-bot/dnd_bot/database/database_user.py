from sqlite3 import ProgrammingError

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseUser:

    @staticmethod
    def add_user(id_game: int, discord_id: int) -> int | None:
        """add user to a game
        :param id_game: database game id
        :param discord_id: user discord id
        """
        return DatabaseConnection.add_to_db('INSERT INTO public."User" (id_game, discord_id) VALUES (%s, %s)',
                                            (id_game, discord_id), "user")

    @staticmethod
    def get_user(discord_id: int = 0) -> dict | None:
        pass

    @staticmethod
    def get_user_id_from_discord_id(discord_id: int = 0, id_game: int = 0) -> int | None:
        query = f'SELECT id_user FROM public."User" WHERE discord_id = (%s) AND id_game = (%s)'
        return DatabaseConnection.get_object_from_db(query, (discord_id, id_game), "User")[0]

