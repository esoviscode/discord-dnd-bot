import asyncio

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.handler_views import HandlerViews
from dnd_bot.dc.ui.views.view_game import ViewCharacterNonActive, ViewMain
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

            # delete any error messages that were left out
            await Messager.delete_last_user_error_message(game.active_creature.discord_identity, game_token)

        recent_action_message = MessageTemplates.end_turn_recent_action_message(game.active_creature)

        # reset creature's action points to the initial value
        game.active_creature.action_points = game.active_creature.initial_action_points
        game.active_creature = next_creature

        # send messages to users
        await HandlerViews.display_views_for_users(game_token, recent_action_message)

        if not isinstance(game.active_creature, Player):
            await HandlerGame.turn(game_token, game.active_creature)

    @staticmethod
    async def turn(game_token, active_creature):
        game = Multiverse.get_game(game_token)
        while game.active_creature.action_points > 0:
            recent_action_message = await active_creature.ai_action()
            await asyncio.sleep(1)
            print(f"{active_creature.name}<{active_creature.id}>", recent_action_message)
            await HandlerViews.display_views_for_users(game_token, recent_action_message)

        await HandlerGame.end_turn(game_token)

    @staticmethod
    async def pause_game(token: str = ''):
        """pauses game based on the token.
           Game is saved to db and state is set to INACTIVE"""
        game = Multiverse.get_game(token)

        if not game:
            raise Exception('Game with provided token doesn\'t exist!')

        game.status = 'INACTIVE'

        # TODO save game state to database

    @staticmethod
    async def resume_game(token: str = ''):
        """resumes game based on a token.
           Game is loaded from db and state is set to ACTIVE"""
        game = Multiverse.get_game(token)

        if not game:
            raise Exception('Game with provided token doesn\'t exist!')

        # TODO load game state from database

        game.status = 'ACTIVE'
