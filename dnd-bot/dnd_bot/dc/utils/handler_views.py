import asyncio

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.utils import get_player_view


class HandlerViews:
    @staticmethod
    async def display_views_for_users(game_token, recent_action_message, update_pov: bool = True):
        """sends views for users and makes sure that the displayed view is correct"""
        game = Multiverse.get_game(game_token)

        async def send_view(user):
            # get current view from player and resend it in case someone made an action
            player_current_view, player_current_embeds = game.players_views[user.discord_id]
            view_to_show = player_current_view(game_token, user.discord_id)

            player = game.get_player_by_id_user(user.discord_id)
            if not player:
                game.user_list.remove(user)
                del game.players_views[user.discord_id]
                return
            if update_pov:  # if to generate new player's pov
                player_view = get_player_view(Multiverse.get_game(game_token), player, player.attack_mode)
            turn_view_embed = await MessageTemplates.creature_turn_embed(game_token, user.discord_id,
                                                                         recent_action=recent_action_message)
            await Messager.edit_last_user_message(user_id=user.discord_id,
                                                  token=game_token,
                                                  embeds=[turn_view_embed] + player_current_embeds,
                                                  view=view_to_show,
                                                  files=[player_view] if update_pov else None)

        q = asyncio.Queue()
        tasks = []
        for u in game.user_list:
            tasks.append(asyncio.create_task(send_view(u)))

        await asyncio.gather(*tasks)
        await q.join()
