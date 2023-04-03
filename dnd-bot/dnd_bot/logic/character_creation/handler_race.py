from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.character_creation.chosen_attributes import ChosenAttributes
from dnd_bot.logic.character_creation.handler_character_creation import HandlerCharacterCreation


class HandlerRace:
    """Handles interactions with race form"""

    @staticmethod
    async def handle_back(view):
        """Called when user clicks back button
            :param view: ViewRaceForm instance to handle interaction with
            """
        # save user's choices if they were made
        if view.race_dropdown.values:
            ChosenAttributes.chosen_attributes[view.user_id]['race'] = view.race_dropdown.values[0]

        await Messager.delete_last_user_error_message(view.user_id)

    @staticmethod
    async def handle_confirm(view):
        """Called when user clicks confirm button
                    :param view: ViewRaceForm instance to handle interaction with
                    """
        # save user's choices if they were made
        if view.race_dropdown.values:
            ChosenAttributes.chosen_attributes[view.user_id]['race'] = view.race_dropdown.values[0]

        # user hasn't chosen any option
        if not view.race_dropdown.values and not ChosenAttributes.chosen_attributes[view.user_id]['race']:
            raise Exception("You must choose a race!")

        await HandlerCharacterCreation.assign_attribute_values(view.user_id)
        await Messager.delete_last_user_error_message(view.user_id)
