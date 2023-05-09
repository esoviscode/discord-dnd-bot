import copy
import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.multiverse import Multiverse as Mv

TMP_IMAGES_PATH = 'dnd_bot/assets/tmp'


def in_range(from_x: int, from_y: int, to_x: int, to_y: int, radius_range: int) -> bool:
    # mod is conditional variable which depends on radius_range
    mod = 1
    if 3 < radius_range < 6:
        mod = 4
    elif radius_range >= 6:
        mod = 5

    return (from_x - to_x) ** 2 + (from_y - to_y) ** 2 <= radius_range ** 2 + mod


def generate_circle_points(radius: int, range_length: int, outer=False) -> list:
    """
    returns list of points of filled circle (centered at 0,0) for given radius
    :param radius: circle radius
    :param range_length: outer square range
    :param outer: if to generate the outer points or inner
    :return points: list of tuples (x, y)
    """
    points = []

    if outer:
        for y in range(-range_length, range_length + 1):
            for x in range(-range_length, range_length + 1):
                if not in_range(0, 0, x, y, radius):
                    points.append((x, y))
    else:
        for y in range(-range_length, range_length + 1):
            for x in range(-range_length, range_length + 1):
                if in_range(0, 0, x, y, radius):
                    points.append((x, y))

    return points


def find_position_to_check(from_x: int, from_y: int, to_x: int, to_y: int) -> list:
    """returns discrete segment from point to point
    algorithm on the basis of midpoint alg extended with symmetrical smoothing
    :param from_x: start x coordinate
    :param from_y: start y coordinate
    :param to_x: end x coordinate
    :param to_y: end y coordinate
    :return path: list of points (x, y)"""

    if from_x == to_x:  # vertical line
        bias = 1 if to_y >= from_y else -1
        return [(from_x, y) for y in range(from_y, to_y + bias, bias)]

    import math
    return_x = False
    return_y = False
    mirror = False

    # transformations
    # all to trivialize the slope to be in 1st quarter and <= 45°
    if to_x < from_x:  # angle quarter 3,4
        to_x = 2 * from_x - to_x
        return_x = True
    if to_y < from_y:  # angle quarter 2,3
        to_y = 2 * from_y - to_y
        return_y = True
    if to_y - from_y > to_x - from_x:  # > 45°
        to_x, to_y = from_x + (to_y - from_y), from_y + (to_x - from_x)
        mirror = True

    # linear function parameters
    a = (to_y - from_y) / (to_x - from_x)
    b = from_y - .5 - (from_x - .5) * a

    # segment's dimensions
    length = to_x - from_x + 1
    width = to_y - from_y + 1
    mid = math.ceil((to_x + from_x) / 2)
    center = (to_y + from_y) // 2

    left = []
    right = []

    # predict points
    for x in range(from_x, mid):
        x_cen = x - .5
        y_cen = x_cen * a + b
        y = math.ceil(y_cen)
        left.append((x, y))
        right.insert(0, (to_x - x + from_x, to_y - y + from_y))

    # handle center point/points
    if length % 2 == 1:
        if width % 2 == 0:
            path = left + [(mid, center), (mid, center + 1)] + right
        else:
            path = left + [(mid, center)] + right
    else:
        path = left + right

    # reverse transformations
    if mirror:
        path = [(from_x + (p[1] - from_y), from_y + (p[0] - from_x)) for p in path]

    if return_y:
        path = [(p[0], 2 * from_y - p[1]) for p in path]

    if return_x:
        path = [(2 * from_x - p[0], p[1]) for p in path]

    return path


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


