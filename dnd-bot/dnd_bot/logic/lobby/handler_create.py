import random

from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.lobby.handler_join import HandlerJoin
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.user import User
from dnd_bot.logic.utils.exceptions import CreateLobbyException

generated_ids = []
MAX_RANDOM_VALUE = 10000


class HandlerCreate:
    """handles creation of the lobby"""

    id_index = 0

    @staticmethod
    def generate_game_id():
        """generates unique and random game token"""
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
    async def create_lobby(host_id, host_dm_channel, host_username, discord_channel) -> (str, User):
        """creates an actual lobby
        :param host_id: discord id of the host/user who used the command
        :param host_dm_channel: discord private message channel with host
        :param host_username: discord username
        :param discord_channel: id of discord channel
        :return: (new game token, User object of host)
        """
        tokens = DatabaseGame.get_all_game_tokens()
        token = await HandlerCreate.generate_token()
        while token in tokens:
            token = await HandlerCreate.generate_token()

        #TODO add ability to choose another campaign
        DatabaseGame.add_game(token, host_id, "LOBBY", "Storm King's Thunder")
        game = Game(token, host_id, "Storm King's Thunder", "LOBBY")

        if game.id is None:
            raise CreateLobbyException(":no_entry: Error creating game!")

        DatabaseUser.add_user(game.id, host_id, discord_channel)
        user = User(token, host_id, host_dm_channel, host_username, HandlerJoin.get_color_by_index(0), True)
        if user.id is None:
            raise CreateLobbyException(":no_entry: Error creating host user")

        if not Multiverse.masks:
            Multiverse.generate_masks()
        Multiverse.add_game(game)
        Multiverse.get_game(token).add_host(user)

        return token, user

    @staticmethod
    async def generate_token() -> str:
        return str(random.randint(10000, 99999))
