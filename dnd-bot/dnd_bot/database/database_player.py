from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.player import Player


class DatabasePlayer:

    @staticmethod
    def add_player(x: int = 0, y: int = 0, name: str = 'Creature', hp: int = 0, strength: int = 0,
                   dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0,
                   initiative: int = 0, action_points: int = 0, level: int = 0, discord_identity: int = 0,
                   alignment: str = '', backstory: str = '', id_game: int = 1, experience: int = 0,
                   character_class: str = '', character_race: str = '', id_equipment: int = 0) -> int | None:
        id_creature = DatabaseCreature.add_creature(x=x, y=y, name=name, hp=hp, strength=strength,
                                                    dexterity=dexterity, intelligence=intelligence, charisma=charisma,
                                                    perception=perception, initiative=initiative,
                                                    action_points=action_points, level=level, id_game=id_game,
                                                    experience=experience)
        id_user = DatabaseUser.get_user_id_from_discord_id(discord_identity, id_game)
        id_player = DatabaseConnection.add_to_db('INSERT INTO public."Player" (id_user, alignment, backstory, '
                                                 'race, class, id_equipment,id_creature) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                                 (id_user, alignment, backstory,
                                                  character_race.upper(), character_class.upper(), id_equipment,
                                                  id_creature), "Player")
        return id_player

    @staticmethod
    def update_player(id_player: int = 0,hp: int = 0, level: int = 0, money: int = 0, experience: int = 0, x: int = 0,
                      y: int = 0) -> None:
        id_creature = DatabasePlayer.get_players_id_creature(id_player)
        DatabaseCreature.update_creature(id_creature=id_creature, level=level, money=money, experience=experience, x=x,
                                         y=y, hp=hp)

    @staticmethod
    def get_player(id_player) -> Player | None:
        player_tuple = DatabaseConnection.get_object_from_db('SELECT * FROM public."Player" WHERE id_player = (%s)',
                                                             (id_player))

        creature_tuple = DatabaseConnection.get_object_from_db(
            'SELECT * FROM public."Creature" WHERE id_creature = (%s)',
            (player_tuple[5]))

        entity_tuple = DatabaseConnection.get_object_from_db('SELECT * FROM public."Entity" WHERE id_entity = (%s)',
                                                             (creature_tuple[11]))

        if entity_tuple is None:
            return None

        player = Player(entity_id=entity_tuple[0], x=entity_tuple[2], y=entity_tuple[3], name=entity_tuple[1],
                        hp=creature_tuple[2], level=creature_tuple[1], strength=creature_tuple[3],
                        dexterity=creature_tuple[4], intelligence=creature_tuple[5], charisma=creature_tuple[6],
                        perception=creature_tuple[7], initiative=creature_tuple[8], action_points=creature_tuple[9],
                        discord_identity=player_tuple[1], alignment=player_tuple[2], backstory=player_tuple[3],
                        experience=creature_tuple[12])

        player.id = player_tuple[0]

        return player

    @staticmethod
    def get_players_id_entity(id_player: int = 0) -> int:
        id_creature = DatabasePlayer.get_players_id_creature(id_player=id_player)

        return DatabaseConnection.get_object_from_db(
            'SELECT id_entity FROM public."Creature" WHERE id_creature = (%s)',
            (id_creature,))

    @staticmethod
    def get_players_id_creature(id_player: int = 0) -> int:
        return DatabaseConnection.get_object_from_db('SELECT id_creature FROM public."Player" WHERE '
                                                     'id_player = (%s)', (id_player,), "Player")
