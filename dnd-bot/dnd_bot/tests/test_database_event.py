import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_event import DatabaseEvent
from dnd_bot.logic.prototype.event import Event

def test_add_event():
    DatabaseConnection.connection_establish()
    DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)
    DatabaseConnection.connection_close()


def test_get_event():
    DatabaseConnection.connection_establish()
    id_event = DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)
    test_dictionary = DatabaseEvent.get_event(id_event)
    assert test_dictionary['status'] == 'AVAILABLE' and test_dictionary['json_id'] == 1
    DatabaseConnection.connection_close()


def test_update_event():
    DatabaseConnection.connection_establish()
    id_event = DatabaseEvent.add_event(status='AVAILABLE', id_game=None, json_id=1)
    DatabaseEvent.update_event(id_event, 'NOT_AVAILABLE')
    test_dictionary = DatabaseEvent.get_event(id_event)
    assert test_dictionary['status'] == 'NOT_AVAILABLE' and test_dictionary['json_id'] == 1
    DatabaseConnection.connection_close()



