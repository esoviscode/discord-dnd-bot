import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_skill import DatabaseSkill
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_skill')


def test_add_skill(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_skill = DatabaseSkill.add_skill("test_skill")
    db_t = DatabaseConnection.get_object_from_db(f'SELECT * FROM public."Skill" WHERE id_skill = (%s)',(id_skill,),
                                                 "Skill")
    assert db_t[0] == id_skill
    assert db_t[1] == 'test_skill'


def test_get_skill(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_skill = DatabaseSkill.add_skill("test_skill")
    db_t = DatabaseSkill.get_skill(id_skill)
    assert db_t['id_skill'] == id_skill
    assert db_t['name'] == 'test_skill'


def test_add_entity_skill(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_entity = DatabaseConnection.add_to_db(f'INSERT INTO public."Entity" (name) VALUES (%s)', ("test_entity",), "Entity")
    id_skill = DatabaseSkill.add_skill('test_skill')
    DatabaseSkill.add_entity_skill(id_entity, id_skill)
    db_t = DatabaseConnection.get_object_from_db(f'SELECT * FROM public."Entity_Skill"')
    assert db_t[0] == id_entity
    assert db_t[1] == id_skill


def test_get_all_skills(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_skills = []
    for i in range(4):
        id_skills.append(DatabaseSkill.add_skill(f'test_skill{i}'))

    db_l = DatabaseSkill.get_all_skills()
    for i, element in enumerate(db_l):
        assert element['id_skill'] == id_skills[i]
        assert element['name'] == f'test_skill{i}'


def test_get_players_skills(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    id_entity = DatabaseConnection.add_to_db(f'INSERT INTO public."Entity" (name) VALUES (%s)', ('test_entity',), 'Entity')
    id_creature = DatabaseConnection.add_to_db(f'INSERT INTO public."Creature" (level, id_entity) VALUES (%s, %s)',
                                               (1, id_entity), 'Creature')
    id_player = DatabaseConnection.add_to_db(f'INSERT INTO public."Player" (backstory, id_creature) VALUES (%s, %s)',
                                             ('story', id_creature), 'Player')
    id_skills = []
    for i in range(4):
        id_skills.append(DatabaseSkill.add_skill(f'test_name{i}'))
        DatabaseSkill.add_entity_skill(id_entity, id_skills[i])

    db_l = DatabaseSkill.get_players_skills(id_player)
    for i, element in enumerate(db_l):
        assert element['id_skill'] == id_skills[i]
        assert element['name'] == f'test_name{i}'
