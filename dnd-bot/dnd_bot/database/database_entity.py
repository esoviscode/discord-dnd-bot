from typing import List

from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseEntity:

    @staticmethod
    def add_entity(name: str = "", x: int = 0, y: int = 0, id_game: int = None, description: str = "", look_direction: str = "RIGHT") -> int | None:
        if look_direction is not None:
            look_direction = look_direction.upper()

        return DatabaseConnection.add_to_db('INSERT INTO public."Entity" (name, x, y, id_game, description, look_direction) VALUES'
                                            '(%s, %s, %s, %s, %s, %s)', (name, x, y, id_game, description, look_direction), "entity")

    @staticmethod
    def add_entity_query(name: str = "", x: int = 0, y: int = 0, id_game: int = None, description: str = "", look_direction: str = "RIGHT") -> tuple[str, tuple]:
        if look_direction is not None:
            look_direction = look_direction.upper()

        return 'INSERT INTO public."Entity" (name, x, y, id_game, description, look_direction) VALUES (%s, %s, %s, %s, %s, %s)', (name, x, y, id_game, description, look_direction)

    @staticmethod
    def update_entity(id_entity: int = 0, x: int = 0, y: int = 0, look_direction: str = "RIGHT") -> None:
        DatabaseConnection.update_object_in_db('UPDATE public."Entity" SET x = (%s), y = (%s), look_direction = (%s) WHERE id_entity = (%s)',
                                               (x, y, look_direction, id_entity), "Entity")

    @staticmethod
    def update_entity_query(id_entity: int = 0, x: int = 0, y: int = 0) -> tuple[str, tuple]:
        return 'UPDATE public."Entity" SET x = (%s), y = (%s) WHERE id_entity = (%s)', (x, y, id_entity)

    @staticmethod
    def get_entity(id_entity: int) -> dict | None:
        query = f'SELECT * FROM public."Entity" WHERE id_entity = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_entity,), "Entity")
        return {'id_entity': db_t[0], 'name': db_t[1], 'x': db_t[2], 'y': db_t[3],
                'id_game': db_t[4], 'description': db_t[5], 'look_direction': db_t[6]}

    @staticmethod
    def get_all_entities(id_game: int) -> List[dict] | None:
        query = f'SELECT * FROM public."Entity" WHERE id_game = (%s)'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, (id_game,), "Entities")
        return [{'id_entity': db_t[0], 'name': db_t[1], 'x': db_t[2], 'y': db_t[3],
                 'id_game': db_t[4], 'description': db_t[5]} for db_t in db_l]

    @staticmethod
    def get_entity_query(id_entity: int) -> tuple[str, tuple]:
        return 'SELECT * FROM public."Entity" WHERE id_entity = (%s)', (id_entity,)

    @staticmethod
    def get_entity_skills(id_entity: int = 0) -> list | None:
        pass
