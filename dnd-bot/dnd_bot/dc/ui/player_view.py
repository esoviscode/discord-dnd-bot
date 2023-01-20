import copy

import cv2 as cv
import numpy as np

from dnd_bot.logic.prototype.game import Game


square_size = 50


def paste_image(src, dest, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + square_size
    x1, x2 = x_offset, x_offset + square_size

    alpha_src = src[:, :, 3] / 255
    alpha_dest = 1.0 - alpha_src

    for c in range(0, 3):
        dest[y1:y2, x1:x2, c] = (alpha_src * src[:, :, c] + alpha_dest * dest[y1:y2, x1:x2, c])


def get_player_view(game: Game):
    view_range = 3
    map_margin = 100
    whole_map = copy.deepcopy(game.sprite)

    e1 = cv.getTickCount()
    for y, row in enumerate(game.entities):
        for x, entity in enumerate(row):
            if entity:
                paste_image(entity.sprite, whole_map, map_margin + x * square_size, map_margin + y * square_size)

                # whole_map[map_margin + y * square_size:map_margin + (y + 1) * square_size,
                # map_margin + x * square_size:map_margin + (x + 1) * square_size] = game.entities[y][x].sprite

    e2 = cv.getTickCount()
    t = (e2 - e1) / cv.getTickFrequency()
    print("image processing time: {t} s")

    # pov = np.zeros(((view_range * 2 - 1) * square_size, (view_range * 2 - 1) * square_size, 4), np.uint8)
    cv.imwrite("dnd_bot/dc/ui/pov.png", whole_map)
    del whole_map

    return "dnd_bot/dc/ui/pov.png"
