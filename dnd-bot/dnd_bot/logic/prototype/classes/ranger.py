from dnd_bot.logic.prototype.character_class import CharacterClass


class Ranger(CharacterClass):
    @staticmethod
    def emoji():
        return "🏹"

    @staticmethod
    def base_hp():
        return 0

    @staticmethod
    def base_strength():
        return 0

    @staticmethod
    def base_dexterity():
        return 0

    @staticmethod
    def base_intelligence():
        return 0

    @staticmethod
    def base_charisma():
        return 0

    @staticmethod
    def base_perception():
        return 0

    @staticmethod
    def base_action_points():
        return 0

    @staticmethod
    def base_initiative():
        return 10
