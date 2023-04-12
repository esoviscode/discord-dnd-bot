import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('item')


def test_get_item(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_item = DatabaseItem.add_item('test_item')
    db_d = DatabaseItem.get_item(id_item)
    assert db_d['id_item'] == id_item
    assert db_d['name'] == 'test_item'


def test_get_all_items(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    id_items = []
    for i in range(4):
        id_items.append(DatabaseItem.add_item(f'test_item{i}'))

    db_l = DatabaseItem.get_all_items()
    for i, item in enumerate(db_l):
        assert item['id_item'] == id_items[i]
        assert item['name'] == f'test_item{i}'
