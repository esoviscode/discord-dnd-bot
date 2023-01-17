class User:
    """defines discord user"""

    def __init__(self, id_game, discord_id, channel_id, username):
        self.id_game = id_game
        self.discord_id = discord_id
        self.channel_id = channel_id
        self.username = username
        self.is_host = False
        self.is_ready = False
