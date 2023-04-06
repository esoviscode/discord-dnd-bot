from dnd_bot.logic.prototype.entity import Entity


class DeadBody(Entity):

    entity_name = "Dead body"
    sprite_path = "dnd_bot/assets/gfx/entities/hole.png"

    def __init__(self, x, y, game_token, sprite_path=None):
        if sprite_path is not None:
            DeadBody.sprite_path = sprite_path
        super().__init__(x=x, y=y, game_token=game_token, name=DeadBody.entity_name, sprite=DeadBody.sprite_path)
