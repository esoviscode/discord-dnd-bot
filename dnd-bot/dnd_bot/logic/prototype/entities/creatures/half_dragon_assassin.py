from dnd_bot.logic.prototype.creature import Creature


class HalfDragonAssassin(Creature):

    def __init__(self, x=0, y=0, game_token='', look_direction='down'):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/entities/creatures/half_dragon_assassin_sprite.png",
                         name="Half dragon assassin", game_token=game_token, look_direction=look_direction)
