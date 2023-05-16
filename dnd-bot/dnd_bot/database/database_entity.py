from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseEntity:

    @staticmethod
    def add_entity(name: str = "", x: int = 0, y: int = 0, id_game: int = None, description: str = "") -> int | None:
        return DatabaseConnection.add_to_db('INSERT INTO public."Entity" (name, x, y, id_game, description) VALUES'
                                            '(%s, %s, %s, %s, %s)', (name, x, y, id_game, description), "entity")

    @staticmethod
    def add_entity_query(name: str = "", x: int = 0, y: int = 0, id_game: int = None, description: str = "") -> tuple[str, tuple]:
        return 'INSERT INTO public."Entity" (name, x, y, id_game, description) VALUES (%s, %s, %s, %s, %s)', (name, x, y, id_game, description)

    @staticmethod
    def update_entity(id_entity: int = 0, x: int = 0, y: int = 0) -> None:
        DatabaseConnection.update_object_in_db('UPDATE public."Entity" SET x = (%s), y = (%s) WHERE id_entity = (%s)',
                                               (x, y, id_entity), "Entity")

    @staticmethod
    def get_entity(id_entity: int) -> dict | None:
        query = f'SELECT * FROM public."Entity" WHERE id_entity = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query,(id_entity,), "Entity")
        return {'id_entity': db_t[0], 'name': db_t[1], 'x': db_t[2], 'y': db_t[3],
                'id_game': db_t[4], 'description': db_t[5]}

    @staticmethod
    def get_entity_skills(id_entity: int = 0) -> list | None:
        pass
