from sqlite3 import ProgrammingError
from typing import List

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseUser:

    @staticmethod
    def add_user(id_game: int, discord_id: int, discord_channel: int) -> int | None:
        """add user to a game
        :param id_game: database game id
        :param discord_id: user discord id
        :param discord_channel: user discord channel
        """
        return DatabaseConnection.add_to_db('INSERT INTO public."User" (id_game, discord_id, discord_channel) VALUES (%s, %s, %s)',
                                            (id_game, discord_id, discord_channel), "user")

    @staticmethod
    def get_user(id_user: int = 0) -> dict | None:
        query = f'SELECT id_game, discord_id, discord_channel FROM public."User" WHERE id_user = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_user,), "User")
        return {'id_user': id_user, 'id_game': db_t[0], 'discord_id': db_t[1], 'discord_channel': db_t[2]}

    @staticmethod
    def get_all_users(id_game: int = 0) -> List[dict] | None:
        query = f'SELECT * FROM public."User" WHERE id_game = (%s) ORDER BY id_user'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, (id_game,), "User")
        return [{'id_user': el[0], 'id_game': el[1], 'discord_id': el[2], 'discord_channel': el[3]} for el in db_l]

    @staticmethod
    def get_user_id_from_discord_id(discord_id: int = 0, id_game: int = 0) -> int | None:
        query = f'SELECT id_user FROM public."User" WHERE discord_id = (%s) AND id_game = (%s)'
        return DatabaseConnection.get_object_from_db(query, (discord_id, id_game), "User")[0]

    @staticmethod
    def delete_user(id_user: int = 0) -> None:
        query = 'DELETE FROM public."User" WHERE id_user = (%s)'
        parameters = (id_user,)
        return DatabaseConnection.update_object_in_db(query, parameters)
