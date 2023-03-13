from dnd_bot.logic.prototype.creature import Creature


class FrostMage(Creature):

    def __init__(self, x=0, y=0, game_token='', look_direction='down'):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/entities/creatures/frost_mage_sprite.png",
                         name="Frost mage", game_token=game_token, look_direction=look_direction)
