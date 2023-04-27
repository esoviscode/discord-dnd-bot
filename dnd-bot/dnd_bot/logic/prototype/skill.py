from dnd_bot.logic.prototype.database_object import DatabaseObject


class Skill(DatabaseObject):
    """Represents a skill that can be used by entity"""

    def __init__(self, id_skill: int = 0, name: str = ""):
        ## TODO super().__init__(DatabaseSkill.add_skill(name))
        self.id_skill = id_skill
        self.name = name
