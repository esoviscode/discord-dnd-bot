import nextcord

from dnd_bot.dc.ui.message_templates import MessageTemplates
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import CharacterCreationInterfaceException


class HandlerStatsRetrospective:
    """Handles interactions with stats retrospective form"""

    @staticmethod
    async def handle_confirm(view):
        """Called when user clicks confirm button
                    :param view: ViewStatsRetrospectiveForm instance to handle interaction with
                    """
        game = Multiverse.get_game(view.token)

        if game is None:
            raise CharacterCreationInterfaceException("Game of provided token doesn't exist!")

        game.find_user(view.user_id).is_ready = True

        if game.all_users_ready():
            # delete error messages for all users
            for user in game.user_list:
                await Messager.delete_last_user_error_message(user.discord_id, view.token)

            await GameStart.start(view.token)
            await GameLoop.start_loop(view.token)
        else:
            for component in view.children:
                if isinstance(component, nextcord.ui.Button):
                    component.disabled = True
            await Messager.edit_last_user_message(user_id=view.user_id,
                                                  token=view.token,
                                                  embeds=[MessageTemplates.stats_retrospective_form_view_message_template(
                                                      view.user_id, view.token)],
                                                  view=view)
            raise CharacterCreationInterfaceException("You created your character! Now wait for other players to "
                                                      "finish!")
