from dnd_bot.logic.prototype.entity import Entity


class Corpse(Entity):

    entity_name = "Corpse"
    sprite_path = "dnd_bot/assets/gfx/entities/corpse.png"

    def __init__(self, x=0, y=0, game_token="", creature_name="", dropped_money=0, dropped_items=None, sprite_path=None):
        """creates corpse entity with default sprite, but you can pass path to other sprite"""
        if dropped_items is None:
            dropped_items = []
        if sprite_path is not None:
            Corpse.sprite_path = sprite_path
        super().__init__(x=x, y=y, game_token=game_token, name=Corpse.entity_name, sprite=Corpse.sprite_path, fragile=True)
        self.dropped_money = dropped_money
        self.dropped_items = dropped_items
        self.creature_name = creature_name
