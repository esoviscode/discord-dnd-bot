from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.database.database_user import DatabaseUser
from dnd_bot.logic.prototype.database_object import DatabaseObject


class User(DatabaseObject):
    """defines discord user"""

    def __init__(self, game_token: str = "", discord_id: int = 0, channel_id: int = 0, username: str = "",
                 color: str = "", is_host: bool = False):
        game_id = DatabaseGame.get_id_game_from_game_token(game_token)
        super().__init__(DatabaseUser.get_user_id_from_discord_id(discord_id, game_id))
        self.game_token = game_token
        self.discord_id = discord_id
        self.channel_id = channel_id
        self.username = username
        self.is_host = is_host
        self.is_ready = False
        self.color = color

    def __repr__(self):
        return f'<{self.username} id={self.discord_id} host={self.is_host}>'
