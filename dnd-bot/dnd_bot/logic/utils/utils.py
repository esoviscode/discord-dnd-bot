import copy
import cv2 as cv
import numpy as np

<<<<<<< HEAD
from dnd_bot.logic.prototype.creature import Creature
=======
from dnd_bot.logic.prototype.classes.mage import Mage
from dnd_bot.logic.prototype.classes.ranger import Ranger
from dnd_bot.logic.prototype.classes.warrior import Warrior
>>>>>>> staging
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.multiverse import Multiverse as Mv
from dnd_bot.logic.prototype.races.dwarf import Dwarf
from dnd_bot.logic.prototype.races.elf import Elf
from dnd_bot.logic.prototype.races.human import Human

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


def find_position_to_check(x_src=0, y_src=0, x_dest=1, y_dest=1):
    result = []

    def find_positions(x1, y1, x2, y2, dx, dy, decide):
        pk = 2 * dy - dx
        for i in range(0, dx + 1):
            if decide == 0:
                result.append((x1, y1))
            else:
                result.append((y1, x1))

            if x1 < x2:
                x1 = x1 + 1
            else:
                x1 = x1 - 1
            if pk < 0:

                if decide == 0:
                    pk = pk + 2 * dy
                else:
                    pk = pk + 2 * dy
            else:
                if y1 < y2:
                    y1 = y1 + 1
                else:
                    y1 = y1 - 1

                pk = pk + 2 * dy - 2 * dx

    dx = abs(x_dest - x_src)
    dy = abs(y_dest - y_src)

    # If slope is less than one
    if dx > dy:
        find_positions(x_src, y_src, x_dest, y_dest, dx, dy, 0)
    # if slope is greater than or equal to 1
    else:
        find_positions(y_src, x_src, y_dest, x_dest, dy, dx, 1)

    return result[1:-1]


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
        tmp1 = dest[y1:y2, x1:x2, c]
        tmp2 = alpha_src * src[:, :, c]
        tmp3 = alpha_dest * dest[y1:y2, x1:x2, c]

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
    points_in_range = generate_circle_points(player.perception, Mv.view_range)
    entities = [e for e in sum(game.entities, []) if e and e.fragile
                and (e.x - player.x, e.y - player.y) in points_in_range]

    # for entity in entities:
    #     sprite = copy.deepcopy(entity.sprite)
    #     sprite = rotate_image_to_direction(sprite, entity.look_direction)
    #
    #     paste_image(sprite, player_view, entity.x * Mv.square_size, entity.y * Mv.square_size)

    # raytracing
    mask_points, _ = get_non_visible_tiles_in_player_view(game, player)
    for x, y in mask_points:
        cv.rectangle(player_view, (x * Mv.square_size, y * Mv.square_size),
                     ((x + 1) * Mv.square_size, (y + 1) * Mv.square_size),
                     (0, 0, 0), -1)

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
                for pos in path:
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


<<<<<<< HEAD
def get_non_visible_tiles_in_player_view(game: Game, player: Player):
    result = []
    obstacles = []
    for ray_destination in generate_hollow_square_points(player.perception + 1):
        ray_points = find_position_to_check(player.x, player.y,
                                            player.x + ray_destination[0], player.y + ray_destination[1])

        obstacle_index = 0
        found_obstacle = False
        for i, point in enumerate(ray_points):
            checked_entity = game.get_entity_by_x_y(x=point[0], y=point[1])

            if checked_entity and not isinstance(checked_entity, Creature):
                found_obstacle = True
                obstacle_index = i
                obstacles.append(point)

                break

        if found_obstacle:
            [result.append(point) for point in ray_points[obstacle_index + 1:] if point not in result and
             point[0] in range(0, game.world_width) and point[1] in range(0, game.world_height)]

    return result, obstacles


def generate_hollow_square_points(radius):
    """
    returns a hollow square centered around 0,0
    """
    result = []
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i in [-radius, radius] or j in [-radius, radius]:
                result.append((i, j))

    return result


def find_position_to_check(x_src=0, y_src=0, x_dest=1, y_dest=1):
    result = []

    def find_positions(x1, y1, x2, y2, dx, dy, decide):
        pk = 2 * dy - dx
        for i in range(0, dx + 1):
            if decide == 0:
                result.append((x1, y1))
            else:
                result.append((y1, x1))

            if x1 < x2:
                x1 = x1 + 1
            else:
                x1 = x1 - 1
            if pk < 0:

                if decide == 0:
                    pk = pk + 2 * dy
                else:
                    pk = pk + 2 * dy
            else:
                if y1 < y2:
                    y1 = y1 + 1
                else:
                    y1 = y1 - 1

                pk = pk + 2 * dy - 2 * dx

    dx = abs(x_dest - x_src)
    dy = abs(y_dest - y_src)

    # If slope is less than one
    if dx > dy:
        find_positions(x_src, y_src, x_dest, y_dest, dx, dy, 0)
    # if slope is greater than or equal to 1
    else:
        find_positions(y_src, x_src, y_dest, x_dest, dy, dx, 1)

    return result[1:-1]
=======
def string_to_character_class(class_name: str):
    """
    returns class (not object) defining particular character class given its name
    :param class_name: name of character class
    :return class: class defining character class
    """
    if str.lower(class_name) == "warrior":
        return Warrior
    if str.lower(class_name) == "ranger":
        return Ranger
    if str.lower(class_name) == "mage":
        return Mage
    return None


def string_to_character_race(race_name: str):
    """
        returns class (not object) defining particular character race given its name
        :param race_name: name of character class
        :return class: class defining character race
    """
    if str.lower(race_name) == "human":
        return Human
    if str.lower(race_name) == "elf":
        return Elf
    if str.lower(race_name) == "dwarf":
        return Dwarf
    return None
>>>>>>> staging
