import copy

from dnd_bot.logic.prototype.user import User
from queue import Queue
from collections import deque

class Game:
    """class represents particular games and lobbies"""
    def __init__(self, token, id_host=None, id_campaign=None, game_state="LOBBY", user_list=None, events=None, queue=None):
        if user_list is None:
            user_list = []
        if events is None:
            events = []
        self.id_host = id_host
        self.token = token
        self.id_campaign = id_campaign
        self.game_state = game_state
        self.user_list = user_list
        self.entities = []

        # this queue contains all the creatures in current map that can possibly make move in a turn
        if queue is None:
            self.creatures_queue = deque()
        self.events = events

    # def __deepcopy__(self, memodict={}):
    #     queue = copy.deepcopy(self.creatures_queue)
    #     return Game(self, self.token, id_host=self.id_host, id_campaign=self.id_campaign, game_state=self.game_state,
    #                 user_list=self.user_list, events=self.events, queue=queue)

    def add_player(self, user_id, user_channel_id, username):
        """adds player to the game
        :param user_id: users discord id
        :param user_channel_id: private discord channel id
        :param username: username
        :return: None
        """
        self.user_list.append(User(self.token, user_id, user_channel_id, username))

    def add_host(self, user_id, user_channel_id, username):
        """ adds player as the host to the game
        :param user_id: users discord id
        :param user_channel_id: private discord channel id
        :param username: username
        :return: None
        """
        self.id_host = user_id
        user = User(self.token, user_id, user_channel_id, username)
        user.is_host = True
        self.user_list.append(user)

    def find_user(self, discord_id):
        for u in self.user_list:
            if u.discord_id == discord_id:
                return u

        return None

    def all_users_ready(self):
        """checks if all users in lobby are ready"""
        for user in self.user_list:
            if not user.is_ready:
                return False

        return True
