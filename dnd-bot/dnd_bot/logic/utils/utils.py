import copy
import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.player import Player

TMP_IMAGES_PATH = 'dnd_bot/assets/tmp'


def generate_superset_circle_points(radius: int, range_length: int) -> list:
    """
    returns list of points of filled circle (centered at 0,0) for given radius
    :param radius: circle radius
    :param range_length: outer square range
    :return points: list of tuples (x, y)
    """

    def belongs_to_circle(x, y):
        return x ** 2 + y ** 2 <= radius ** 2 + 1

    points = []

    for y in range(-range_length, range_length + 1):
        for x in range(-range_length, range_length + 1):
            if not belongs_to_circle(x, y):
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
    square_size = 50
    whole_map = cv.imread(game.sprite, cv.IMREAD_UNCHANGED)

    objects = [o for o in sum(game.entities, []) if o and not o.fragile]
    for obj in objects:
        sprite = rotate_image_to_direction(obj.sprite, obj.look_direction)
        paste_image(sprite, whole_map, obj.x * square_size, obj.y * square_size)

    file_name = "%s/game_images/map%s.png" % (TMP_IMAGES_PATH, game.token)

    cv.imwrite(file_name, whole_map, [cv.IMWRITE_PNG_COMPRESSION, 9])
    del whole_map

    return file_name


def get_player_view(game: Game, player: Player):
    """
    generates image and returns its path
    :param game: game object
    :param player: player
    :return filename: path to game view image with player's POV
    """
    view_range = 4
    square_size = 50
    player_view = copy.deepcopy(game.sprite)

    entities = [e for e in sum(game.entities, []) if e and e.fragile]
    for entity in entities:
        sprite = copy.deepcopy(entity.sprite)
        sprite = rotate_image_to_direction(sprite, entity.look_direction)

        paste_image(sprite, player_view, entity.x * square_size, entity.y * square_size)

    blind_spot = np.zeros((square_size, square_size, 3), np.uint8)
    for point in generate_superset_circle_points(player.perception, view_range):
        if player.x + point[0] >= 0 and (player.x + point[0] + 1) * square_size <= player_view.shape[1] \
                and player.y + point[1] >= 0 and (player.y + point[1] + 1) * square_size <= player_view.shape[0]:
            player_view[(player.y + point[1]) * square_size:(player.y + point[1] + 1) * square_size,
                        (player.x + point[0]) * square_size:(player.x + point[0] + 1) * square_size, :] \
                = blind_spot

    player_view = player_view[max(0, player.y - view_range) * square_size:
                              min(player_view.shape[0], (player.y + view_range + 1) * square_size),
                              max(0, player.x - view_range) * square_size:
                              min(player_view.shape[1], (player.x + view_range + 1) * square_size)]

    file_name = "%s/game_images/pov%s_%s.png" % (TMP_IMAGES_PATH, game.token, player.discord_identity)

    cv.imwrite(file_name, player_view, [cv.IMWRITE_PNG_COMPRESSION, 9])
    del player_view

    return file_name


def rotate_image_to_direction(img, direction):
    """rotates image by given direction"""
    if direction == 'down':
        return img
    if direction == 'right':
        image = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    elif direction == 'left':
        image = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    elif direction == 'up':
        image = cv.rotate(img, cv.ROTATE_180)
    return image
