class DatabaseItem:

    @staticmethod
    def add_item(name: str = "", hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0,
                 charisma: int = 0, perception: int = 0, action_points: int = 0, effect: str = "",
                 base_price: int = 0) -> int | None:
        pass

    @staticmethod
    def get_item(id_item) -> dict | None:
        pass

    @staticmethod
    def add_creature_item(id_creature: int = 0, id_item: int = 0, amount: int = 0) -> None:
        pass

