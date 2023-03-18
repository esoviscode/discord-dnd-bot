from dnd_bot.database.database_connection import DatabaseConnection


class DatabaseItem:

    @staticmethod
    def add_item(name: str = "", hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0,
                 charisma: int = 0, perception: int = 0, action_points: int = 0, effect: str = "",
                 base_price: int = 0, description: str = "") -> int | None:
        return DatabaseConnection.add_to_db(f'INSERT INTO public."Item" (name, "HP", strength, dexterity, intelligence,'
                                            f'charisma, perception, action_points, effect, base_price, description) '
                                            f'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                            (name, hp, strength, dexterity, intelligence, charisma, perception,
                                             action_points, effect, base_price, description), "Item")

    @staticmethod
    def get_item(id_item) -> dict | None:
        pass

    @staticmethod
    def add_creature_item(id_creature: int = 0, id_item: int = 0, amount: int = 0) -> None:
        pass

