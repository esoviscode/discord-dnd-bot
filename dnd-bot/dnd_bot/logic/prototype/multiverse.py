import copy

from dnd_bot.logic.prototype.game import Game


class Multiverse:
    """contains the list of all the games (objects of Game class) that are being played"""
    games = {}

    @staticmethod
    def get_game(token) -> Game:
        return Multiverse.games[token]

    @staticmethod
    def add_game(game) -> None:
        Multiverse.games[game.token] = copy.deepcopy(game)
