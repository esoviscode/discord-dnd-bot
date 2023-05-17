import time
from typing import List

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_creature import DatabaseCreature
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import GameException


class DatabaseMultiverse:

    @staticmethod
    def save_game_state(token):
        """
        driver method that handles saving all elements of a game
        :param token: game token
        """
        game: Game = Multiverse.get_game(token)
        if not game:
            raise GameException('Game with provided token doesn\'t exist!')

        print("\n-- Saving game state --")

        time_snapshot = time.time()
        DatabaseMultiverse.__save_game_entities(game.entities)
        print(f'   - saving entities - {round((time.time() - time_snapshot) * 1000, 2)} ms')

    @staticmethod
    def __save_game_entities(entities: List[List[Entity]]):

        for entities_row in entities:
            queries = []
            parameters_list = []

            for e in entities_row:
                if e is None:
                    continue

                if isinstance(e, Creature):
                    DatabaseMultiverse.__add_query_update_entity(e, queries, parameters_list)
                    DatabaseMultiverse.__add_query_update_creature(e, queries, parameters_list)
                    continue

                if isinstance(e, Entity):
                    DatabaseMultiverse.__add_query_update_entity(e, queries, parameters_list)
                    continue

            DatabaseConnection.update_multiple_objects_in_db(queries, parameters_list)

    @staticmethod
    def __add_query_update_entity(entity: Entity, queries: List[str], parameters_list: List[tuple]) -> None:
        query, parameters = DatabaseEntity.update_entity_query(id_entity=entity.id,
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
