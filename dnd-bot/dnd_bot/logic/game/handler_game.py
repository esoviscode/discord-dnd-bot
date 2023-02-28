from threading import Thread

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.views.view_game import ViewMain
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerGame:
    @staticmethod
    def end_turn(game_token):
        game = Multiverse.get_game(game_token)

        next_creature = game.creatures_queue.popleft()

        if len(game.creatures_queue) == 0:
            GameLoop.prepare_queue(game)

        recent_action_message = MessageTemplates.end_turn_recent_action_message(game.active_creature)
        ViewMain.display_views_for_users(game_token, next_creature, recent_action_message)

        # reset creature's stats
        game.active_creature.action_points = game.active_creature.initial_action_points

        game.active_creature = next_creature
