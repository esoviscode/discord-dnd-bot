from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.database.database_player import DatabasePlayer


class DatabaseSkill:

    @staticmethod
    def add_skill(name: str = "") -> int | None:
        query = f'INSERT INTO public."Skill" (name) VALUES (%s)'
        return DatabaseConnection.add_to_db(query, (name,), "Skill")

    @staticmethod
    def get_skill(id_skill) -> dict | None:
        query = f'SELECT name FROM public."Skill" WHERE id_skill = (%s)'
        db_t = DatabaseConnection.get_object_from_db(query, (id_skill,), "Skill")
        return {'id_skill': id_skill, 'name': db_t[0]}

    @staticmethod
    def get_all_skills() -> list | None:
        query = f'SELECT * FROM public."Skill"'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, element_name="Skills")
        skill_list = []
        for element in db_l:
            skill_list.append({'id_skill': element[0], 'name': element[1]})

        return skill_list

    @staticmethod
    def add_entity_skill(id_entity: int = 0, id_skill: int = 0) -> None:
        query = f'INSERT INTO public."Entity_Skill" (id_entity, id_skill) VALUES (%s, %s)'
        DatabaseConnection.add_to_db(query, (id_entity, id_skill), "Entity_Skill")

    @staticmethod
    def get_players_skills(id_player) -> list | None:
        id_entity = DatabasePlayer.get_players_id_entity(id_player)
        query = f'SELECT id_skill FROM public."Entity_Skill" WHERE id_entity = (%s)'
        db_l = DatabaseConnection.get_multiple_objects_from_db(query, (id_entity,), "Entity_Skill")
        skills = []
        for element in db_l:
            skill = DatabaseSkill.get_skill(element[0])
            skills.append({'id_skill': skill['id_skill'], 'name': skill['name']})

        return skills
