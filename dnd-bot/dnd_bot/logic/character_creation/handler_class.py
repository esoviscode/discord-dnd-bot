from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes


class HandlerClass:
    """Handles interactions with class form"""

    @staticmethod
    async def handle_back(view):
        """Called when user clicks back button
            :param view: ViewClassForm instance to handle interaction with
            """
        # save user's choices if they were made
        if view.class_dropdown.values:
            ChosenAttributes.chosen_attributes[view.user_id]['class'] = view.class_dropdown.values[0]

        await Messager.delete_last_user_error_message(view.user_id)

    @staticmethod
    async def handle_next(view):
        """Called when user clicks next button
                    :param view: ViewClassForm instance to handle interaction with
                    """
        # save user's choices if they were made
        if view.class_dropdown.values:
            ChosenAttributes.chosen_attributes[view.user_id]['class'] = view.class_dropdown.values[0]

        # user hasn't chosen any option
        if not view.class_dropdown.values and not ChosenAttributes.chosen_attributes[view.user_id]['class']:
            raise Exception("You must choose a class!")

        await Messager.delete_last_user_error_message(view.user_id)
