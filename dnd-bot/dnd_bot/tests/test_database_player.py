import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_player')


def test_get_player(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    pm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3,
          'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR', 'id_user': None,
          'alignment': "happy", 'backstory': "interesting backstory", 'race': 'ELF', 'max_hp': 9,
          'initial_action_points': 15}
    id_player = DatabasePlayer.add_player(x=pm['x'], y=pm['y'], name=pm['name'], hp=pm['hp'], strength=pm['strength'],
                                          dexterity=pm['dexterity'], intelligence=pm['intelligence'],
                                          charisma=pm['charisma'], perception=pm['perception'],
                                          initiative=pm['initiative'], action_points=pm['action_points'],
                                          level=pm['level'], money=pm['money'], id_game=pm['id_game'],
                                          experience=pm['experience'], id_equipment=pm['id_equipment'],
                                          character_class=pm['class'], description=pm['description'],
                                          discord_identity=None, alignment=pm['alignment'], backstory=pm['backstory'],
                                          character_race=pm['race'], max_hp=pm['max_hp'],
                                          initial_action_points=pm['initial_action_points'])
    db_d = DatabasePlayer.get_player(id_player)

    for key, value in db_d.items():
        if key == 'id_player':
            assert value == id_player
        elif key == 'id_entity' or key == 'id_creature':
            continue
        else:
            assert value == pm[key]
