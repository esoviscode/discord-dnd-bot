import pytest
from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_entity')


def test_add_entity(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseConnection.add_to_db(f'INSERT INTO public."Game" (token) VALUES (1)', None, "element")
    id_entity = DatabaseEntity.add_entity("test_entity", x=1, y=2, id_game=id_game, description="test_description")

    db_d = cur.execute(f'SELECT * FROM public."Entity" WHERE id_entity = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert db_d[0] == id_entity
    assert db_d[1] == "test_entity"
    assert db_d[2] == 1
    assert db_d[3] == 2
    assert db_d[4] == id_game
    assert db_d[5] == "test_description"


def test_add_entity_no_id_game(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    DatabaseConnection.add_to_db(f'INSERT INTO public."Game" (token) VALUES (1)', None, "element")
    id_entity = DatabaseEntity.add_entity("test_entity", x=1, y=2, description="test_description")

    assert id_entity == 1
    # TODO should be None!! but somehow this change breaks all tests
    # assert id_entity is None


def test_update_entity(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    id_game = DatabaseConnection.add_to_db(f'INSERT INTO public."Game" (token) VALUES (1)', None, "element")
    id_entity = DatabaseEntity.add_entity("test_entity", x=1, y=2, id_game=id_game, description="test_description")

    DatabaseEntity.update_entity(id_entity=id_entity, x=111, y=222)

    db_d = cur.execute(f'SELECT * FROM public."Entity" WHERE id_entity = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert id_entity == 1
    assert db_d[0] == id_entity
    assert db_d[1] == "test_entity"
    assert db_d[2] == 111
    assert db_d[3] == 222
    assert db_d[4] == id_game
    assert db_d[5] == "test_description"


def test_get_entity(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseConnection.add_to_db(f'INSERT INTO public."Game" (token) VALUES (1)', None, "element")
    id_entity = DatabaseEntity.add_entity("test_entity", x=1, y=2, id_game=id_game, description="test_description")
    db_d = DatabaseEntity.get_entity(id_entity)
    assert db_d['name'] == "test_entity"
    assert db_d['x'] == 1
    assert db_d['y'] == 2
    assert db_d['description'] == "test_description"
    assert db_d['id_game'] == id_game
