from threading import Thread

from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerGame:
    @staticmethod
    def handle_game(token):
        """creates a game loop running in the background in a parallel thread"""
        game = Multiverse.get_game(token)

        # create a separate thread running the main game loop
        thread = Thread(target=GameLoop.game_loop, args=(token,))
        game.game_loop_thread = thread
        thread.start()
