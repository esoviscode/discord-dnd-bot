import random

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse

generated_ids = []
MAX_RANDOM_VALUE = 10000


class HandlerCreate:

    id_index = 0

    @staticmethod
    def generate_game_id():
        ret = generated_ids[HandlerCreate.id_index]
        HandlerCreate.id_index += 1
        return ret

    @staticmethod
    def generate_random_unique_numbers(to_generate):
        generated_ids_number = 0

        for i in range(to_generate):
            rm = to_generate - generated_ids_number
            if random.randint(0, MAX_RANDOM_VALUE - i) < rm:
                generated_ids.append(i)
                generated_ids_number += 1

        assert generated_ids_number == to_generate

        for i in range(to_generate):
            j = i + random.randint(0, to_generate - i)
            tmp = generated_ids[j]
            generated_ids[i] = generated_ids[j]
            generated_ids[j] = tmp

    @staticmethod
    async def create_lobby(host_id, host_dm_channel, host_username) -> (bool, int, str):
        token = str(random.randint(10000, 99999))

        game_id = DatabaseConnection.add_game(token, host_id, 0, "LOBBY")
        if game_id is None:
            return False, -1, ":no_entry: Error creating game!"

        user_id = DatabaseConnection.add_user(game_id, host_id)
        if user_id is None:
            return False, -1, ":no_entry: Error creating host user"

        game = Game(token)

        Multiverse.add_game(game)
        print(Multiverse.games)
        Multiverse.get_game(token).add_host(host_id, host_dm_channel, host_username)

        return True, token, ""
