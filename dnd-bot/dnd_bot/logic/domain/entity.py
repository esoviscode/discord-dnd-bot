class Entity:

    def __init__(self, entity_id, x, y, sprite, name, skill=None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.id = entity_id
        self.name = name
        self.skill = skill