def get_player_view(game: Game, player: Player, attack_mode=False):
    """
    generates image and returns its path
    :param game: game object
    :param player: player
    :param attack_mode: if to paste grid, coords, and attackable tiles
    :return filename: path to game view image with player's POV
    """
    player_view = copy.deepcopy(game.sprite)

    # pasting entities in vision
    points_in_range = generate_circle_points(min(player.perception, 4), Mv.view_range)
    entities = [e for e in sum(game.entities, []) if e and e.fragile
                and (e.x - player.x, e.y - player.y) in points_in_range]

    # cropping image
    from_y = max(0, player.y - Mv.view_range)
    to_y = min(game.world_height, player.y + Mv.view_range + 1)
    from_x = max(0, player.x - Mv.view_range)
    to_x = min(game.world_width, player.x + Mv.view_range + 1)
    player_view = player_view[from_y * Mv.square_size:to_y * Mv.square_size,
                              from_x * Mv.square_size:to_x * Mv.square_size]

    # cropping mask
    mask = Mv.masks[min(player.perception, 4)][
           -min(0, player.y - Mv.view_range) * Mv.square_size:
           ((Mv.view_range * 2 + 1) + min(0, (game.world_height - 1 - player.y - Mv.view_range))) * Mv.square_size,
           -min(0, player.x - Mv.view_range) * Mv.square_size:
           ((Mv.view_range * 2 + 1) + min(0, (game.world_width - 1 - player.x - Mv.view_range))) * Mv.square_size]

    # pasting player's blind spots
    player_view = cv.bitwise_and(player_view, player_view, mask=mask)

    # pasting coordinates and grid
    if attack_mode:
        attackable = []
        attack_range = min(player.equipment.right_hand.use_range, player.perception)
        from dnd_bot.logic.prototype.creature import Creature
        for p in generate_circle_points(attack_range, attack_range):
            x = player.x + p[0]
            y = player.y + p[1]
            if x < 0 or x >= game.world_width or y < 0 or y >= game.world_height:
                continue
            if (not game.entities[y][x]) or \
                    (isinstance(game.entities[y][x], Creature) and not isinstance(game.entities[y][x], Player)):
                path = find_position_to_check(player.x, player.y, player.x + p[0], player.y + p[1])
                add = True
                for pos in path[1:-1]:
                    if game.entities[pos[1]][pos[0]]:
                        add = False
                        break
                if add:
                    attackable.append((x, y))

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
        attack_color = (0, 0, 50)

        coords = np.zeros((player_view.shape[0] + padding_top, player_view.shape[1] + padding_left, player_view.shape[2]),
                          player_view.dtype)
        lines = coords.copy()
        tiles = coords.copy()
        coords[padding_top:, padding_left:, :] = player_view[:, :, :]

        for p in attackable:
            cv.rectangle(tiles, (padding_left + (p[0] - from_x) * square, padding_top + (p[1] - from_y) * square),
                         (padding_left + (p[0] - from_x + 1) * square - 1,
                          padding_top + (p[1] - from_y + 1) * square - 1), attack_color, -1)

        for i in range(width + 1):
            cv.line(lines, (padding_left + i * square - 1, padding_top),
                    (padding_left + i * square - 1, coords.shape[0]), line_color, 1)
            cv.putText(img=coords, text=str(from_x + i),
                       org=(padding_left + i * square + (square - length(from_x + i)) // 2, padding_top - 6),
                       fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.55, color=(200, 200, 200), thickness=1, lineType=cv.LINE_AA)
        for i in range(height + 1):
            cv.line(lines, (padding_left, padding_top + i * square - 1),
                    (coords.shape[1], padding_top + i * square - 1), line_color, 1)
            cv.putText(img=coords, text=str(from_y + i),
                       org=(padding_left - length(from_y + i) - 5, padding_top + ((i + 1) * square - 19)),
                       fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=0.55, color=(200, 200, 200), thickness=1, lineType=cv.LINE_AA)

        player_view = cv.addWeighted(tiles, .4, coords, 1.0, 0)
        player_view = cv.addWeighted(lines, .6, player_view, 1.0, 0)

    for entity in entities:
        sprite = copy.deepcopy(entity.sprite)
        sprite = rotate_image_to_direction(sprite, entity.look_direction)

        if attack_mode:
            paste_image(sprite, player_view, padding_left + (entity.x - from_x) * Mv.square_size,
                        padding_top + (entity.y - from_y) * Mv.square_size)
        else:
            paste_image(sprite, player_view, (entity.x - from_x) * Mv.square_size, (entity.y - from_y) * Mv.square_size)

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


def string_to_character_class(class_name: str, token: str):
    """
    returns object of python class defining particular character class in particular game given its name
    :param class_name: name of character class
    :param token: game token
    :return class: object defining character class
    """
    from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
    game = Mv.get_game(token)

    for character_class in HandlerCharacterCreation.campaigns[game.campaign_name]["classes"]:
        if character_class.name == class_name:
            return character_class
    return None


def string_to_character_race(race_name: str, token: str):
    """
        returns object of class defining particular character race given its name
        :param race_name: name of character class
        :param token: game token
        :return class: object defining character race
    """
    from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation
    game = Mv.get_game(token)

    for character_race in HandlerCharacterCreation.campaigns[game.campaign_name]["races"]:
        if character_race.name == race_name:
            return character_race
    return None


def campaign_name_to_path(campaign_name: str = "") -> str:
    """return path to json containing campaign given campaign name"""
    path = "dnd_bot/assets/campaigns/"
    if campaign_name == "Storm King's Thunder":
        path += "campaign.json"
    return path
