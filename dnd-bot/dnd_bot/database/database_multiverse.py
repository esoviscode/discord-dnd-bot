import time
from typing import List

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_event import DatabaseEvent
from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.game.initialize_world import InitializeWorld
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.event import Event
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.user import User
from dnd_bot.logic.utils.exceptions import GameException
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
        game: Game = Multiverse.get_game(token)
        if not game:
            # create a new game object
            dbdict = DatabaseGame.get_game(DatabaseGame.get_id_game_from_game_token(token))
            game = Game(token=dbdict['token'], id_host=dbdict['id_host'], game_state=dbdict['game_state'],
                        campaign_name=dbdict['campaign_name'])
            game.id = DatabaseGame.get_id_game_from_game_token(token)

            Multiverse.add_game(game)

            await InitializeWorld.load_entities(game, 'dnd_bot/assets/maps/map.json',
                                                'dnd_bot/assets/campaigns/campaign.json')

        time_snapshot = time.time()
        DatabaseMultiverse.__load_game_state_user_list(game)
        print(f'   - loading users - {round((time.time() - time_snapshot) * 1000, 2)} ms')

        time_snapshot = time.time()
        DatabaseMultiverse.__load_game_entities(game)
        print(f'   - loading entities - {round((time.time() - time_snapshot) * 1000, 2)} ms')

    @staticmethod
    def __load_game_state_user_list(game):
        game.user_list = []
        user_list = DatabaseUser.get_all_users(game.id)
        for user_dict in user_list:
            user = User(game_token=game.token, discord_id=user_dict['discord_id'])
            game.user_list.append(user)

    @staticmethod
    def __load_game_entities(game):
        entities: List[List[Entity]] = game.entities

        database_entities = DatabaseEntity.get_all_entities(game.id)

        for entities_row in entities:
            for e in entities_row:
                if e is None or e.fragile:
                    continue








