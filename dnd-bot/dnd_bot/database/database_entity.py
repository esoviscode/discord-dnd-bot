from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseEntity:

    @staticmethod
    def add_entity(name: str = "", x: int = 0, y: int = 0, sprite=None, id_game: int = 0) -> int | None:
        return DatabaseConnection.add_to_db('INSERT INTO public."Entity" (name, x, y, sprite, id_game) VALUES'
                                            '(%s, %s, %s, %s, %s)', (name, x, y, sprite, id_game), "entity")

    @staticmethod
    def update_entity(id_entity: int = 0, x: int = 0, y: int = 0) -> None:
        pass

    @staticmethod
    def get_entity(id_entity: int) -> dict | None:
        pass

    @staticmethod
    def get_entity_skills(id_entity: int = 0) -> list | None:
        pass
