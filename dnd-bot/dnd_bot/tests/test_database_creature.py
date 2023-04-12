import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('creature')


def test_get_creature(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    cm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3, 'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR'}
    id_creature = DatabaseCreature.add_creature(x=cm['x'], y=cm['y'], name=cm['name'], hp=cm['hp'], strength=cm['strength'],
                                  dexterity=cm['dexterity'], intelligence=cm['intelligence'], charisma=cm['charisma'],
                                  perception=cm['perception'], initiative=cm['initiative'],
                                  action_points=cm['action_points'], level=cm['level'], money=cm['money'],
                                  id_game=cm['id_game'], experience=cm['experience'], id_equipment=cm['id_equipment'],
                                  creature_class=cm['class'], description=cm['description'])
    db_d = DatabaseCreature.get_creature(id_creature)
    for key, value in db_d.items():
        if key == 'id_creature':
            assert value == id_creature
        elif key == 'id_entity':
            continue
        else:
            assert value == cm[key]
