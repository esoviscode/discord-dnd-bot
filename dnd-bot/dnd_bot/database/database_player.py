from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_user import DatabaseUser


class DatabasePlayer:

    @staticmethod
    def add_player(x: int = 0, y: int = 0, name: str = 'Creature', hp: int = 0, strength: int = 0,
                   dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0,
                   initiative: int = 0, action_points: int = 0, level: int = 0, discord_identity: int = 0,
                   alignment: str = '', backstory: str = '', id_game: int = None, experience: int = 0,
                   character_class: str = None, character_race: str = None, id_equipment: int = None, money: int = 0,
                   description: str = "", max_hp: int = 0, initial_action_points: int = 0) -> int | None:
        id_creature = DatabaseCreature.add_creature(x=x, y=y, name=name, hp=hp, strength=strength,
                                                    dexterity=dexterity, intelligence=intelligence, charisma=charisma,
                                                    perception=perception, initiative=initiative,
                                                    action_points=action_points, level=level, id_game=id_game,
                                                    experience=experience, id_equipment=id_equipment,
                                                    creature_class=character_class, money=money, description=description,
                                                    max_hp=max_hp, initial_action_points=initial_action_points)
        id_user = None
        if discord_identity:
            id_user = DatabaseUser.get_user_id_from_discord_id(discord_identity, id_game)
        if character_race:
            character_race = character_race.upper()
        id_player = DatabaseConnection.add_to_db('INSERT INTO public."Player" (id_user, alignment, backstory, '
                                                 'race,id_creature) VALUES (%s, %s, %s, %s, %s)',
                                                 (id_user, alignment, backstory, character_race, id_creature),
                                                 "Player")
        return id_player

    @staticmethod
    def update_player(id_player: int = 0,hp: int = 0, level: int = 0, money: int = 0, experience: int = 0, x: int = 0,
                      y: int = 0) -> None:
        id_creature = DatabasePlayer.get_players_id_creature(id_player)
        DatabaseCreature.update_creature(id_creature=id_creature, level=level, money=money, experience=experience, x=x,
                                         y=y, hp=hp)

    @staticmethod
    def get_player(id_player) -> dict | None:
        query = f'SELECT * FROM public."Player" WHERE id_player = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_player,), "Player")
        player = {'id_player': db_t[0], 'id_user': db_t[1], 'alignment': db_t[2], 'backstory': db_t[3],
                  'id_creature': db_t[4], 'race': db_t[5]}
        db_d = DatabaseCreature.get_creature(player['id_creature'])
        for key, value in db_d.items():
            player[key] = value

        return player

    @staticmethod
    def get_players_id_entity(id_player: int = 0) -> int:
        id_creature = DatabasePlayer.get_players_id_creature(id_player=id_player)

        return DatabaseConnection.get_object_from_db(
            'SELECT id_entity FROM public."Creature" WHERE id_creature = (%s)',
            (id_creature,), "Creature")[0]

    @staticmethod
    def get_players_id_creature(id_player: int = 0) -> int:
        return DatabaseConnection.get_object_from_db('SELECT id_creature FROM public."Player" WHERE '
                                                     'id_player = (%s)', (id_player,), "Player")[0]
