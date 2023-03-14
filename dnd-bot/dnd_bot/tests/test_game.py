import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_game import DatabaseGame

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('game')


def test_add_game(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    DatabaseConnection.add_to_db('INSERT INTO public."Game" (token, id_host, game_state, campaign_name)'
                                 ' VALUES (%s, %s, %s, %s)', ('12345', 1, 'LOBBY', 'test'))

    game_tuple = cur.execute(f'SELECT * FROM public."Game" WHERE id_game = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert (game_tuple[1] == '12345')  # token
    assert (game_tuple[2] == 1)  # id_host
    assert (game_tuple[3] == 'LOBBY')
    assert (game_tuple[4] == 'test')

    cur.close()


def test_add_game_no_token(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    DatabaseConnection.add_to_db('INSERT INTO public."Game" (id_host, game_state, campaign_name)'
                                 ' VALUES (%s, %s, %s)', (1, 'LOBBY', 'test'))

    game_tuple = cur.execute(f'SELECT * FROM public."Game" WHERE id_game = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert (game_tuple[1] is None)  # token
    assert (game_tuple[2] == 1)  # id_host
    assert (game_tuple[3] == 'LOBBY')
    assert (game_tuple[4] == 'test')


def test_add_game_no_game_state(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    DatabaseConnection.add_to_db('INSERT INTO public."Game" (token, id_host, campaign_name)'
                                 ' VALUES (%s, %s, %s)', ('12345', 1, 'test'))

    game_tuple = cur.execute(f'SELECT * FROM public."Game" WHERE id_game = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert (game_tuple[1] == '12345')
    assert (game_tuple[2] == 1)
    assert (game_tuple[3] is None)
    assert (game_tuple[4] == 'test')


#
# get_id_game_from_game_token
#
def test_get_id_game_from_game_token_exists(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseGame.get_id_game_from_game_token('12345')

    assert (id_game == 1)


def test_get_id_game_from_game_token_doesnt_exist(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseGame.get_id_game_from_game_token('00000')

    assert (id_game is None)


def test_get_id_game_from_game_token_negative(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    try:
        id_game = DatabaseGame.get_id_game_from_game_token('00000')
    except ValueError:
        pytest.fail('test_get_id_game_from_game_token_negative failed')

    assert id_game is None


#
# get_game_token_from_id_game
#
def test_get_game_token_from_id_game_exists(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    game_token = DatabaseGame.get_game_token_from_id_game(1)

    assert game_token == '12345'
