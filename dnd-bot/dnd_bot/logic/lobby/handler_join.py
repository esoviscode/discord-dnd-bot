from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerJoin:
    """handles joining the lobby """

    @staticmethod
    async def join_lobby(token, user_id, user_dm_channel, username) -> (bool, list, str):
        """ tries to join the player to the lobby
        :param token: token of the lobby/game
        :param user_id: user discord id
        :param user_dm_channel: user's private channel
        :param username: username
        :return:
            true if everything went correctly
                  - third argument is an empty string (no error);
            false if an error happened
                  - players in lobby is the second argument (list consisting of (player name, readiness, is_host, id_player) tuple),
                  - error message is the third argument
        """

        try:
            game = Multiverse.get_game(token)
        except KeyError:
            return False, [], f':warning: No game found using this token!'

        for user in game.user_list:
            if user.discord_id == user_id:
                return False, [], f':no_entry: You have already joined this game.'

        if game.game_state != 'LOBBY':
            return False, [], f':no_entry: This game has already started!'

        DatabaseUser.add_user(game.id, user_id)
        game.add_player(user_id, user_dm_channel, username, HandlerJoin.get_color_by_index(len(game.user_list)))

        users = game.user_list
        lobby_players = []

        for user in users:
            lobby_players.append((user.username, user.is_ready, user.is_host, user.discord_id))

        return True, lobby_players, ""

    @staticmethod
    def get_color_by_index(player_lobby_index):
        """returns string representing color by index of player in lobby"""
        if player_lobby_index == 0: return 'red'
        if player_lobby_index == 1: return 'blue'
        if player_lobby_index == 2: return 'green'
        if player_lobby_index == 3: return 'yellow'
        if player_lobby_index == 4: return 'orange'
        if player_lobby_index == 5: return 'purple'
