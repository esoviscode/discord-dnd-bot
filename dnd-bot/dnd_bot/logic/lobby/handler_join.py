import asyncio

import nextcord

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.dc.utils.utils import get_user_name_by_id


class HandlerJoin:

    @staticmethod
    async def join_lobby(token, user_id, name):
        game_data = DatabaseConnection.find_game_by_token(token)
        if game_data is None:
            await Messager.send_dm_message(user_id, "The token is wrong or the game has already started")
            return

        users = game_data['players']

        for user in users:
            if user['discord_id'] == user_id:
                await Messager.send_dm_message(user_id, "You have already joined this game.")
                return

        # send message to other users in the lobby
        DatabaseConnection.add_user(game_data['id_game'], user_id)

        game_data = DatabaseConnection.find_game_by_token(token)
        users = game_data['players']
        lobby_players = []

        for user in users:
            username = await get_user_name_by_id(user['discord_id'])
            if user['discord_id'] == game_data['id_host']:
                lobby_players.append((username, False, True))
            else:
                lobby_players.append((username, False, False))

        lobby_view_embed = MessageTemplates.lobby_view_message_template(token, lobby_players)

        await Messager.send_dm_message(user_id, f"Welcome to lobby of game {token}.\nNumber of players in lob"
                                          f"by: **{len(users)}**", embed=lobby_view_embed)

        for user in users:
            if user['discord_id'] != user_id:
                await Messager.send_dm_message(user['discord_id'], f"\n**{name}** has joined the lobby! Current number of "
                                                                f"players: **{len(users)}**", embed=lobby_view_embed)


