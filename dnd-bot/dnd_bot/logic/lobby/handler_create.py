import random

from dnd_bot.dc.ui.send_message import send_message, send_dm_message
from dnd_bot.logic.prototype.game import Game

generated_ids = []
MAX_RANDOM_VALUE = 10000


class HandlerCreate:

    id_index = 0

    def __init__(self):
        pass

    @staticmethod
    def handler_create(id_host):
        game = Game(id_host)

    @staticmethod
    def generate_game_id():
        ret = generated_ids[HandlerCreate.id_index]
        HandlerCreate.id_index += 1
        return ret

    @staticmethod
    def __generate_random_unique_numbers(to_generate):
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
    async def create_lobby(server, channel_id, host_id):
        host = server.get_member(host_id)
        game_id = 42069
        await send_message(server, channel_id, f"Hello {host.mention}!\n "
                                               f"A fresh game for you and your team has been created! Make sure that everyone who wants to play has to be in this server!\n"
                                               f"Game ID: ||{game_id}||")
        await send_dm_message(server, host_id, f"Welcome to **{game_id}** lobby!")
