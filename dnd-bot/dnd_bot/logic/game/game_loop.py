import asyncio
import copy

from dnd_bot.dc.ui.views.view_game import ViewMain
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


class GameLoop:
    """This class manages all logic behind turns. The idea of usage is that when player invokes a command/action then
    the static method of this class is called.
    """

    @staticmethod
    def prepare_queue(game: Game):
        """puts all the creatures to the queue with order by initiative"""

        def entity_sorting_value(e):
            if not isinstance(e, Creature):
                return -1
            else:
                return e.initiative

        # sort entities to put creatures into the queue in right order
        entities = game.get_movable_entities()
        entities.sort(reverse=True, key=entity_sorting_value)

        # make sure that the queue is empty
        if not len(game.creatures_queue) == 0:
            game.creatures_queue.clear()

        # add creatures to the queue
        for c in entities:
            if isinstance(c, Creature) or isinstance(c, Player):
                game.creatures_queue.append(c)

    @staticmethod
    def creatures_queue_contains_any_player(game: Game):
        queue = copy.deepcopy(game.creatures_queue)
        for creature in queue:
            if isinstance(creature, Player):
                return True

        return False

    @staticmethod
    def get_game_object(game_token):
        """returns game object from given id"""
        return Multiverse.get_game(game_token)

    @staticmethod
    def game_loop(game_token):
        """loops over all creatures and lets them perform actions, each iteration is a move"""
        game = GameLoop.get_game_object(game_token)

        while game.game_state == 'ACTIVE':
            # each iteration is a creature's move
            current_creature: Creature = game.creatures_queue.popleft()

            if len(game.creatures_queue) == 0:
                GameLoop.prepare_next_round(game)

            if isinstance(current_creature, Player):
                GameLoop.players_turn(game, current_creature)
            else:
                GameLoop.creature_turn(game, current_creature)

    @staticmethod
    def prepare_next_round(game: Game):
        GameLoop.prepare_queue(game)

        next_active_player = None
        for i, creature in enumerate(Multiverse.get_game(game.token).creatures_queue):
            if isinstance(creature, Player):
                next_active_player = Multiverse.get_game(game.token).creatures_queue[i]
                break
        if next_active_player is None:
            print('SEVERE: no active player')
            return

        asyncio.run(ViewMain.send_new_round_messages(game.token, next_active_player))

    @staticmethod
    def players_turn(game, player):
        """one turn of a player"""
        player.active = True

        while True:
            # player performs asynchronous actions via commands or buttons
            if not player.active:
                break

    @staticmethod
    def creature_turn(game, creature):
        """one turn of a creature"""
        # TODO creature performs some actions
        print(f'turn of {creature.name}')
