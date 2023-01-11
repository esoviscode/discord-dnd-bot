from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerJoin:
    """handles joining to the lobby """

    @staticmethod
    async def join_lobby(token, user_id, user_dm_channel, username) -> (bool, list, str):
        """ tries to join the player to the lobby
        :param token: token of the lobby/game
        :param user_id: user discord id
        :param user_dm_channel: users private channel
        :param username: username
        :return:
            true if everything went correctly
                  - second argument is an empty string;
            false if an error happened
                  - players in lobby is the third argument (list consisting of (player name, readiness, is_host, id_player) tuple),
                  - error message is the fourth argument
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

        game.add_player(user_id, user_dm_channel, username)

        users = game.user_list
        lobby_players = []

        for user in users:
            lobby_players.append((user.username, user.is_ready, user.is_host, user.discord_id))

        return True, lobby_players, ""
