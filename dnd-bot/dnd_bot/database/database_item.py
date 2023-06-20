from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseItem:

    @staticmethod
    def add_item(name: str = "") -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Item" (name) VALUES (%s)', (name,), "Item")

    @staticmethod
    def get_item(id_item) -> dict | None:
        query = f'SELECT * FROM public."Item" WHERE id_item = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_item,), "Item")
        if db_t is None:
            return None

        return {'id_item': db_t[0], 'name': db_t[1]}

    @staticmethod
    def get_all_items() -> list | None:
        query = f'SELECT * FROM public."Item"'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query,element_name="Item")
        item_list = []
        for element in db_l:
            item_list.append({'id_item': element[0], 'name': element[1]})

        return item_list


