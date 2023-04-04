from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import JoinLobbyException


class HandlerJoin:
    """handles joining the lobby """

    @staticmethod
    async def join_lobby(token, user_id, user_dm_channel, username) -> list:
        """ tries to join the player to the lobby
        :param token: token of the lobby/game
        :param user_id: user discord id
        :param user_dm_channel: user's private channel
        :param username: username
        :return: list of users in lobby
        """

        game = Multiverse.get_game(token)
        if game is None:
            raise JoinLobbyException(":warning: No game found using this token!")

        for user in game.user_list:
            if user.discord_id == user_id:
                raise JoinLobbyException(":no_entry: You have already joined this game!")

        if game.game_state != 'LOBBY':
            raise JoinLobbyException(":no_entry: This game has already started!")

        DatabaseUser.add_user(game.id, user_id)
        game.add_player(user_id, user_dm_channel, username, HandlerJoin.get_color_by_index(len(game.user_list)))

        return game.user_list

    @staticmethod
    def get_color_by_index(player_lobby_index):
        """returns string representing color by index of player in lobby"""
        if player_lobby_index == 0: return 'red'
        if player_lobby_index == 1: return 'blue'
        if player_lobby_index == 2: return 'green'
        if player_lobby_index == 3: return 'yellow'
        if player_lobby_index == 4: return 'orange'
        if player_lobby_index == 5: return 'purple'
