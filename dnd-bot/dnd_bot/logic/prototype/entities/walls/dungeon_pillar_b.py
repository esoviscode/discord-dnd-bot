from dnd_bot.logic.prototype.entity import Entity


class DungeonPillarB(Entity):

    def __init__(self, x=0, y=0, game_token='', look_direction='down'):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/walls/dungeon_pillar_2.png",
                         name="Dungeon pillar B", game_token=game_token, look_direction=look_direction)
