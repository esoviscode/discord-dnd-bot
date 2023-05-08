import random
from random import randint

import dnd_bot.logic.prototype.player
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.misc.corpse import Corpse
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.items.item import Item


class HandlerKillEnemy:

    @staticmethod
    def handle_kill_enemy(game: Game, enemy: Creature):
        """handles the creation of enemies' bodies and theirs drops"""
        if isinstance(enemy, dnd_bot.logic.prototype.player.Player):
            return

        # in campaign.json drop money is defined as two element array defining the range of money to be dropped
        dropped_money = randint(enemy.drop_money[0], enemy.drop_money[1])

        # in campaign.json drops are defined as item and its chance to drop. more than one item can drop at a time
        dropped_items = []
        if enemy.drops:
            for item_name in enemy.drops:
                chance = enemy.drops[item_name]
                if random.random() < chance:
                    dropped_items.append(Item(name=item_name))

        # creating corpse entity
        # if you want the corpse to have other sprite pass its path below
        game.add_entity(Corpse(enemy.x, enemy.y, game.token, enemy.name, dropped_money, dropped_items, sprite_path=None))
