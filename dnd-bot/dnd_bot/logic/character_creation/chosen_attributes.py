class ChosenAttributes:
    """Class used to hold the information about user's choices during character creation process to retain them when
    user is switching between forms. Information about particular user should be deleted after finishing creation
    process """

    # dict with user's choices, keys are discord_ids and values are another dicts with attributes names as keys
    chosen_attributes = {}

    @staticmethod
    def add_empty_user(user_id):
        ChosenAttributes.chosen_attributes[user_id] = {'name': None,
                                                       'backstory': None,
                                                       'alignment': [None, None],
                                                       'class': None,
                                                       'race': None,
                                                       'hp': None,
                                                       'strength': None,
                                                       'dexterity': None,
                                                       'intelligence': None,
                                                       'charisma': None,
                                                       'perception': None,
                                                       'initiative': None,
                                                       'action points': None}

    @staticmethod
    def delete_user(user_id):
        del ChosenAttributes.chosen_attributes[user_id]
