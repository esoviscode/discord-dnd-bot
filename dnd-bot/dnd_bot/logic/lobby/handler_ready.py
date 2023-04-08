from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import OnReadyException


class HandlerReady:

    @staticmethod
    async def on_ready(token, user_id) -> list:
        """ tries to join the player to the lobby
        :param token: token of the lobby/game
        :param user_id: user discord id
        :return: list of users in lobby
        """

        game = Multiverse.get_game(token)
        if game is None:
            raise OnReadyException(":warning: No game found using this token!")

        game.find_user(user_id).is_ready = True

        return game.user_list
