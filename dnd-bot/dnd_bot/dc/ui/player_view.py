import copy
import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game


def paste_image(src, dest, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + src.shape[0]
    x1, x2 = x_offset, x_offset + src.shape[1]

    alpha_src = src[:, :, 3] / 255.0
    alpha_dest = 1.0 - alpha_src

    for c in range(0, 3):
        dest[y1:y2, x1:x2, c] = (alpha_src * src[:, :, c] + alpha_dest * dest[y1:y2, x1:x2, c])


def get_player_view(game: Game):
    view_range = 3
    map_margin = 100
    square_size = 50
    whole_map = copy.deepcopy(game.sprite)

    e1 = cv.getTickCount()
    entities = [e for e in sum(game.entities, []) if e]
    for i, entity in enumerate(entities):
        # print(i)
        paste_image(entity.sprite, whole_map, map_margin + entity.x * square_size, map_margin + entity.y * square_size)

        # whole_map[map_margin + y * square_size:map_margin + (y + 1) * square_size,
        # map_margin + x * square_size:map_margin + (x + 1) * square_size] = game.entities[y][x].sprite

    e2 = cv.getTickCount()
    t = (e2 - e1) / cv.getTickFrequency()
    print(f"image processing time: {t} s")

    # pov = np.zeros(((view_range * 2 - 1) * square_size, (view_range * 2 - 1) * square_size, 4), np.uint8)
    cv.imwrite("dnd_bot/dc/ui/game_images/pov.png", whole_map)
    del whole_map

    return "dnd_bot/dc/ui/game_images/pov.png"
