from dnd_bot.logic.prototype.character_race import CharacterRace


class Dwarf(CharacterRace):
    @staticmethod
    def emoji():
        return "🤏"

    @staticmethod
    def base_hp():
        return 20

    @staticmethod
    def base_strength():
        return 10

    @staticmethod
    def base_dexterity():
        return 3

    @staticmethod
    def base_intelligence():
        return 3

    @staticmethod
    def base_charisma():
        return 10

    @staticmethod
    def base_perception():
        return 1

    @staticmethod
    def base_action_points():
        return 3

    @staticmethod
    def base_initiative():
        return 7
