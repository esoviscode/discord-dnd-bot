from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_player import DatabasePlayer

from dnd_bot.logic.prototype.player import Player

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('player')


def test_add_player(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    player = Player(x=1, y=2, name='silentsky', hp=3, strength=4, dexterity=5, intelligence=6, charisma=7, perception=8,
                    initiative=9, action_points=10, level=11, discord_identity=12, alignment='align', backstory='back',
                    game_token='12345')
    DatabasePlayer.add_player(player)

    player_tuple = cur.execute(f'SELECT * FROM public."Player" WHERE id_player = (SELECT LASTVAL())').fetchone()
    creature_tuple = cur.execute(f'SELECT * FROM public."Creature" WHERE id_creature = (SELECT LASTVAL())').fetchone()
    entity_tuple = cur.execute(f'SELECT * FROM public."Entity" WHERE id_entity = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert (entity_tuple[1] == 'silentsky')
    assert (entity_tuple[2] == 1)
    assert (entity_tuple[3] == 2)
    assert (creature_tuple[1] == 11)
    assert (creature_tuple[2] == 3)
    assert (creature_tuple[3] == 4)

