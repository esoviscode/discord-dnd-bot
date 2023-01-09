import asyncio

import nextcord

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.utils import get_user_name_by_id
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

        game_data = DatabaseConnection.find_game_by_token(token)
        if game_data is None:
            return False, [], f':no_entry: No game found using this token!'

        if game_data['game_state'] != 'LOBBY':
            return False, [], f':warning: This game has already started!'

        users = game_data['players']

        for user in users:
            if user['discord_id'] == user_id:
                return False, [], f':no_entry: You have already joined this game.'

        # handle join user operation
        DatabaseConnection.add_user(game_data['id_game'], user_id)

        game_data = DatabaseConnection.find_game_by_token(token)
        users = game_data['players']
        lobby_players = []

        for user in users:
            username = await get_user_name_by_id(user['discord_id'])
            if user['discord_id'] == game_data['id_host']:
                lobby_players.append((username, False, True, user['discord_id']))
            else:
                lobby_players.append((username, False, False, user['discord_id']))

        # add data to Multiverse
        game = Multiverse.get_game(token)
        game.add_player(user_id, user_dm_channel, username)

        return True, lobby_players, ""
