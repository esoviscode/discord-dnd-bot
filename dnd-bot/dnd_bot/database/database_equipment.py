class DatabaseEquipment:

    @staticmethod
    def add_equipment(helmet: int = -1, chest: int = -1, leg_armor: int = -1, boots: int = -1, left_hand=-1,
                      right_hand: int = -1, accessory: int = -1) -> int | None:
        pass

    @staticmethod
    def update_equipment(id_equipment: int = 0, helmet: int = -1, chest: int = -1, leg_armor: int = -1, boots: int = -1,
                         left_hand: int = -1, right_hand: int = -1, accessory: int = -1) -> None:
        pass

    @staticmethod
    def get_equipment(id_equipment: int = 0) -> dict | None:
        pass
