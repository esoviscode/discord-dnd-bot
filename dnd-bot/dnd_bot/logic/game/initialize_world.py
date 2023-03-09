import copy
import json
import random
import cv2 as cv

from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.logic.prototype.creature import Creature
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
                        entities_row = InitializeWorld.add_entity(entities_row, Rock, x, y, game.token, game.id, 'Rock')
                    elif entity_types[str(entity)] == 'Hole':
                        entities_row = InitializeWorld.add_entity(entities_row, Hole, x, y, game.token, game.id, 'Hole')
                    elif entity_types[str(entity)] == 'Mushrooms':
                        entities_row = InitializeWorld.add_entity(entities_row, Mushrooms, x, y, game.token, game.id,
                                                                  'Mushrooms')

                    # walls
                    elif entity_types[str(entity)] == 'Dungeon connector':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonConnector, x, y, game.token,
                                                                  game.id, 'Dungeon connector')
                    elif entity_types[str(entity)] == 'Dungeon corner in':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCornerIn, x, y, game.token,
                                                                  game.id, 'Dungeon corner in')
                    elif entity_types[str(entity)] == 'Dungeon corner out':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCornerOut, x, y, game.token,
                                                                  game.id, 'Dungeon corner out')
                    elif entity_types[str(entity)] == 'Dungeon crossroads':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCrossroads, x, y, game.token,
                                                                  game.id, 'Dungeon crossroads')
                    elif entity_types[str(entity)] == 'Dungeon pillar A':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarA, x, y, game.token,
                                                                  game.id, 'Dungeon pillar A')
                    elif entity_types[str(entity)] == 'Dungeon pillar B':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarB, x, y, game.token,
                                                                  game.id, 'Dungeon pillar B')
                    elif entity_types[str(entity)] == 'Dungeon pillar C':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarC, x, y, game.token,
                                                                  game.id, 'Dungeon pillar C')
                    elif entity_types[str(entity)] == 'Dungeon straight A':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonStraightA, x, y, game.token,
                                                                  game.id, 'Dungeon straight A')
                    elif entity_types[str(entity)] == 'Dungeon straight B':
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonStraightB, x, y, game.token,
                                                                  game.id, 'Dungeon straight B')
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
            players_positions = InitializeWorld.spawn_players_positions(player_spawning_points, len(game.user_list))
            for i, player_pos in enumerate(players_positions):
                entities[player_pos[1]].pop(player_pos[0])
                player = Player(x=player_pos[0], y=player_pos[1],
                                name=game.user_list[i].username,
                                discord_identity=game.user_list[i].discord_id,
                                game_token=game.token)
                player.id_game = game.id
                DatabasePlayer.add_player(player)
                entities[player_pos[1]].insert(player_pos[0], player)

            game.entities = copy.deepcopy(entities)
            game.sprite = str(map_json['map']['img_file'])  # path to raw map image
            # generated image of map with not fragile entities
            game.sprite = cv.imread(get_game_view(game), cv.IMREAD_UNCHANGED)
            game.world_width = map_json['map']['size']['x']
            game.world_height = map_json['map']['size']['y']

    @staticmethod
    def spawn_players_positions(spawning_points, num_players):
        """function that returns random available spawning points that players can spawn in"""
        players_positions = []
        for _ in range(num_players):
            x, y = spawning_points.pop(random.randint(0, len(spawning_points) - 1))
            players_positions.append((x, y))

        return players_positions

    @staticmethod
    def add_entity(entity_row, entity_class, x, y, game_token, game_id, entity_name):
        new_entity = entity_class(x=x, y=y, game_token=game_token)

        if isinstance(entity_class, Creature):
            DatabaseCreature.add_creature(new_entity)
        else:
            id_entity = DatabaseEntity.add_entity(entity_name, x, y, id_game=game_id)
            new_entity.id = id_entity
        entity_row.append(new_entity)
        return entity_row
