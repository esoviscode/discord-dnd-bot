import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_user')


def test_get_user_id_from_discord_id(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseGame.add_game('shhesh')
    um = {'id_game': id_game, 'discord_id': 78, 'discord_channel': 514}
    id_user = DatabaseUser.add_user(um['id_game'], um['discord_id'], um['discord_channel'])

    test_user_id = DatabaseUser.get_user_id_from_discord_id(um['discord_id'], um['id_game'])

    assert id_user == test_user_id


def test_get_user(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_game = DatabaseGame.add_game('shhesh')
    um = {'id_game': id_game, 'discord_id': 78, 'discord_channel': 514}
    id_user = DatabaseUser.add_user(um['id_game'], um['discord_id'], um['discord_channel'])

    db_d = DatabaseUser.get_user(id_user)

    for key, value in db_d.items():
        if key == 'id_user':
            assert value == id_user
        else:
            assert value == um[key]


