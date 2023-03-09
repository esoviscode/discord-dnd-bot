from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.logic.prototype.creature import Creature


class DatabaseCreature:

    @staticmethod
    def add_creature(c: Creature) -> int | None:
        id_entity = DatabaseEntity.add_entity(c.name, c.x, c.y, 'sprite', c.id_game)
        id_creature = DatabaseConnection.add_to_db('INSERT INTO public."Creature" (level, "HP", strength, dexterity, '
                                                   'intelligence, charisma, perception, initiative, action_points, '
                                                   'money, id_entity) VALUES'
                                                   '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                                   (
                                                       c.level, c.hp, c.strength, c.dexterity, c.intelligence,
                                                       c.charisma, c.perception,
                                                       c.initiative, c.action_points, c.drop_money, id_entity),
                                                   "creature")
        c.id = id_creature
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
