class User:
    """defines discord user"""

    def __init__(self, id_game: int = 0, discord_id: int = 0, channel_id: int = 0, username: str = "", color: str = ""):
        self.id_game = id_game
        self.discord_id = discord_id
        self.channel_id = channel_id
        self.username = username
        self.is_host = False
        self.is_ready = False
        self.color = color

    def __repr__(self):
        return f'<{self.username} id={self.discord_id} host={self.is_host}>'
