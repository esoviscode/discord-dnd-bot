import asyncio
import copy
import json
import random
import time

import cv2 as cv

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_equipment import DatabaseEquipment
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.creatures.enemy import Enemy
from dnd_bot.logic.prototype.entities.creatures.npc import NPC
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.utils import get_game_view


class InitializeWorld:

    @staticmethod
    def load_entities(game, map_path, campaign_path):
        """loads entities from json, players will be placed in random available spawning spots"""

        print("\n-- Initializing world --")
        time_snapshot = time.time()
        map_json, entities, player_spawning_points = InitializeWorld.load_entities_from_json(game, map_path,
                                                                                             campaign_path)
        game.entities = copy.deepcopy(entities)
        print(f'   - loading entities from json - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        time_snapshot = time.time()
        InitializeWorld.load_entity_rotations(game, map_path)
        print(f'   - loading entity rotations - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        time_snapshot = time.time()
        InitializeWorld.spawn_players(game, player_spawning_points)
        print(f'   - spawning players - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        InitializeWorld.load_map_information(game, map_path)

    @staticmethod
    def load_map_information(game, map_path):
        with open(map_path) as file:
            map_json = json.load(file)
            game.sprite = str(map_json['map']['img_file'])  # path to raw map image
            # generated image of map without fragile entities
            game.sprite = cv.imread(get_game_view(game), cv.IMREAD_UNCHANGED)
            game.world_width = map_json['map']['size']['x']
            game.world_height = map_json['map']['size']['y']

    @staticmethod
    def load_entities_from_json(game, map_path, campaign_path):
        with open(map_path) as file:
            map_json = json.load(file)
            entities_json = map_json['map']['entities']

            # load entity types dict
            entity_types = map_json['entity_types']

        with open(campaign_path) as file:
            campaign_json = json.load(file)
            enemies_json = campaign_json['entities']['enemies']
            npc_json = campaign_json['entities']['npc']
            map_elements_json = campaign_json['entities']['map_elements']

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
                        entities_row = InitializeWorld.add_entity(entities_row, entity_types[str(entity)], x, y,
                                                                  game.token, game.id, enemies_json, npc_json,
                                                                  map_elements_json)

                entities.append(entities_row)

        return map_json, entities, player_spawning_points

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
            if (game.user_list[i].discord_id, game.token) in ChosenAttributes.chosen_attributes:
                character = ChosenAttributes.chosen_attributes[game.user_list[i].discord_id, game.token]
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
                ChosenAttributes.delete_user(game.user_list[i].discord_id, game.token)
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
    def add_entity(entity_row, entity_name, x, y, game_token, game_id, enemies_json, npc_json, map_elements_json):
        """adds entity of class to entity matrix in game
        :param entity_row: representing row of entity matrix
        :param entity_name: name of entity to be added
        :param x: entity x position
        :param y: entity y position
        :param map_elements_json: data of map elements
        :param enemies_json: data of enemies
        :param npc_json: data of npc
        :param game_id: id from database
        :param game_token: game token
        """

        if entity_name in enemies_json:
            entity_row = InitializeWorld.add_creature(entity_row, x, y, entity_name, game_token, game_id,
                                                      enemies_json[entity_name], "Enemy")
            return entity_row
        if entity_name in npc_json:
            entity_row = InitializeWorld.add_creature(entity_row, x, y, entity_name, game_token, game_id,
                                                      npc_json[entity_name], "NPC")
            return entity_row

        entity = Entity(x=x, y=y, sprite=map_elements_json[entity_name], name=entity_name, game_token=game_token)

        entity_row.append(entity)
        return entity_row

    @staticmethod
    def add_creature(entity_row, x, y, name, game_token, game_id, entity_data, creature_type="Creature"):
        creature = eval(creature_type)(game_token=game_token, x=x, y=y, sprite=entity_data['sprite_path'], name=name,
                                       hp=entity_data['hp'],
                                       strength=entity_data['strength'], dexterity=entity_data['dexterity'],
                                       intelligence=entity_data['intelligence'],
                                       charisma=entity_data['charisma'], perception=entity_data['perception'],
                                       initiative=entity_data['initiative'],
                                       action_points=entity_data['action_points'], level=entity_data['level'],
                                       drop_money=entity_data['drop_money'], drops=entity_data['drops'],
                                       creature_class=entity_data['creature_class'], ai=entity_data['ai'])

        creature.equipment = Equipment()
        for eq_part in entity_data['equipment']:
            creature.equipment.__setattr__(eq_part, Item(name=entity_data['equipment'][eq_part]))
        entity_row.append(creature)

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

        # TODO change location of adding equipment/items
        if p.creature_class == 'Warrior':
            p.equipment = Equipment(right_hand=Item(name='Novice sword'), accessory=Item(name='Holy Bible'))
        elif p.creature_class == 'Mage':
            p.equipment = Equipment(right_hand=Item(name='Novice staff'), accessory=Item(name='Necklace of prudence'))
        elif p.creature_class == 'Ranger':
            p.equipment = Equipment(right_hand=Item(name='Novice bow'), accessory=Item(name='Hunting necklace'))

        id_player = DatabasePlayer.add_player(p.x, p.y, p.name, p.hp, p.base_strength, p.base_dexterity,
                                              p.base_intelligence, p.base_charisma, p.base_perception, p.initiative,
                                              p.action_points, p.level, p.discord_identity, p.alignment,
                                              p.backstory, id_game=game_id, character_race=p.character_race,
                                              character_class=p.creature_class, id_equipment=p.equipment.id,
                                              max_hp=p.max_hp, initial_action_points=p.initial_action_points)
        p.id = id_player

        entities[y].insert(x, p)
        return entities

    @staticmethod
    def add_equipment(helmet: Item = None, chest: Item = None, leg_armor: Item = None, boots: Item = None,
                      left_hand: Item = None, right_hand: Item = None, accessory: Item = None) -> Equipment:
        """adds equipment to database and returns id_equipment"""
        e = Equipment()
        if helmet is not None:
            helmet_id = helmet.id = InitializeWorld.add_item(helmet)
            e.helmet = helmet
        else:
            helmet_id = None
        if chest is not None:
            chest_id = chest.id = InitializeWorld.add_item(chest)
            e.chest = chest
        else:
            chest_id = None
        if leg_armor is not None:
            leg_armor_id = leg_armor.id = InitializeWorld.add_item(leg_armor)
            e.leg_armor = leg_armor
        else:
            leg_armor_id = None
        if boots is not None:
            boots_id = boots.id = InitializeWorld.add_item(boots)
            e.boots = boots
        else:
            boots_id = None
        if left_hand is not None:
            left_hand_id = left_hand.id = InitializeWorld.add_item(left_hand)
            e.left_hand = left_hand
        else:
            left_hand_id = None
        if right_hand is not None:
            right_hand_id = right_hand.id = InitializeWorld.add_item(right_hand)
            e.right_hand = right_hand
        else:
            right_hand_id = None
        if accessory is not None:
            accessory_id = accessory.id = InitializeWorld.add_item(accessory)
            e.accessory = accessory
        else:
            accessory_id = None

        e.id = DatabaseEquipment.add_equipment(helmet=helmet_id, chest=chest_id, leg_armor=leg_armor_id, boots=boots_id,
                                               left_hand=left_hand_id, right_hand=right_hand_id, accessory=accessory_id)
        return e

    @staticmethod
    def add_item(i: Item) -> int:
        """adds item to database and returns its id_item"""
        return DatabaseItem.add_item(name=i.name)

    @staticmethod
    async def add_entities_to_database(game):
        async def add_row_entities_to_database(row):
            queries = []
            parameters_list = []

            # add entities
            entities_in_row = [e for e in row if isinstance(e, Entity) and not isinstance(e, Player)]
            for entity in entities_in_row:
                query, parameters = DatabaseEntity.add_entity_query(name=entity.name, x=entity.x, y=entity.y,
                                                                    id_game=game.id)
                queries.append(query)
                parameters_list.append(parameters)

            entity_ids = DatabaseConnection.add_multiple_to_db(queries, parameters_list)

            for entity, entity_id in zip(entities_in_row, entity_ids):
                entity.id = entity_id

            queries.clear()
            parameters_list.clear()
            # add creatures
            creatures_in_row = [c for c in entities_in_row if isinstance(c, Creature) and not isinstance(c, Player)]
            for creature in creatures_in_row:
                query, parameters = DatabaseCreature.add_creature_query(name=creature.name, x=creature.x, y=creature.y,
                                                                        hp=creature.hp, strength=creature.strength,
                                                                        dexterity=creature.dexterity,
                                                                        intelligence=creature.intelligence,
                                                                        charisma=creature.charisma,
                                                                        perception=creature.perception,
                                                                        initiative=creature.initiative,
                                                                        action_points=creature.action_points,
                                                                        level=creature.level, id_game=game.id,
                                                                        experience=creature.experience,
                                                                        id_entity=creature.id, max_hp=creature.max_hp,
                                                                        initial_action_points=creature.initial_action_points)
                queries.append(query)
                parameters_list.append(parameters)

            creature_ids = DatabaseConnection.add_multiple_to_db(queries, parameters_list)

            for creature, creature_id in zip(creatures_in_row, creature_ids):
                creature.id = creature_id

        # add rows in parallel
        q = asyncio.Queue()
        tasks = [asyncio.create_task(add_row_entities_to_database(row)) for row in game.entities]
        await asyncio.gather(*tasks)
        await q.join()
