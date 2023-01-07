class Entity:

    def __init__(self, entity_id: int, x: int, y: int, sprite, name: str, skill):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.id = entity_id
        self.name = name
        self.skill = skill
