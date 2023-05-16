import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_game')


def test_get_game(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    gm = {'token': 'game_token', 'id_host': None, 'game_state': 'ACTIVE', 'campaign_name': "Sheeesh game"}

    id_game = DatabaseGame.add_game(token=gm['token'], id_host=gm['id_host'], game_state=gm['game_state'],
                                    campaign_name=gm['campaign_name'])
    db_d = DatabaseGame.get_game(id_game)
    for key, value in db_d.items():
        if key == 'id_game':
            assert value == id_game
        else:
            assert value == gm[key]
