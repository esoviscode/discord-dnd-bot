from dnd_bot.dc.ui.views.view_game import ViewCharacterNonActive, ViewGame
import asyncio
import copy

from dnd_bot.dc.ui.views.view_game import ViewMain
from dnd_bot.logic.prototype.creature import Creature
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
    def get_game_object(game_token):
        """returns game object from given id"""
        return Multiverse.get_game(game_token)

    @staticmethod
    async def start_loop(game_token):
        """prepares the queue for the game and begins turns of the creatures"""
        game = GameLoop.get_game_object(game_token)

        GameLoop.prepare_queue(game)

        first_creature = game.creatures_queue.popleft()
        game.active_creature = first_creature

        for user in game.user_list:
            game.players_views[user.discord_id] = (ViewCharacterNonActive, [])
        if isinstance(first_creature, Player):
            game.players_views[first_creature.discord_identity] = (ViewMain, [])

        await ViewGame.display_views_for_users(game_token, "Let the adventure begin!")

        # move of non player creature
        if not isinstance(first_creature, Player):
            from dnd_bot.logic.game.handler_game import HandlerGame
            await HandlerGame.turn(game_token, first_creature)


