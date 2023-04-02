from dnd_bot.database.database_connection import DatabaseConnection


class DatabasePlayerItem:

    @staticmethod
    def add_player_item(id_player: int, id_item: int, amount: int = 1):
        DatabaseConnection.add_to_db(f'INSERT INTO public."Player_Item" (id_player, id_item, amount) VALUES (%s,%s, %s)',
                                     (id_player, id_item, amount), "Player_Item")

    @staticmethod
    def get_creature_items(id_player: int):
        return DatabaseConnection.get_multiple_objects_from_db(f'SELECT id_item, amount FROM public."Player_Item" WHERE '
                                                                f'id_player = (%s)', (id_player,), "player_Item")
