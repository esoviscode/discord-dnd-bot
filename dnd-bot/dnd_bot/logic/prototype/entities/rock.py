from dnd_bot.logic.prototype.entity import Entity


class Rock(Entity):

    def __init__(self, id=0, x=0, y=0, game_token=''):
        super().__init__(id=id, x=x, y=y, sprite="dnd_bot/assets/gfx/entities/rock.png", name="Rock", game_token=game_token)
