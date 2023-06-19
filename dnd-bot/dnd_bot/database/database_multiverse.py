import copy
import json
import time
from typing import List

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_equipment import DatabaseEquipment
from dnd_bot.database.database_event import DatabaseEvent
from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_item import DatabaseItem
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.logic.game.initialize_world import InitializeWorld
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.creatures.enemy import Enemy
from dnd_bot.logic.prototype.entities.creatures.npc import NPC
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.event import Event
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.user import User
from dnd_bot.logic.utils.exceptions import GameException, DiscordDndBotException
from dnd_bot.logic.prototype.player import Player


class DatabaseMultiverse:

    @staticmethod
    def update_game_state(token):
        """
        driver method that handles saving all elements of a game to the database
        :param token: game token
        """
        game: Game = Multiverse.get_game(token)
        if not game:
            raise GameException('Game with provided token doesn\'t exist!')

        print("\n-- Updating db game state --")

        DatabaseGame.update_game_state(DatabaseGame.get_id_game_from_game_token(token), game.game_state)

        time_snapshot = time.time()
        DatabaseMultiverse.__update_game_entities(game.entities)
        print(f'   - saving entities - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        time_snapshot = time.time()
        DatabaseMultiverse.__update_game_events(game.events)
        print(f'   - saving events - {round((time.time() - time_snapshot) * 1000, 2)} ms')

    @staticmethod
    def __update_game_entities(entities: List[List[Entity]]):
        queries = []
        parameters_list = []
        for entities_row in entities:
            for e in entities_row:
                if e is None:
                    continue

                if isinstance(e, Creature):
                    DatabaseMultiverse.__add_query_update_entity(e, queries, parameters_list)
                    DatabaseMultiverse.__add_query_update_creature(e, queries, parameters_list)
                    continue

                if isinstance(e, Entity) and e.fragile:
                    DatabaseMultiverse.__add_query_update_entity(e, queries, parameters_list)
                    continue

        DatabaseConnection.update_multiple_objects_in_db(queries, parameters_list)

    @staticmethod
    def __add_query_update_entity(entity: Entity, queries: List[str], parameters_list: List[tuple]) -> None:
        entity_id = entity.id
        if isinstance(entity, Creature):
            entity_id = DatabaseCreature.get_creature_id_entity(entity.id)
        if isinstance(entity, Player):
            creature_id = DatabasePlayer.get_players_id_creature(entity.id)
            entity_id = DatabaseCreature.get_creature_id_entity(creature_id)

        query, parameters = DatabaseEntity.update_entity_query(id_entity=entity_id,
                                                               x=entity.x, y=entity.y)
        queries.append(query)
        parameters_list.append(parameters)

    @staticmethod
    def __add_query_update_creature(creature: Creature, queries: List[str], parameters_list: List[tuple]) -> None:
        query, parameters = DatabaseCreature.update_creature_query(id_creature=creature.id, hp=creature.hp,
                                                                   level=creature.level, money=creature.money,
                                                                   experience=creature.experience,
                                                                   x=creature.x, y=creature.y)
        queries.append(query)
        parameters_list.append(parameters)

    @staticmethod
    def __update_game_events(events: List[Event]):
        BATCH_SIZE = 100  # how many events should be saved during one transaction

        events_batches = [events[i::BATCH_SIZE] for i in range(BATCH_SIZE)]

        for batch in events_batches:
            event_ids = [ev.id for ev in batch]
            event_statuses = [ev.status for ev in batch]

            DatabaseEvent.update_multiple_events(event_ids, event_statuses)

    @staticmethod
    async def load_game_state(token):
        """
        driver method that handles loading all game elements
        :param token: game token
        """

        print(f"\n-- Loading game state for game #{token} from db --")

        # create a new game object
        dbdict = DatabaseGame.get_game(DatabaseGame.get_id_game_from_game_token(token))
        game = Game(token=dbdict['token'], id_host=dbdict['id_host'], game_state=dbdict['game_state'],
                    campaign_name=dbdict['campaign_name'])
        print(f'game {game.id}, {game.game_state}, {game.id_host}, {game.token}')

        Multiverse.add_game(game)

        InitializeWorld.load_map_information(game, map_path='dnd_bot/assets/maps/map.json')

        time_snapshot = time.time()
        await DatabaseMultiverse.__load_game_state_user_list(game)
        print(f'   - loading users - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        print(f'game {game.token} users: {game.user_list}')

        time_snapshot = time.time()
        DatabaseMultiverse.__load_game_entities(game, 'dnd_bot/assets/campaigns/campaign.json')
        print(f'   - loading entities - {round((time.time() - time_snapshot) * 1000, 2)} ms')

    @staticmethod
    async def __load_game_state_user_list(game):
        user_list = DatabaseUser.get_all_users(game.id)
        for user_dict in user_list:
            username = await get_user_name_by_id(user_dict['discord_id'])
            user = User(game_token=game.token, discord_id=user_dict['discord_id'], username=username)

            if user_dict['discord_id'] == game.id_host:
                user.is_host = True

            game.user_list.append(user)

    @staticmethod
    def __load_game_entities(game, campaign_path):
        with open(campaign_path) as file:
            campaign_json = json.load(file)
            enemies_json = campaign_json['entities']['enemies']
            npc_json = campaign_json['entities']['npc']
            map_elements_json = campaign_json['entities']['map_elements']

        database_entities = DatabaseEntity.get_all_entities(game.id)

        # populate entities matrix with Nones
        for i in range(game.world_height):
            row = []
            for j in range(game.world_width):
                row.append(None)
            game.entities.append(row)

        for db_entity in database_entities:
            if db_entity['name'] in enemies_json:
                # enemy creature
                db_c = DatabaseCreature.get_creature_by_id_entity(db_entity['id_entity'])
                row = game.entities[db_entity['y']]
                DatabaseMultiverse.__load_creature(row, db_entity['x'], db_entity['y'], db_entity['name'], game.token,
                                                   db_c, enemies_json[db_entity['name']], "Enemy")
                continue

            if db_entity['name'] in npc_json:
                # npc creature
                db_c = DatabaseCreature.get_creature_by_id_entity(db_entity['id_entity'])
                row = game.entities[db_entity['y']]
                DatabaseMultiverse.__load_creature(row, db_entity['x'], db_entity['y'], db_entity['name'], game.token,
                                                   db_c, npc_json[db_entity['name']], "NPC")
                continue
            if db_entity['name'] in map_elements_json:
                # just an entity
                entity = Entity(id=db_entity['id_entity'], x=db_entity['x'], y=db_entity['y'],
                                sprite=map_elements_json[db_entity['name']], name=db_entity['name'],
                                game_token=game.token)  # TODO load look_direction
                row = game.entities[db_entity['y']]
                row[db_entity['x']] = copy.deepcopy(entity)

                continue

            # TODO the following code uses an assumption that any name not found in campaign json is a player - this
            #  might be wrong in the future, though

            db_c = DatabaseCreature.get_creature_by_id_entity(db_entity['id_entity'])
            db_p = DatabasePlayer.get_player_by_id_creature(db_c['id_creature'])
            db_user = DatabaseUser.get_user(db_p['id_user'])

            player = Player(x=db_entity['x'], y=db_entity['y'], name=db_entity['name'],
                            discord_identity=db_user['discord_id'],
                            game_token=game.token,
                            backstory=db_p['backstory'],
                            alignment=db_p['alignment'], hp=db_c['hp'], strength=db_c['strength'],
                            dexterity=db_c['dexterity'],
                            intelligence=db_c['intelligence'],
                            charisma=db_c['charisma'], perception=db_c['perception'], initiative=db_c['initiative'],
                            action_points=db_c['action_points'],
                            character_race=db_p['race'], character_class=db_c['class'], level=db_c['level'],
                            money=db_c['money'])
            player.id = db_p['id_player']

            equipment_db = DatabaseEquipment.get_equipment(db_c['id_equipment'])
            equipment = Equipment(helmet=Item(name=DatabaseItem.get_item(equipment_db['helmet'])['name']) if equipment_db['helmet'] else None,
                                  chest=Item(name=DatabaseItem.get_item(equipment_db['chest'])['name']) if equipment_db['chest'] else None,
                                  leg_armor=Item(name=DatabaseItem.get_item(equipment_db['leg_armor'])['name']) if equipment_db['leg_armor'] else None,
                                  boots=Item(name=DatabaseItem.get_item(equipment_db['boots'])['name']) if equipment_db['boots'] else None,
                                  left_hand=Item(name=DatabaseItem.get_item(equipment_db['left_hand'])['name']) if equipment_db['left_hand'] else None,
                                  right_hand=Item(name=DatabaseItem.get_item(equipment_db['right_hand'])['name']) if equipment_db['right_hand'] else None,
                                  accessory=Item(name=DatabaseItem.get_item(equipment_db['accessory'])['name']) if equipment_db['accessory'] else None)
            player.equipment = equipment

            row = game.entities[db_entity['y']]
            row[db_entity['x']] = copy.deepcopy(player)

    @staticmethod
    def __load_creature(entity_row, x, y, name, game_token, entity_data, json_data, creature_type="Creature"):
        creature = eval(creature_type)(game_token=game_token, x=x, y=y, sprite=json_data['sprite_path'], name=name,
                                       hp=entity_data['hp'],
                                       strength=entity_data['strength'], dexterity=entity_data['dexterity'],
                                       intelligence=entity_data['intelligence'],
                                       charisma=entity_data['charisma'], perception=entity_data['perception'],
                                       initiative=entity_data['initiative'],
                                       action_points=entity_data['action_points'], level=entity_data['level'],
                                       creature_class=entity_data['class'], money=entity_data['money'],
                                       ai=json_data['ai'], drop_money=json_data['drop_money'], drops=json_data['drops'])

        creature.id = entity_data['id_creature']

        equipment_db = DatabaseEquipment.get_equipment(entity_data['id_equipment']) if entity_data['id_equipment'] is not None else None
        # TODO equipment is not even saved to the database for creatures - for now it resets to
        #  default equipment from JSON
        creature.equipment = Equipment()
        for eq_part in json_data['equipment']:
            creature.equipment.__setattr__(eq_part, Item(name=json_data['equipment'][eq_part]))

        entity_row.append(creature)
