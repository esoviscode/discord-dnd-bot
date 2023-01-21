from dnd_bot.logic.prototype.entity import Entity


class Rock(Entity):

    def __init__(self, x=0, y=0, game_token=''):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/entities/rock.png", name="Rock", game_token=game_token)
