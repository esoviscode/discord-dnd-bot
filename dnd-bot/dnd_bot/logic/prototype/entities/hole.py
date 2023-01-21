from dnd_bot.logic.prototype.entity import Entity


class Hole(Entity):

    def __init__(self, x, y):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/entities/hole.png", name="Hole")
