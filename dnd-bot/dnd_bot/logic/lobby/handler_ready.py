from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerReady:

    @staticmethod
    async def on_ready(token, user_id) -> (bool, list, str):
        """on_ready
            returns users in lobby
                - list consisting of (player name, readiness, is_host, id_player) tuple
        """

        Multiverse.get_game(token).find_user(user_id).is_ready = True
        users = Multiverse.get_game(token).user_list
        lobby_players = []
        for user in users:
            lobby_players.append((user.username, user.is_ready, user.is_host, user.discord_id))

        return lobby_players
