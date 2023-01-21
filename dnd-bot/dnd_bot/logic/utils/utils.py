import copy
import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.player import Player


def generate_filled_circle_points(radius: int) -> list:
    """
    returns list of points of filled circle (centered at 0,0) for given radius
    :param radius: circle radius
    :return points: list of tuples (x, y)
    """
    def belongs_to_circle(x, y):
        return x**2 + y**2 <= radius**2 + 1

    points = []

    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if belongs_to_circle(x, y):
                points.append((x, y))

    return points


def paste_image(src: np.ndarray, dest: np.ndarray, x_offset: int, y_offset: int):
    """
    pastes src on dest with x,y offsets
    :param src: source image
    :param dest: destination image
    :param x_offset: x offset in dest
    :param y_offset: y offset in dest
    """
    y1, y2 = y_offset, y_offset + src.shape[0]
    x1, x2 = x_offset, x_offset + src.shape[1]

    alpha_src = src[:, :, 3] / 255.0
    alpha_dest = 1.0 - alpha_src

    for c in range(0, 3):
        dest[y1:y2, x1:x2, c] = (alpha_src * src[:, :, c] + alpha_dest * dest[y1:y2, x1:x2, c])


def get_game_view(game: Game) -> str:
    """
    generates image and returns its path
    :param game: game object
    :return filename: path to game view image
    """
    map_margin = 100
    square_size = 50
    whole_map = cv.imread(game.sprite, cv.IMREAD_UNCHANGED)

    objects = [o for o in sum(game.entities, []) if o and not o.fragile]
    for obj in objects:
        paste_image(obj.sprite, whole_map, map_margin + obj.x * square_size, map_margin + obj.y * square_size)

    file_name = "dnd_bot/logic/utils/game_images/map%s.png" % game.token

    cv.imwrite(file_name, whole_map)
    del whole_map

    return file_name


def get_player_view(game: Game, player: Player):
    """
    generates image and returns its path
    :param game: game object
    :param player: player
    :return filename: path to game view image with player's POV
    """
    view_range = 2
    map_margin = 100
    square_size = 50
    player_view = copy.deepcopy(game.sprite)

    entities = [e for e in sum(game.entities, []) if e and e.fragile]
    for entity in entities:
        paste_image(entity.sprite, player_view, map_margin + entity.x * square_size,
                    map_margin + entity.y * square_size)

    player_view = player_view[map_margin + (player.y - view_range) * square_size:
                              map_margin + (player.y + view_range + 1) * square_size,
                              map_margin + (player.x - view_range) * square_size:
                              map_margin + (player.x + view_range + 1) * square_size, :]

    file_name = "dnd_bot/logic/utils/game_images/pov%s_%s.png" % (game.token, player.discord_identity)

    cv.imwrite(file_name, player_view)
    del player_view

    return file_name
