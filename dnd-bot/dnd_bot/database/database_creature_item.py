from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseCreatureItem:

    @staticmethod
    def add_creature_item(id_creature, id_item):
        DatabaseConnection.add_to_db(f'INSERT INTO public."Creature_Item" (id_creature, id_item) VALUES (%s,%s)',
                                     (id_creature, id_item), "Creature_Item")

    @staticmethod
    def get_creature_items(id_creature):
        DatabaseConnection.get_multiple_objects_from_db(f'SELECT id_item FROM public."Creature_Item" WHERE '
                                                        f'id_creature = (%s)', (id_creature,), "Creature_Item")
