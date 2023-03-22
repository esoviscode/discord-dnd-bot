from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseItem:

    @staticmethod
    def add_item(name: str = "") -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Item" (name) '
                                            f'VALUES(%s)', (name,), "Item")

    @staticmethod
    def get_item(id_item) -> dict | None:
        pass

    @staticmethod
    def add_creature_item(id_creature: int = 0, id_item: int = 0, amount: int = 0) -> None:
        pass

