import copy
import json
import random
import cv2 as cv

from dnd_bot.logic.prototype.entities.creatures.frost_mage import FrostMage
from dnd_bot.logic.prototype.entities.creatures.half_dragon_assassin import HalfDragonAssassin
from dnd_bot.logic.prototype.entities.creatures.half_dragon_warrior import HalfDragonWarrior
from dnd_bot.logic.prototype.entities.creatures.lizardfolk_archer import LizardfolkArcher
from dnd_bot.logic.prototype.entities.creatures.nothic import Nothic
from dnd_bot.logic.prototype.entities.creatures.skeleton_morningstar import SkeletonMorningstar
from dnd_bot.logic.prototype.entities.creatures.skeleton_warrior import SkeletonWarrior
from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.rock import Rock
from dnd_bot.logic.prototype.entities.mushrooms import Mushrooms
from dnd_bot.logic.prototype.entities.walls.dungeon_connector import DungeonConnector
from dnd_bot.logic.prototype.entities.walls.dungeon_corner_in import DungeonCornerIn
from dnd_bot.logic.prototype.entities.walls.dungeon_corner_out import DungeonCornerOut
from dnd_bot.logic.prototype.entities.walls.dungeon_crossroads import DungeonCrossroads
from dnd_bot.logic.prototype.entities.walls.dungeon_pillar_a import DungeonPillarA
from dnd_bot.logic.prototype.entities.walls.dungeon_pillar_b import DungeonPillarB
from dnd_bot.logic.prototype.entities.walls.dungeon_pillar_c import DungeonPillarC
from dnd_bot.logic.prototype.entities.walls.dungeon_straight_a import DungeonStraightA
from dnd_bot.logic.prototype.entities.walls.dungeon_straight_b import DungeonStraightB
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
                    elif entity_types[str(entity)] == 'Frost mage':
                        entities_row.append(FrostMage(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Half dragon assassin':
                        entities_row.append(HalfDragonAssassin(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Half dragon warrior':
                        entities_row.append(HalfDragonWarrior(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Lizardfolk archer':
                        entities_row.append(LizardfolkArcher(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Nothic':
                        entities_row.append(Nothic(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Skeleton morningstar':
                        entities_row.append(SkeletonMorningstar(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Skeleton warrior':
                        entities_row.append(SkeletonWarrior(x=x, y=y, game_token=game.token))

                    # walls
                    elif entity_types[str(entity)] == 'Dungeon connector':
                        entities_row.append(DungeonConnector(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon corner in':
                        entities_row.append(DungeonCornerIn(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon corner out':
                        entities_row.append(DungeonCornerOut(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon crossroads':
                        entities_row.append(DungeonCrossroads(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon pillar A':
                        entities_row.append(DungeonPillarA(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon pillar B':
                        entities_row.append(DungeonPillarB(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon pillar C':
                        entities_row.append(DungeonPillarC(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon straight A':
                        entities_row.append(DungeonStraightA(x=x, y=y, game_token=game.token))
                    elif entity_types[str(entity)] == 'Dungeon straight B':
                        entities_row.append(DungeonStraightB(x=x, y=y, game_token=game.token))
                entities.append(entities_row)

            # handle entity rotations
            for y, row in enumerate(map_json['map']['entities_rotation']):
                for x, entity_rotation in enumerate(row):
                    if entities[y][x] is not None:
                        if entity_rotation == 0:
                            entities[y][x].look_direction = 'down'
                        elif entity_rotation == 1:
                            entities[y][x].look_direction = 'left'
                        elif entity_rotation == 2:
                            entities[y][x].look_direction = 'up'
                        elif entity_rotation == 3:
                            entities[y][x].look_direction = 'right'
                        else:
                            entities[y][x].look_direction = 'down'

            # handle random spawning points
            players_positions = InitializeWorld.spawn_players(player_spawning_points, len(game.user_list))
            for i, player_pos in enumerate(players_positions):
                print(f'spawning player at {player_pos}')
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
