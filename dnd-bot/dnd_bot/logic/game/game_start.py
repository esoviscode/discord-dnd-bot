from dnd_bot.logic.game.initialize_world import InitializeWorld
from dnd_bot.logic.prototype.multiverse import Multiverse


class GameStart:

    @staticmethod
    def start(token):
        game = Multiverse.get_game(token)

        game.game_state = 'ACTIVE'

        InitializeWorld.load_entities(game, 'dnd_bot/assets/maps/map.json')





