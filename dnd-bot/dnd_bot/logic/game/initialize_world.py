import copy
import json
import random
import cv2 as cv

from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_player import DatabasePlayer
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
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.items.bow import Bow
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.items.staff import Staff
from dnd_bot.logic.prototype.items.sword import Sword
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
                    elif entity_types[str(entity)] == Rock.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, Rock, x, y, game.token, game.id)
                    elif entity_types[str(entity)] == Hole.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, Hole, x, y, game.token, game.id)
                    elif entity_types[str(entity)] == Mushrooms.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, Mushrooms, x, y, game.token, game.id,)
                    elif entity_types[str(entity)] == FrostMage.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, FrostMage, x, y, game.token, game.id,
                                                                  entity_types[str(entity)])
                    elif entity_types[str(entity)] == HalfDragonAssassin.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, HalfDragonAssassin, x, y, game.token, game.id,
                                                                  entity_types[str(entity)])
                    elif entity_types[str(entity)] == HalfDragonWarrior.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, HalfDragonWarrior, x, y, game.token, game.id,
                                       entity_types[str(entity)])
                    elif entity_types[str(entity)] == LizardfolkArcher.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, LizardfolkArcher, x, y, game.token, game.id,
                                       entity_types[str(entity)])
                    elif entity_types[str(entity)] == Nothic.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, Nothic, x, y, game.token, game.id,
                                       entity_types[str(entity)])
                    elif entity_types[str(entity)] == SkeletonMorningstar.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, SkeletonMorningstar, x, y, game.token, game.id,
                                       entity_types[str(entity)])
                    elif entity_types[str(entity)] == SkeletonWarrior.creature_name:
                        entities_row = InitializeWorld.add_creature(entities_row, SkeletonWarrior, x, y, game.token, game.id,
                                       entity_types[str(entity)])

                    # walls
                    elif entity_types[str(entity)] == DungeonConnector.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonConnector, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonCornerIn.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCornerIn, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonCornerOut.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCornerOut, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonCrossroads.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonCrossroads, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonPillarA.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarA, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonPillarB.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarB, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonPillarC.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonPillarC, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonStraightA.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonStraightA, x, y, game.token,
                                                                  game.id)
                    elif entity_types[str(entity)] == DungeonStraightB.entity_name:
                        entities_row = InitializeWorld.add_entity(entities_row, DungeonStraightB, x, y, game.token,
                                                                  game.id)
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
                if game.user_list[i].discord_id in ChosenAttributes.chosen_attributes:
                    character = ChosenAttributes.chosen_attributes[game.user_list[i].discord_id]
                    entities = InitializeWorld.add_player(x=player_pos[0], y=player_pos[1],
                                                          name=character['name'],
                                                          discord_identity=game.user_list[i].discord_id,
                                                          game_token=game.token,
                                                          entities=entities,
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
                                                          entities=entities,
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
    def add_entity(entity_row, entity_class, x, y, game_token, game_id):
        entity = entity_class(x=x, y=y, game_token=game_token, name=entity_class.entity_name, sprite=entity_class.sprite_path)
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
        if p.character_class == 'Warrior':
            p.equipment = Equipment(right_hand=Sword(name='Novice sword'), accessory=Item(name='Holy Bible'))
        elif p.character_class == 'Mage':
            p.equipment = Equipment(right_hand=Staff(name='Novice staff'), accessory=Item(name='Necklace of prudence'))
        elif p.character_class == 'Ranger':
            p.equipment = Equipment(right_hand=Bow(name='Novice bow'), accessory=Item(name='Hunting necklace'))

        entities[y].insert(x, p)
        return entities
