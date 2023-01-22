from dnd_bot.logic.prototype.entity import Entity


class DungeonConnector(Entity):

    def __init__(self, x=0, y=0, game_token=''):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/walls/dungeon_connector.png",
                         name="Dungeon connector", game_token=game_token)
