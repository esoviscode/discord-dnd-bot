import pytest
from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('dialog')


# def test_add_entity(postgresql):
#     pass


def test_get_entity(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseConnection.add_to_db(f'INSERT INTO public."Game" (token) VALUES (1)',None,"element")
    id_entity = DatabaseEntity.add_entity("test_entity", x=1, y=2, id_game= id_game, description="test_description")
    db_d = DatabaseEntity.get_entity(id_entity)
    assert db_d['name'] == "test_entity"
    assert db_d['x'] == 1
    assert db_d['y'] == 2
    assert db_d['description'] == "test_description"
    assert db_d['id_game'] == id_game
