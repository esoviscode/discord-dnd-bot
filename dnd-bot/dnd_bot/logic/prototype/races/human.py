from dnd_bot.logic.prototype.character_race import CharacterRace


class Human(CharacterRace):
    @staticmethod
    def emoji():
        return "👨"

    @staticmethod
    def base_hp():
        return 15

    @staticmethod
    def base_strength():
        return 6

    @staticmethod
    def base_dexterity():
        return 6

    @staticmethod
    def base_intelligence():
        return 10

    @staticmethod
    def base_charisma():
        return 6

    @staticmethod
    def base_perception():
        return 2

    @staticmethod
    def base_action_points():
        return 10

    @staticmethod
    def base_initiative():
        return 10
