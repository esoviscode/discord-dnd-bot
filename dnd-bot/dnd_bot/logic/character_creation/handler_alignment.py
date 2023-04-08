from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.utils.exceptions import CharacterCreationInterfaceException


class HandlerAlignment:
    """Handles interactions with alignment form"""

    @staticmethod
    async def handle_back(view):
        """Called when user clicks back button
            :param view: ViewAlignmentForm instance to handle interaction with
            """
        # save user's choices if they were made
        if view.lawfulness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][0] = view.lawfulness_axis_dropdown.values[0]

        if view.goodness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][1] = view.goodness_axis_dropdown.values[0]

        await Messager.delete_last_user_error_message(view.user_id)

    @staticmethod
    async def handle_next(view):
        """Called when user clicks next button
                    :param view: ViewAlignmentForm instance to handle interaction with
                    """
        # save user's choices if they were made
        if view.lawfulness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][0] = view.lawfulness_axis_dropdown.values[0]

        if view.goodness_axis_dropdown.values:
            ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][1] = view.goodness_axis_dropdown.values[0]

        # user hasn't made choice in at least one dropdown
        if (not view.lawfulness_axis_dropdown.values or not view.goodness_axis_dropdown.values) and \
                (not ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][0] or
                 not ChosenAttributes.chosen_attributes[(view.user_id, view.token)]['alignment'][1]):
            raise CharacterCreationInterfaceException("You must choose an alignment!")

        await Messager.delete_last_user_error_message(view.user_id)
