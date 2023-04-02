import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_dialog import DatabaseDialog
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.tests.autoconf import database_fixture


def test_add_dialog():
    DatabaseConnection.connection_establish()
    id_entity = DatabaseEntity.add_entity('name')
    DatabaseDialog.add_dialog(id_entity, id_entity, "test content", 'AVAILABLE', 3)
    DatabaseConnection.connection_close()
    assert True


def test_get_dialog():
    DatabaseConnection.connection_establish()
    id_entity = DatabaseEntity.add_entity('name')
    id_dialog = DatabaseDialog.add_dialog(id_entity, id_entity, "test content", 'AVAILABLE', 3)
    test_dictionary = DatabaseDialog.get_dialog(id_dialog)

    assert test_dictionary['id_speaker'] == id_entity
    assert test_dictionary['id_listener'] == id_entity
    assert test_dictionary['content'] == "test content"
    assert test_dictionary['status'] == "AVAILABLE"
    assert test_dictionary['json_id'] == 3

    DatabaseConnection.connection_close()


def test_get_speakers_dialogs():
    DatabaseConnection.connection_establish()
    id_entity = DatabaseEntity.add_entity('name')
    id_dialog = DatabaseDialog.add_dialog(id_entity, id_entity, "test content", 'AVAILABLE', 3)
    id_dialog = DatabaseDialog.add_dialog(id_entity, id_entity, "test content 2", 'NOT_AVAILABLE', 2)
    test_list = DatabaseDialog.get_speakers_dialogs(id_entity)
    assert test_list[0]['id_speaker'] == id_entity and test_list[0]['id_listener'] == id_entity and \
           test_list[0]['content'] == "test content" and test_list[0]['status'] == "AVAILABLE" and\
           test_list[0]['json_id'] == 3
    assert test_list[1]['id_speaker'] == id_entity and test_list[1]['id_listener'] == id_entity and \
           test_list[1]['content'] == "test content 2" and test_list[1]['status'] == "NOT_AVAILABLE" and \
           test_list[1]['json_id'] == 2

    DatabaseConnection.connection_close()


def test_update_dialog():
    DatabaseConnection.connection_establish()
    id_entity = DatabaseEntity.add_entity('name')
    id_dialog = DatabaseDialog.add_dialog(id_entity, id_entity, "test content", 'AVAILABLE', 3)
    DatabaseDialog.update_dialog(id_dialog, "NOT_AVAILABLE")
    assert DatabaseDialog.get_dialog(id_dialog)['status'] == "NOT_AVAILABLE"
    DatabaseConnection.connection_close()