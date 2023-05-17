import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.database.database_player_item import DatabasePlayerItem
from dnd_bot.logic.prototype.item import Item
from dnd_bot.logic.prototype.player import Player

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('db_player_item')


def test_add_player_item(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur
    p = Player(x=0, y=0, name='Creature', hp=0, strength=0, dexterity=0, intelligence=0, charisma=0,
               perception=0, initiative=0, action_points=0, level=0, equipment=None, money=0, game_token='',
               experience=0)
    p.id = DatabasePlayer.add_player(x=p.x, y=p.y, name=p.name, hp=p.hp, strength=p.base_strength, dexterity=p.base_dexterity,
                                     intelligence=p.base_intelligence, charisma=p.base_charisma, perception=p.base_perception,
                                     initiative=p.initiative, action_points=p.action_points, level=p.level,
                                     experience=p.experience, max_hp=p.max_hp, initial_action_points=p.initial_action_points)

    i = Item(name='TestItem', hp=1, strength=2, dexterity=3, intelligence=4, charisma=5, perception=6, action_points=7,
             effect='efekt', base_price=8, use_range=1, description="test item")
    i.id = DatabaseItem.add_item(i.name)
    DatabasePlayerItem.add_player_item(p.id, i.id, 2)
    list = DatabaseConnection.get_object_from_db('SELECT id_player, id_item, amount FROM public."Player_Item"')
    assert list[0] == p.id
    assert list[1] == i.id
    assert list[2] == 2


def test_get_player_items(postgresql):
    cur = postgresql.cursor()
    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    p = Player(x=0, y=0, name='Creature', hp=0, strength=0, dexterity=0, intelligence=0, charisma=0,
               perception=0, initiative=0, action_points=0, level=0, equipment=None, money=0, game_token='',
               experience=0)
    p.id = DatabasePlayer.add_player(x=p.x, y=p.y, name=p.name, hp=p.hp, strength=p.base_strength, dexterity=p.base_dexterity,
                                     intelligence=p.base_intelligence, charisma=p.base_charisma, perception=p.base_perception,
                                     initiative=p.initiative, action_points=p.action_points, level=p.level,
                                     experience=p.experience, max_hp=p.max_hp, initial_action_points=p.initial_action_points)

    i = Item(name='TestItem', hp=1, strength=2, dexterity=3, intelligence=4, charisma=5, perception=6, action_points=7,
             effect='efekt', base_price=8, use_range=1, description="test item")
    i.id = DatabaseItem.add_item(i.name)
    DatabasePlayerItem.add_player_item(p.id, i.id, 2)
    list = DatabasePlayerItem.get_player_items(p.id)
    assert list[0]['id_item'] == i.id
    assert list[0]['amount'] == 2
    assert list[0]['id_player'] == p.id
