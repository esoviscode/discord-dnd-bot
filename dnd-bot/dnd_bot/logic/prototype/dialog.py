from dnd_bot.logic.prototype.database_object import DatabaseObject


class Dialog(DatabaseObject):
    """represents a dialog in the game"""

    def __init__(self, id_speaker: int = 0, id_listener: int = 0, content: str = "", status: str = ""):
        ## TODO super().__init__(DatabaseDialog.add_dialog(id_speaker, id_listener, content, status))
        self.id_speaker = id_speaker
        self.id_listener = id_listener
        self.content = content
        self.status = status
