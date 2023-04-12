from dnd_bot.logic.prototype.database_object import DatabaseObject


class Event(DatabaseObject):
    """represents various events that happen randomly in the game"""
    def __init__(self, x: int = 0, y: int = 0, range: int = 0, status: str = "", content: str = "", id_game:int = 0):
        ## TODO super().__init__(DatabaseEvent.add_event(x, y, range, status, content, id_game))
        self.x = x
        self.y = y
        self.range = range
        self.status = status
        self.content = content
        self.id_game = id_game
