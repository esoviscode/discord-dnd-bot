import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_event import DatabaseEvent
from dnd_bot.logic.prototype.event import Event

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('event')


def test_add_event(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)


def test_get_event(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    id_event = DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)
    test_dictionary = DatabaseEvent.get_event(id_event)
    assert test_dictionary['status'] == 'AVAILABLE' and test_dictionary['json_id'] == 1


def test_update_event(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    id_event = DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)
    DatabaseEvent.update_event(id_event, 'NOT_AVAILABLE')
    test_dictionary = DatabaseEvent.get_event(id_event)
    assert test_dictionary['status'] == 'NOT_AVAILABLE' and test_dictionary['json_id'] == 1
