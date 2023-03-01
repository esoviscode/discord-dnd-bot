import copy
import numpy as np


class Multiverse:
    """contains the list of all the games (objects of Game class) that are being played"""
    games = dict()
    square_size = 50
    view_range = 4
    masks = dict()

    @staticmethod
    def get_game(token):
        return Multiverse.games[token]

    @staticmethod
    def add_game(game) -> None:
        Multiverse.games[game.token] = copy.deepcopy(game)

    @staticmethod
    def generate_masks():
        from dnd_bot.logic.utils.utils import generate_circle_points
        import cv2 as cv

        blank_view = np.zeros((Multiverse.square_size * (Multiverse.view_range * 2 + 1),
                               Multiverse.square_size * (Multiverse.view_range * 2 + 1), 3), np.uint8)

        for p in range(1, Multiverse.view_range + 1):
            mask = np.zeros(blank_view.shape[:2], dtype="uint8")
            for x, y in generate_circle_points(p, Multiverse.view_range):
                cv.rectangle(mask,
                             ((x+Multiverse.view_range) * Multiverse.square_size,
                              (y+Multiverse.view_range) * Multiverse.square_size),
                             ((x+Multiverse.view_range+1) * Multiverse.square_size,
                              (y+Multiverse.view_range+1) * Multiverse.square_size),
                             255, -1)
            Multiverse.masks[p] = mask
