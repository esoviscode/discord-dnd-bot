from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_player import DatabasePlayer

from dnd_bot.logic.prototype.player import Player

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('player')


def test_add_player(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    p = Player(x=1, y=2, name='silentsky', hp=3, strength=4, dexterity=5, intelligence=6, charisma=7, perception=8,
               initiative=9, action_points=10, level=11, alignment='align', backstory='back',
               character_class='MAGE', character_race='HUMAN')

    game_id = DatabaseGame.get_id_game_from_game_token('12345')
    id_player = DatabasePlayer.add_player(x=p.x, y=p.y, name=p.name, hp=p.hp, strength=p.base_strength,
                                          dexterity=p.base_dexterity, intelligence=p.base_intelligence,
                                          charisma=p.base_charisma, perception=p.base_perception,
                                          initiative=p.initiative, action_points=p.action_points,
                                          level=p.level, discord_identity=p.discord_identity, alignment=p.alignment,
                                          backstory=p.backstory, id_game=game_id,
                                          character_race=p.character_race, character_class=p.creature_class,
                                          max_hp=p.max_hp, initial_action_points=p.initial_action_points)

    player_tuple = cur.execute(f'SELECT * FROM public."Player" WHERE id_player = (SELECT LASTVAL())').fetchone()
    creature_tuple = cur.execute(f'SELECT * FROM public."Creature" WHERE id_creature = (SELECT LASTVAL())').fetchone()
    entity_tuple = cur.execute(f'SELECT * FROM public."Entity" WHERE id_entity = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert entity_tuple[1] == 'silentsky'
    assert entity_tuple[2] == 1
    assert entity_tuple[3] == 2
    assert creature_tuple[1] == 11
    assert creature_tuple[2] == 3
    assert creature_tuple[3] == 4

    assert player_tuple[2] == p.alignment
    assert player_tuple[3] == p.backstory
    assert player_tuple[5] == p.character_race
    assert creature_tuple[14] == p.creature_class
