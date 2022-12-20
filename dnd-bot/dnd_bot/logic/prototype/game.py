from dnd_bot.logic.prototype.user import User


class Game:

    def __init__(self, id_host):
        self.id_host = id_host
        self.password = None
        self.id_campaign = None
        self.game_state = None
        self.user_list = []
        self.token = 73473

    def add_player(self, user_id, user_channel_id):
        self.user_list.append(User(self.token, user_id, user_channel_id))
