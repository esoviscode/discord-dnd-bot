from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerJoin:

    @staticmethod
    async def join_lobby(token, user_id, user_dm_channel, username) -> (bool, list, str):
        """join_lobby
            returns true if everything went correctly
                - second argument is an empty string
            returns false if an error happened
                - players in lobby is the third argument (list consisting of (player name, readiness, is_host, id_player) tuple)
                - error message is the fourth argument
        """

        game = Multiverse.get_game(token)
        game.add_player(user_id, user_dm_channel, username)

        users = game.user_list
        lobby_players = []

        for user in users:
            lobby_players.append((user.username, user.is_ready, user.is_host, user.discord_id))

        return True, lobby_players, ""
