import cv2 as cv


class Entity:
    """This class is the base class for all entities in the game like creatures and elements on the map"""
    def __init__(self, x=0, y=0, sprite=None, name='Entity', id_game=0, game_token='', skills=None, fragile=False):
        """":param fragile: if entity can be moved or destroyed from its position"""
        if skills is None:
            skills = []
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name = name
        self.id_game = id_game
        self.game_token = game_token
        self.skills = skills
        self.fragile = fragile
        self.look_direction = 'down'
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
            if game.entities[self.y][self.x + 1] is not None:
                return False, 'This field is taken!'

            tmp = game.entities[self.y].pop(self.x + 1)
            this = game.entities[self.y].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y].insert(self.x + 1, this)

            self.x += 1
            self.look_direction = direction
            return True, ''

        elif direction == 'left':
            if game.entities[self.y][self.x - 1] is not None:
                return False, 'This field is taken!'

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y].pop(self.x - 1)

            game.entities[self.y].insert(self.x - 1, this)
            game.entities[self.y].insert(self.x, tmp)

            self.x -= 1
            self.look_direction = direction
            return True, ''

        elif direction == 'up':
            if game.entities[self.y - 1][self.x] is not None:
                return False, 'This field is taken!'

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y - 1].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y - 1].insert(self.x, this)

            self.y -= 1
            self.look_direction = direction
            return True, ''
        elif direction == 'down':
            if game.entities[self.y + 1][self.x] is not None:
                return False, 'This field is taken!'

            this = game.entities[self.y].pop(self.x)
            tmp = game.entities[self.y + 1].pop(self.x)

            game.entities[self.y].insert(self.x, tmp)
            game.entities[self.y + 1].insert(self.x, this)

            self.y += 1
            self.look_direction = direction
            return True, ''
        else:
            return False, 'Severe: this direction doesn\'t exist!'
