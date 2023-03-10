from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.logic.prototype.creature import Creature


class DatabaseCreature:

    @staticmethod
    def add_creature(x: int = 0, y: int = 0, sprite: str = '', name: str = 'Creature', hp: int = 0, strength: int = 0,
                     dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0,
                     initiative: int = 0, action_points: int = 0, level: int = 0, drop_money: int = 0,
                     id_game: int = 1) -> int | None:
        id_entity = DatabaseEntity.add_entity(name, x, y, sprite, id_game)
        id_creature = DatabaseConnection.add_to_db('INSERT INTO public."Creature" (level, "HP", strength, dexterity, '
                                                   'intelligence, charisma, perception, initiative, action_points, '
                                                   'money, id_entity) VALUES'
                                                   '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                                   (
                                                       level, hp, strength, dexterity, intelligence,
                                                       charisma, perception,
                                                       initiative, action_points, drop_money, id_entity),
                                                   "creature")
        return id_creature

    @staticmethod
    def update_creature(id_creature: int = 0, level: int = 0, hp: int = 0, strength: int = 0, dexterity: int = 0,
                        intelligence: int = 0, perception: int = 0, initiative: int = 0, action_points: int = 0,
                        money: int = 0) -> None:
        pass

    @staticmethod
    def get_creature(id_creature: int = 0) -> dict | None:
        pass

    @staticmethod
    def get_creature_items(id_creature) -> list | None:
        pass
