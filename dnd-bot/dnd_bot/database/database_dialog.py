from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseDialog:

    @staticmethod
    def add_dialog(id_speaker: int = 0, id_listener: int = 0, content: str = "", status: str = "",
                   json_id: int = 0) -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Dialog" (id_speaker, id_listener, content, status'
                                            f', json_id) VALUES(%s, %s, %s, %s, %s)', (id_speaker, id_listener, content,
                                                                                       status, json_id), "Dialog")

    @staticmethod
    def update_dialog(id_dialog: int, status: str = "") -> None:
        DatabaseConnection.update_object_in_db(f'UPDATE public."Dialog" SET status = (%s) WHERE  id_dialog = (%s)',
                                               (status, id_dialog), "Dialog")

    @staticmethod
    def get_dialog(id_dialog: int = 0) -> dict | None:
        db_d = DatabaseConnection.get_object_from_db(f'SELECT * FROM public."Dialog" WHERE id_dialog = (%s)',
                                                     (id_dialog,), "Dialog")
        return {'id_dialog': db_d[0], 'id_speaker': db_d[1], 'id_listener': db_d[2], 'content': db_d[3],
                'status': db_d[4], 'json_id': db_d[5]}

    @staticmethod
    def get_speakers_dialogs(id_speaker: int = None) -> list | None:
        query = f'SELECT id_dialog FROM public."Dialog" WHERE id_speaker = (%s)'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, (id_speaker,), "Dialog")
        speakers_dialogs = []
        for element in db_l:
            speakers_dialogs.append(DatabaseDialog.get_dialog(element[0]))
        return speakers_dialogs
