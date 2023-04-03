import pytest

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.database.database_player_item import DatabasePlayerItem
from dnd_bot.logic.prototype.item import Item
from dnd_bot.logic.prototype.player import Player

from dnd_bot.tests.autoconf import database_fixture

postgresql, postgresql_in_docker = database_fixture('player_item')


def test_add_creature_item(postgresql):
    cur = postgresql.cursor()

    DatabaseConnection.connection = postgresql
    DatabaseConnection.cursor = cur

    p = Player(x=0, y=0, name='Creature', hp=0, strength=0, dexterity=0, intelligence=0, charisma=0,
               perception=0, initiative=0, action_points=0, level=0, equipment=None, money=0, game_token='',
               experience=0)
    p.id = DatabasePlayer.add_player(x=p.x, y=p.y, name=p.name, hp=p.hp, strength=p.strength, dexterity=p.dexterity,
                                     intelligence=p.intelligence, charisma=p.charisma, perception=p.perception,
                                     initiative=p.initiative, action_points=p.action_points, level=p.level,
                                     experience=p.experience)

    i = Item(name='TestItem', hp=1, strength=2, dexterity=3, intelligence=4, charisma=5, perception=6, action_points=7,
             effect='efekt', base_price=8, use_range=1, description="test item")
    i.id = DatabaseItem.add_item(i.name)
    DatabasePlayerItem.add_player_item(p.id, i.id, 2)
    list = DatabasePlayerItem.get_creature_items(p.id)
    assert list[0][0] == i.id
    assert list[0][1] == 2
