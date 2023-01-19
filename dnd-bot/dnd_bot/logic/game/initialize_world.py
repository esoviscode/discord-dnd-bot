import copy
import json
import random

from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.player import Player


class InitializeWorld:

    @staticmethod
    def load_entities(game, path):
        with open(path) as file:
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

                    elif entity_types[str(entity)] == 'Rock':
                        entities_row.append(Rock(x=x, y=y))
                    elif entity_types[str(entity)] == 'Hole':
                        entities_row.append(Hole(x=x, y=y))
                    elif entity_types[str(entity)] == 'Player':
                        player_spawning_points.append((x, y))
                        entities_row.append(None)
                entities.append(entities_row)

            # handle random spawning points
            players_positions = InitializeWorld.spawn_players(player_spawning_points, len(game.user_list))
            for i, player_pos in enumerate(players_positions):
                entities[player_pos[1]].pop(player_pos[0])
                entities[player_pos[1]].insert(player_pos[0], Player(x=player_pos[0], y=player_pos[1], name=game.user_list[i].username,
                                                                     discord_identity=game.user_list[i].discord_id))

            game.entities = copy.deepcopy(entities)

    @staticmethod
    def spawn_players(spawning_points, num_players):
        players_positions = []
        for _ in range(num_players):
            x, y = spawning_points.pop(random.randint(0, len(spawning_points) - 1))
            players_positions.append((x, y))

        return players_positions
