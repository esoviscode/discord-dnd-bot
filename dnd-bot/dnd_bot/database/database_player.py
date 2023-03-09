from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.player import Player


class DatabasePlayer:

    @staticmethod
    def add_player(p: Player) -> int | None:
        id_creature = DatabaseCreature.add_creature(p)
        id_user = DatabaseUser.get_user_id_from_discord_id(p.discord_identity, p.id_game)
        id_player = DatabaseConnection.add_to_db('INSERT INTO public."Player" (id_user, alignment, backstory, '
                                                 'id_creature) VALUES (%s, %s, %s, %s)',
                                                 (id_user, p.alignment, p.backstory, id_creature))
        p.id = id_player
        return id_player

    @staticmethod
    def get_player(id_player) -> dict | None:
        pass
