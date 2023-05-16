from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseEvent:

    @staticmethod
    def add_event(status: str = "NOT_AVAILABLE", id_game: int = None, json_id: int = 0) -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Event" (status, id_game, json_id) VALUES(%s, %s, %s)',
                                            (status, id_game, json_id), "Event")

    @staticmethod
    def get_event(id_event) -> dict | None:
        query = f'SELECT * FROM public."Event" WHERE id_event = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_event,), "Event")
        if db_t is None:
            return None
        return {'id_event': db_t[0], 'status': db_t[1], 'id_game': db_t[2], 'json_id': db_t[3]}
    
    @staticmethod
    def get_game_events(id_game) -> list | None:
        query = f'SELECT id_event FROM public."Event" WHERE id_game = (%s)'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, (id_game,), "Event")
        game_events = []
        for element in db_l:
            game_events.append(DatabaseEvent.get_event(element[0]))

        return game_events

    @staticmethod
    def update_event(id_event: int, status: str = '') -> None:
        query = f'UPDATE public."Event" SET status = (%s) WHERE id_event = (%s)'
        DatabaseConnection.update_object_in_db(query, (status, id_event), "Event")
