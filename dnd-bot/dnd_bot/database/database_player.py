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
    def get_player(id_player) -> Player | None:
        player_tuple = DatabaseConnection.get_object_from_db('SELECT * FROM public."Player" WHERE id_player = (%s)',
                                                             (id_player))

        creature_tuple = DatabaseConnection.get_object_from_db('SELECT * FROM public."Creature" WHERE id_creature = (%s)',
                                                               (player_tuple[5]))

        entity_tuple = DatabaseConnection.get_object_from_db('SELECT * FROM public."Entity" WHERE id_entity = (%s)',
                                                             (creature_tuple[11]))

        if entity_tuple is None:
            return None

        player = Player(entity_id=entity_tuple[0], x=entity_tuple[2], y=entity_tuple[3], name=entity_tuple[1],
                        hp=creature_tuple[2], level=creature_tuple[1], strength=creature_tuple[3],
                        dexterity=creature_tuple[4], intelligence=creature_tuple[5], charisma=creature_tuple[6],
                        perception=creature_tuple[7], initiative=creature_tuple[8], action_points=creature_tuple[9],
                        discord_identity=player_tuple[1], alignment=player_tuple[2], backstory=player_tuple[3])

        player.id = player_tuple[0]

        return player



