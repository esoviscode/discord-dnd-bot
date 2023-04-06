import copy
import json
import random
import cv2 as cv

from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.creatures.frost_mage import FrostMage
from dnd_bot.logic.prototype.entities.creatures.half_dragon_assassin import HalfDragonAssassin
from dnd_bot.logic.prototype.entities.creatures.half_dragon_warrior import HalfDragonWarrior
from dnd_bot.logic.prototype.entities.creatures.lizardfolk_archer import LizardfolkArcher
from dnd_bot.logic.prototype.entities.creatures.nothic import Nothic
from dnd_bot.logic.prototype.entities.creatures.skeleton_morningstar import SkeletonMorningstar
from dnd_bot.logic.prototype.entities.creatures.skeleton_warrior import SkeletonWarrior
from dnd_bot.logic.prototype.entities.hole import Hole
from dnd_bot.logic.prototype.entities.misc.dead_body import DeadBody
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
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.items.bow import Bow
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.items.staff import Staff
from dnd_bot.logic.prototype.items.sword import Sword
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.utils import get_game_view


class InitializeWorld:
    entity_classes_by_name: dict = {
        'Rock': Rock,
        'Hole': Hole,
        'Mushrooms': Mushrooms,
        'Frost mage': FrostMage,
        'Half dragon assassin': HalfDragonAssassin,
        'Half dragon warrior': HalfDragonWarrior,
        'Lizardfolk archer': LizardfolkArcher,
        'Nothic': Nothic,
        'Skeleton morningstar': SkeletonMorningstar,
        'Skeleton warrior': SkeletonWarrior,
        'Dungeon connector': DungeonConnector,
        'Dungeon corner in': DungeonCornerIn,
        'Dungeon corner out': DungeonCornerOut,
        'Dungeon crossroads': DungeonCrossroads,
        'Dungeon pillar A': DungeonPillarA,
        'Dungeon pillar B': DungeonPillarB,
        'Dungeon pillar C': DungeonPillarC,
        'Dungeon straight A': DungeonStraightA,
        'Dungeon straight B': DungeonStraightB,
    }

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
                    if str(entity) not in entity_types:
                        entities_row.append(None)

                    elif entity_types[str(entity)] == 'Player':
                        player_spawning_points.append((x, y))
                        entities_row.append(None)
                    else:
                        entities_row = InitializeWorld.add_entity(entities_row, InitializeWorld.entity_classes_by_name[
                            entity_types[str(entity)]], x, y, game.token, game.id)

                entities.append(entities_row)

        game.entities = copy.deepcopy(entities)
        InitializeWorld.load_entity_rotations(game, map_path)
        InitializeWorld.spawn_players(game, player_spawning_points)

        game.sprite = str(map_json['map']['img_file'])  # path to raw map image
        # generated image of map without fragile entities
        game.sprite = cv.imread(get_game_view(game), cv.IMREAD_UNCHANGED)
        game.world_width = map_json['map']['size']['x']
        game.world_height = map_json['map']['size']['y']

    @staticmethod
    def load_entity_rotations(game, map_path):
        """
        loads initial entity rotations from json
        """
        with open(map_path) as file:
            map_json = json.load(file)

            for y, row in enumerate(map_json['map']['entities_rotation']):
                for x, entity_rotation in enumerate(row):
                    if game.entities[y][x] is not None:
                        if entity_rotation == 0:
                            game.entities[y][x].look_direction = 'down'
                        elif entity_rotation == 1:
                            game.entities[y][x].look_direction = 'left'
                        elif entity_rotation == 2:
                            game.entities[y][x].look_direction = 'up'
                        elif entity_rotation == 3:
                            game.entities[y][x].look_direction = 'right'
                        else:
                            game.entities[y][x].look_direction = 'down'

    @staticmethod
    def spawn_players(game, player_spawning_spots):
        """
        function spawns players in some spawning spots randomly
        """
        players_positions = InitializeWorld.spawn_players_positions(player_spawning_spots, len(game.user_list))
        for i, player_pos in enumerate(players_positions):
            game.entities[player_pos[1]].pop(player_pos[0])
            if game.user_list[i].discord_id in ChosenAttributes.chosen_attributes:
                character = ChosenAttributes.chosen_attributes[game.user_list[i].discord_id]
                entities = InitializeWorld.add_player(x=player_pos[0], y=player_pos[1],
                                                      name=character['name'],
                                                      discord_identity=game.user_list[i].discord_id,
                                                      game_token=game.token,
                                                      entities=game.entities,
                                                      game_id=game.id,
                                                      backstory=character['backstory'],
                                                      alignment='-'.join(character['alignment']),
                                                      hp=character['hp'],
                                                      strength=character['strength'],
                                                      dexterity=character['dexterity'],
                                                      intelligence=character['intelligence'],
                                                      charisma=character['charisma'],
                                                      perception=character['perception'],
                                                      initiative=character['initiative'],
                                                      action_points=character['action points'],
                                                      character_race=character['race'],
                                                      character_class=character['class'])
                ChosenAttributes.delete_user(game.user_list[i].discord_id)
            else:
                entities = InitializeWorld.add_player(x=player_pos[0], y=player_pos[1],
                                                      name=game.user_list[i].username,
                                                      discord_identity=game.user_list[i].discord_id,
                                                      game_token=game.token,
                                                      entities=game.entities,
                                                      game_id=game.id,
                                                      backstory='fascinating backstory',
                                                      alignment='chaotic-evil',
                                                      hp=random.randint(15, 30),
                                                      strength=random.randint(1, 5),
                                                      dexterity=random.randint(1, 5),
                                                      intelligence=random.randint(1, 5),
                                                      charisma=random.randint(1, 5),
                                                      perception=random.randint(2, 4),
                                                      initiative=random.randint(1, 5),
                                                      action_points=100,
                                                      character_race=random.choice(['Human', 'Elf', 'Dwarf']),
                                                      character_class=random.choice(['Warrior', 'Mage', 'Ranger']))

    @staticmethod
    def spawn_players_positions(spawning_points, num_players):
        """function that returns random available spawning points that players can spawn in"""
        players_positions = []
        for _ in range(num_players):
            x, y = spawning_points.pop(random.randint(0, len(spawning_points) - 1))
            players_positions.append((x, y))

        return players_positions

    @staticmethod
    def add_entity(entity_row, entity_class, x, y, game_token, game_id):
        """adds entity of class to entity matrix in game
        :param entity_row: representing row of entity matrix
        :param entity_class: class of entity to be added
        :param x: entity x position
        :param x: entity y position
        """

        if issubclass(entity_class, Creature):  # add a creature
            entity_row = InitializeWorld.add_creature(entity_row, entity_class, x, y, game_token, game_id,
                                                      entity_class.creature_name)
            return entity_row

        entity = entity_class(x=x, y=y, game_token=game_token, name=entity_class.entity_name,
                              sprite=entity_class.sprite_path)
        id_entity = DatabaseEntity.add_entity(name=entity_class.entity_name, x=x, y=y, id_game=game_id)
        entity.id = id_entity
        entity_row.append(entity)
        return entity_row

    @staticmethod
    def add_creature(entity_row, creature_class, x, y, game_token, game_id, entity_name):
        entity = creature_class(x=x, y=y, game_token=game_token, action_points=2, sprite=creature_class.sprite_path,
                                name=creature_class.creature_name, hp=20)
        id_entity = DatabaseEntity.add_entity(name=entity_name, x=x, y=y, id_game=game_id)
        entity.id = id_entity
        entity_row.append(entity)
        return entity_row

    @staticmethod
    def add_player(x: int = 0, y: int = 0, name: str = '', discord_identity: int = 0, game_token: str = '',
                   game_id: int = 0, entities=None, backstory: str = '', alignment: str = '', hp: int = 0,
                   strength: int = 0, dexterity: int = 0, intelligence: int = 0, charisma: int = 0,
                   perception: int = 0, initiative: int = 0, action_points: int = 0,
                   character_race: str = '', character_class: str = '') -> int | None:

        p = Player(x=x, y=y, name=name, discord_identity=discord_identity, game_token=game_token, backstory=backstory,
                   alignment=alignment, hp=hp, strength=strength, dexterity=dexterity, intelligence=intelligence,
                   charisma=charisma, perception=perception, initiative=initiative, action_points=action_points,
                   character_race=character_race, character_class=character_class)
        id_player = DatabasePlayer.add_player(p.x, p.y, p.name, p.hp, p.strength, p.dexterity,
                                              p.intelligence, p.charisma, p.perception, p.initiative,
                                              p.action_points, p.level, p.discord_identity, p.alignment,
                                              p.backstory, id_game=game_id, character_race=p.character_race,
                                              character_class=p.creature_class)  # TODO add race and class
        p.id = id_player

        # TODO change location of adding equipment/items
        if p.creature_class == 'Warrior':
            p.equipment = Equipment(right_hand=Sword(name='Novice sword'), accessory=Item(name='Holy Bible'))
        elif p.creature_class == 'Mage':
            p.equipment = Equipment(right_hand=Staff(name='Novice staff'), accessory=Item(name='Necklace of prudence'))
        elif p.creature_class == 'Ranger':
            p.equipment = Equipment(right_hand=Bow(name='Novice bow'), accessory=Item(name='Hunting necklace'))

        entities[y].insert(x, p)
        return entities
