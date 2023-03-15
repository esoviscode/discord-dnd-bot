import copy
import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.multiverse import Multiverse as Mv

TMP_IMAGES_PATH = 'dnd_bot/assets/tmp'


def generate_circle_points(radius: int, range_length: int, outer=False) -> list:
    """
    returns list of points of filled circle (centered at 0,0) for given radius
    :param radius: circle radius
    :param range_length: outer square range
    :param outer: if to generate the outer points or inner
    :return points: list of tuples (x, y)
    """

    # mod is conditional variable which defines proper circles
    mod = 1
    if 3 < radius < 6:
        mod = 4
    elif radius >= 6:
        mod = 5

    def belongs_to_circle(x, y):
        return x ** 2 + y ** 2 <= radius ** 2 + mod

    points = []

    if outer:
        for y in range(-range_length, range_length + 1):
            for x in range(-range_length, range_length + 1):
                if not belongs_to_circle(x, y):
                    points.append((x, y))
    else:
        for y in range(-range_length, range_length + 1):
            for x in range(-range_length, range_length + 1):
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
    whole_map = cv.imread(game.sprite, cv.IMREAD_UNCHANGED)

    objects = [o for o in sum(game.entities, []) if o and not o.fragile]
    for obj in objects:
        sprite = rotate_image_to_direction(obj.sprite, obj.look_direction)
        paste_image(sprite, whole_map, obj.x * Mv.square_size, obj.y * Mv.square_size)

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
    player_view = copy.deepcopy(game.sprite)

    # pasting entities in vision
    points_in_range = generate_circle_points(player.perception, Mv.view_range)
    entities = [e for e in sum(game.entities, []) if e and e.fragile
                and (e.x - player.x, e.y - player.y) in points_in_range]

    for entity in entities:
        sprite = copy.deepcopy(entity.sprite)
        sprite = rotate_image_to_direction(sprite, entity.look_direction)

        paste_image(sprite, player_view, entity.x * Mv.square_size, entity.y * Mv.square_size)

    # cropping image
    from_y = max(0, player.y - Mv.view_range)
    to_y = min(game.world_height, player.y + Mv.view_range + 1)
    from_x = max(0, player.x - Mv.view_range)
    to_x = min(game.world_width, player.x + Mv.view_range + 1)
    player_view = player_view[from_y * Mv.square_size:to_y * Mv.square_size,
                              from_x * Mv.square_size:to_x * Mv.square_size]

    # cropping mask
    mask = Mv.masks[player.perception][
           -min(0, player.y - Mv.view_range) * Mv.square_size:
           ((Mv.view_range * 2 + 1) + min(0, (game.world_height - 1 - player.y - Mv.view_range))) * Mv.square_size,
           -min(0, player.x - Mv.view_range) * Mv.square_size:
           ((Mv.view_range * 2 + 1) + min(0, (game.world_width - 1 - player.x - Mv.view_range))) * Mv.square_size]

    # pasting player's blind spots
    player_view = cv.bitwise_and(player_view, player_view, mask=mask)

    # pasting coordinates and grid
    number_width = 10
    number_height = 13
    number_space = 1
    width = to_x - from_x + 1
    height = to_y - from_y + 1

    def length(num):
        return len(str(num)) * number_width + (len(str(num)) + 1) * number_space

    padding_top = 10 + number_height
    padding_left = 10 + length(height)
    square = 50
    line_color = (110, 110, 110)

    coords = np.zeros((player_view.shape[0] + padding_top, player_view.shape[1] + padding_left, player_view.shape[2]),
                      player_view.dtype)
    lines = coords.copy()
    coords[padding_top:, padding_left:, :] = player_view[:, :, :]

    for i in range(width + 1):
        cv.line(lines, (padding_left + i * square - 1, padding_top), (padding_left + i * square - 1, coords.shape[0]),
                line_color, 1)
        cv.putText(img=coords, text=str(from_x + i),
                   org=(padding_left + i * square + (square - length(i + 1)) // 2, padding_top - 6),
                   fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.55, color=(200, 200, 200), thickness=1)
    for i in range(height + 1):
        cv.line(lines, (padding_left, padding_top + i * square - 1), (coords.shape[1], padding_top + i * square - 1),
                line_color, 1)
        cv.putText(img=coords, text=str(from_y + i),
                   org=(padding_left - length(i + 1) - 5, padding_top + ((i + 1) * square - 19)),
                   fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.55, color=(200, 200, 200), thickness=1)

    player_view = cv.addWeighted(lines, .6, coords, 1.0, 0)

    # saving view
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
