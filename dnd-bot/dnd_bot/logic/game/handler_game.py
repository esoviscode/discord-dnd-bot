import asyncio
from datetime import time

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.views.view_game import ViewCharacterNonActive, ViewGame, ViewMain
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player


class HandlerGame:
    @staticmethod
    async def end_turn(game_token):
        game = Multiverse.get_game(game_token)

        if len(game.creatures_queue) == 0:
            GameLoop.prepare_queue(game)

        next_creature = game.creatures_queue.popleft()

        if isinstance(next_creature, Player):
            game.players_views[next_creature.discord_identity] = (ViewMain, [])

        if isinstance(game.active_creature, Player):
            game.players_views[game.active_creature.discord_identity] = (ViewCharacterNonActive, [])

        recent_action_message = MessageTemplates.end_turn_recent_action_message(game.active_creature)
        await ViewGame.display_views_for_users(game_token, recent_action_message)

        # reset creature's action points to the initial value
        game.active_creature.action_points = game.active_creature.initial_action_points

        game.active_creature = next_creature

        if not isinstance(game.active_creature, Player):
            await HandlerGame.turn(game_token, game.active_creature)

    @staticmethod
    async def turn(game_token, active_creature):
        game = Multiverse.get_game(game_token)
        while game.active_creature.action_points > 0:
            recent_action_message = active_creature.ai_action()
            await asyncio.sleep(1)
            print(f"Turn executed in {active_creature.name}")
            await ViewGame.display_views_for_users(game_token, recent_action_message)

        await HandlerGame.end_turn(game_token)
