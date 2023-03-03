class DatabaseCreature:

    @staticmethod
    def add_creature(level: int = 0, hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0,
                     perception: int = 0, initiative: int = 0, action_points: int = 0, money: int = 0,
                     id_entity: int = 0) -> int | None:
        pass

    @staticmethod
    def update_creature(id_entity: int = 0, level: int = 0, hp: int = 0, strength: int = 0, dexterity: int = 0,
                        intelligence: int = 0, perception: int = 0, initiative: int = 0, action_points: int = 0,
                        money: int = 0, ) -> None:
        pass

    @staticmethod
    def get_creature(id_creature: int = 0) -> dict | None:
        pass
