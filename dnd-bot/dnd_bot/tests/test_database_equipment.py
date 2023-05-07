import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_equipment import DatabaseEquipment
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_equipment')


def test_get_equipment(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    im_name = []
    im_id = []
    for i in range(5):
        im_name.append(f'test_item_{i}')
        im_id.append(DatabaseItem.add_item(im_name[i]))

    id_equipment = DatabaseEquipment.add_equipment(helmet=im_id[0], chest=im_id[1], leg_armor=im_id[2], boots=im_id[3],
                                                   left_hand=im_id[4])
    db_d = DatabaseEquipment.get_equipment(id_equipment)

    assert id_equipment == db_d['id_equipment']
    assert im_id[0] == db_d['helmet']
    assert im_id[1] == db_d['chest']
    assert im_id[2] == db_d['leg_armor']
    assert im_id[3] == db_d['boots']
    assert im_id[4] == db_d['left_hand']
    assert db_d['right_hand'] is None
    assert db_d['accessory'] is None
