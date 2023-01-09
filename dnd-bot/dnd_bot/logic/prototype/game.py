from dnd_bot.logic.prototype.user import User
import copy

class Game:

    def __init__(self, token, id_host=None, id_campaign=None, game_state="LOBBY", user_list=None):
        if user_list is None:
            user_list = []
        self.id_host = id_host
        self.token = token
        self.id_campaign = id_campaign
        self.game_state = game_state

        self.user_list = user_list

    def add_player(self, user_id, user_channel_id, username):
        self.user_list.append(User(self.token, user_id, user_channel_id, username))

    def add_host(self, user_id, user_channel_id, username):
        self.id_host = user_id
        user = User(self.token, user_id, user_channel_id, username)
        user.is_host = True
        self.user_list.append(user)

    def all_users_ready(self):
        for user in self.user_list:
            if not user.is_ready:
                return False

        return True
