from dnd_bot.logic.prototype.character_race import CharacterRace


class Elf(CharacterRace):
    @staticmethod
    def emoji():
        return "🧝"

    @staticmethod
    def base_hp():
        return 10

    @staticmethod
    def base_strength():
        return 3

    @staticmethod
    def base_dexterity():
        return 10

    @staticmethod
    def base_intelligence():
        return 6

    @staticmethod
    def base_charisma():
        return 3

    @staticmethod
    def base_perception():
        return 3

    @staticmethod
    def base_action_points():
        return 6

    @staticmethod
    def base_initiative():
        return 7
