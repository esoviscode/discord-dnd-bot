class DatabaseEntity:

    @staticmethod
    def add_entity(name: str = "", x: int = 0, y: int = 0, sprite=None, id_game: int = 0) -> int | None:
        pass

    @staticmethod
    def update_entity(id_entity: int = 0, x: int = 0, y: int = 0) -> None:
        pass

    @staticmethod
    def get_entity(id_entity: int) -> dict | None:
        pass

    @staticmethod
    def get_entity_skills(id_entity: int = 0) -> list | None:
        pass