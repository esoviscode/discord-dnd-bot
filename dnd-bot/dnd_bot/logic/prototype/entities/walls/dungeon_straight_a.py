from dnd_bot.logic.prototype.entity import Entity


class DungeonStraightA(Entity):

    def __init__(self, id=0, x=0, y=0, game_token='', look_direction='down'):
        super().__init__(id=id, x=x, y=y, sprite="dnd_bot/assets/gfx/walls/dungeon_straight_1_black.png",
                         name="Dungeon straight A", game_token=game_token, look_direction=look_direction)
