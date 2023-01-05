import asyncio

import nextcord

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager


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

        lobby_view_embed = MessageTemplates.lobby_view_message_template(token)

        await Messager.send_dm_message(user_id, f"Welcome to lobby of game {token}.\nNumber of players in lob"
                                          f"by: **{len(users) + 1}**", embed=lobby_view_embed)

        for user in users:
            await Messager.send_dm_message(user['discord_id'], f"\n**{name}** has joined the lobby! Current number of "
                                                                f"players: **{len(users) + 1}**", embed=lobby_view_embed)

        DatabaseConnection.add_user(game_data['id_game'], user_id)
