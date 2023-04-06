from dnd_bot.logic.prototype.entity import Entity


class Corpse(Entity):

    entity_name = "Corpse"
    sprite_path = "dnd_bot/assets/gfx/entities/hole.png"

    def __init__(self, x, y, game_token, sprite_path=None):
        if sprite_path is not None:
            Corpse.sprite_path = sprite_path
        super().__init__(x=x, y=y, game_token=game_token, name=Corpse.entity_name, sprite=Corpse.sprite_path, fragile=True)
