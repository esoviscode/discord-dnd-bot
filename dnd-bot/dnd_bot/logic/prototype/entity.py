import cv2 as cv

from dnd_bot.logic.prototype.database_object import DatabaseObject


class Entity(DatabaseObject):
    """This class is the base class for all entities in the game like creatures and elements on the map"""

    def __init__(self, id: int = 0, x: int = 0, y: int = 0, sprite: str = '', name: str = 'Entity', game_token: str = '',
                 skills=None, fragile: bool = False, look_direction: str = 'down'):
        """":param fragile: if entity can be moved or destroyed from its position"""
        super().__init__(id)
        if skills is None:
            skills = []
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name = name
        self.game_token = game_token
        self.skills = skills
        self.fragile = fragile
        self.look_direction = look_direction
        self.sprite_path = sprite
        if sprite:
            self.sprite = cv.imread(sprite, cv.IMREAD_UNCHANGED)
            self.sprite = cv.resize(self.sprite, (50, 50), interpolation=cv.INTER_AREA)

    def __str__(self):
        return f'<{self.name} x={self.x} y={self.y}>'

    def __repr__(self):
        return f'<{self.name} x={self.x} y={self.y}>'

    def move_one_tile(self, direction, game):
        """moves entity one tile in set direction"""

        if direction == 'right':
            if self.x + 1 >= game.world_width:
                raise Exception("You cannot go beyond the world border!")

            if game.entities[self.y][self.x + 1] is not None:
                raise Exception("This field is taken!")

            tmp = game.entities[self.y].pop(self.x + 1)
            this = game.entities[self.y].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y].insert(self.x + 1, this)

            self.x += 1
            self.look_direction = direction
            return
        elif direction == 'left':
            if self.x - 1 < 0:
                raise Exception("You cannot go beyond the world border!")

            if game.entities[self.y][self.x - 1] is not None:
                raise Exception("This field is taken!")

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y].pop(self.x - 1)

            game.entities[self.y].insert(self.x - 1, this)
            game.entities[self.y].insert(self.x, tmp)

            self.x -= 1
            self.look_direction = direction
            return

        elif direction == 'up':
            if self.y - 1 < 0:
                raise Exception("You cannot go beyond the world border!")

            if game.entities[self.y - 1][self.x] is not None:
                raise Exception("This field is taken!")

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y - 1].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y - 1].insert(self.x, this)

            self.y -= 1
            self.look_direction = direction
            return
        elif direction == 'down':
            if self.y + 1 >= game.world_width:
                raise Exception("You cannot go beyond the world border!")

            if game.entities[self.y + 1][self.x] is not None:
                raise Exception("This field is taken!")

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y + 1].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y + 1].insert(self.x, this)

            self.y += 1
            self.look_direction = direction
            return
        else:
            raise Exception("Severe: this direction doesn't exist!")
