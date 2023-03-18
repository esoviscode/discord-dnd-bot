from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseEquipment:

    @staticmethod
    def add_equipment(helmet: int = None, chest: int = None, leg_armor: int = None, boots: int = None, left_hand=None,
                      right_hand: int = None, accessory: int = None) -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Equipment" (helmet, chest, leg_armor, boots, '
                                            f'left_hand, right_hand, accessory) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                            (helmet, chest, leg_armor, boots, left_hand, right_hand, accessory),
                                            "Equipment")

    @staticmethod
    def update_equipment(id_equipment: int = 0, helmet: int = None, chest: int = None, leg_armor: int = None,
                         boots: int = None, left_hand: int = None, right_hand: int = None, accessory: int = None) -> None:
        DatabaseConnection.update_object_in_db(f'UPDATE public."Equipment" SET helmet = (%s), chest = (%s),'
                                               f'leg_armor = (%s), boots = (%s), left_hand = (%s), right_hand = (%s),'
                                               f'accessory = (%s) WHERE id_equipment = (%s)',
                                               (helmet, chest,  leg_armor, boots, left_hand, right_hand, accessory,
                                                id_equipment), "Equipment")

    @staticmethod
    def get_equipment(id_equipment: int = 0) -> dict | None:
        pass
