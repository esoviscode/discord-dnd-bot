from dnd_bot.logic.prototype.entity import Entity


class DungeonCrossroads(Entity):

    def __init__(self, x=0, y=0, game_token='', look_direction='down'):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/walls/dungeon_crossroads.png",
                         name="Dungeon crossroads", game_token=game_token, look_direction=look_direction)
