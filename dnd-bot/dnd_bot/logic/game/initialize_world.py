import copy
import json
import random
import cv2 as cv

from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.entities.mushrooms import Mushrooms
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.utils import get_game_view


class InitializeWorld:

    @staticmethod
    def load_entities(game, map_path):
        """loads entities from json, players will be placed in random available spawning spots"""
        with open(map_path) as file:
            map_json = json.load(file)
            entities_json = map_json['map']['entities']

            # load entity types dict
            entity_types = map_json['entity_types']

            map_size_x = map_json['map']['size']['x']
            map_size_y = map_json['map']['size']['y']

            entities = []
            player_spawning_points = []
            for y, row in enumerate(entities_json):
                entities_row = []
                for x, entity in enumerate(row):
                    if str(entity) not in entity_types.keys():
                        entities_row.append(None)

                    elif entity_types[str(entity)] == 'Player':
                        player_spawning_points.append((x, y))
                        entities_row.append(None)
                    elif entity_types[str(entity)] == 'Rock':
                        entities_row.append(Rock(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Hole':
                        entities_row.append(Hole(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Mushrooms':
                        entities_row.append(Mushrooms(x=x, y=y, game_token=game.token))
                entities.append(entities_row)

            # handle random spawning points
            players_positions = InitializeWorld.spawn_players(player_spawning_points, len(game.user_list))
            for i, player_pos in enumerate(players_positions):
                entities[player_pos[1]].pop(player_pos[0])
                entities[player_pos[1]].insert(player_pos[0], Player(x=player_pos[0], y=player_pos[1],
                                                                     name=game.user_list[i].username,
                                                                     discord_identity=game.user_list[i].discord_id,
                                                                     game_token=game.token))

            game.entities = copy.deepcopy(entities)
            game.sprite = str(map_json['map']['img_file'])  # path to raw map image
            # generated image of map with not fragile entities
            game.sprite = cv.imread(get_game_view(game), cv.IMREAD_UNCHANGED)

    @staticmethod
    def spawn_players(spawning_points, num_players):
        """function that places players in random available spawning points"""
        players_positions = []
        for _ in range(num_players):
            x, y = spawning_points.pop(random.randint(0, len(spawning_points) - 1))
            players_positions.append((x, y))

        return players_positions
