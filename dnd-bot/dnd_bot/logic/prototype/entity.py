class Entity:
    """This class is the base class for all entities in the game like creatures and elements on the map"""
    def __init__(self, x=0, y=0, sprite=None, name="", id_game=None, skills=[]):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name = name
        self.id_game = id_game
        self.skills = skills

