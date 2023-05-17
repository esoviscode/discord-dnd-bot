import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_creature')


def test_add_creature(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    cm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3,
          'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR', 'max_hp': 4,
          'initial_action_points': 11}
    id_creature = DatabaseCreature.add_creature(x=cm['x'], y=cm['y'], name=cm['name'], hp=cm['hp'],
                                                strength=cm['strength'],
                                                dexterity=cm['dexterity'], intelligence=cm['intelligence'],
                                                charisma=cm['charisma'],
                                                perception=cm['perception'], initiative=cm['initiative'],
                                                action_points=cm['action_points'], level=cm['level'], money=cm['money'],
                                                id_game=cm['id_game'], experience=cm['experience'],
                                                id_equipment=cm['id_equipment'],
                                                creature_class=cm['class'], description=cm['description'],
                                                max_hp=cm['max_hp'], initial_action_points=cm['initial_action_points'])

    db_d = cur.execute(f'SELECT * FROM public."Creature" WHERE id_creature = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert id_creature == 1
    assert db_d[0] == 1
    assert db_d[1] == 3
    assert db_d[2] == 4
    assert db_d[3] == 5
    assert db_d[4] == 6
    assert db_d[5] == 7
    assert db_d[6] == 8
    assert db_d[7] == 9
    assert db_d[8] == 10
    assert db_d[9] == 11
    assert db_d[10] == 12
    assert db_d[11] == 1  # id_entity
    assert db_d[12] == 13
    assert db_d[13] is None
    assert db_d[14] == 'WARRIOR'
    assert db_d[15] == 4
    assert db_d[16] == 11


def test_update_creature(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    cm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3,
          'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR', 'max_hp': 9,
          'initial_action_points': 15}
    id_creature = DatabaseCreature.add_creature(x=cm['x'], y=cm['y'], name=cm['name'], hp=cm['hp'],
                                                strength=cm['strength'],
                                                dexterity=cm['dexterity'], intelligence=cm['intelligence'],
                                                charisma=cm['charisma'],
                                                perception=cm['perception'], initiative=cm['initiative'],
                                                action_points=cm['action_points'], level=cm['level'], money=cm['money'],
                                                id_game=cm['id_game'], experience=cm['experience'],
                                                id_equipment=cm['id_equipment'],
                                                creature_class=cm['class'], description=cm['description'],
                                                max_hp=cm['max_hp'], initial_action_points=cm['initial_action_points'])

    DatabaseCreature.update_creature(id_creature=id_creature, hp=100, level=101, money=102, experience=103, x=104,
                                     y=105)

    db_d = cur.execute(f'SELECT * FROM public."Creature" WHERE id_creature = (SELECT LASTVAL())').fetchone()
    postgresql.commit()

    assert db_d[0] == id_creature
    assert db_d[1] == 101
    assert db_d[2] == 100
    assert db_d[3] == 5
    assert db_d[4] == 6
    assert db_d[5] == 7
    assert db_d[6] == 8
    assert db_d[7] == 9
    assert db_d[8] == 10
    assert db_d[9] == 11
    assert db_d[10] == 102
    assert db_d[11] == 1  # id_entity
    assert db_d[12] == 103
    assert db_d[13] is None
    assert db_d[14] == 'WARRIOR'
    assert db_d[15] == 9
    assert db_d[16] == 15


def test_get_creature(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    cm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3,
          'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR', 'max_hp': 9,
          'initial_action_points': 15}
    id_creature = DatabaseCreature.add_creature(x=cm['x'], y=cm['y'], name=cm['name'], hp=cm['hp'],
                                                strength=cm['strength'],
                                                dexterity=cm['dexterity'], intelligence=cm['intelligence'],
                                                charisma=cm['charisma'],
                                                perception=cm['perception'], initiative=cm['initiative'],
                                                action_points=cm['action_points'], level=cm['level'], money=cm['money'],
                                                id_game=cm['id_game'], experience=cm['experience'],
                                                id_equipment=cm['id_equipment'],
                                                creature_class=cm['class'], description=cm['description'],
                                                max_hp=cm['max_hp'], initial_action_points=cm['initial_action_points'])
    db_d = DatabaseCreature.get_creature(id_creature)
    for key, value in db_d.items():
        if key == 'id_creature':
            assert value == id_creature
        elif key == 'id_entity':
            continue
        else:
            assert value == cm[key]


def test_get_creature_id_entity(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    cm = {'name': 'test_name', 'x': 1, 'y': 2, 'id_game': None, 'description': 'tested_description', 'level': 3,
          'hp': 4,
          'strength': 5, 'dexterity': 6, 'intelligence': 7, 'charisma': 8, 'perception': 9, 'initiative': 10,
          'action_points': 11, 'money': 12, 'experience': 13, 'id_equipment': None, 'class': 'WARRIOR', 'max_hp': 9,
          'initial_action_points': 15}
    id_creature = DatabaseCreature.add_creature(x=cm['x'], y=cm['y'], name=cm['name'], hp=cm['hp'],
                                                strength=cm['strength'],
                                                dexterity=cm['dexterity'], intelligence=cm['intelligence'],
                                                charisma=cm['charisma'],
                                                perception=cm['perception'], initiative=cm['initiative'],
                                                action_points=cm['action_points'], level=cm['level'], money=cm['money'],
                                                id_game=cm['id_game'], experience=cm['experience'],
                                                id_equipment=cm['id_equipment'],
                                                creature_class=cm['class'], description=cm['description'],
                                                max_hp=cm['max_hp'], initial_action_points=cm['initial_action_points'])

    id_entity = DatabaseCreature.get_creature_id_entity(id_creature=id_creature)

    assert id_creature == 1
    assert id_entity == 1



