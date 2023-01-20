from collections import deque

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.user import User


class Game:
    """class represents particular games and lobbies"""

    def __init__(self, token, id_host=None, id_campaign=None, game_state="LOBBY", user_list=None, events=None,
                 queue=None):
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
        self.game_loop_thread = None
        self.sprite = None

        # this queue contains all the creatures in current map that can possibly make move in a turn
        if queue is None:
            self.creatures_queue = deque()
        self.events = events

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
        """returns user by discord id, returns None if not successful"""
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

    def get_player_by_id_user(self, id_user):
        """finds player by host's discord id, returns Player(Creature) if successful, None otherwise """
        for entity_row in self.entities:
            for entity in entity_row:
                if isinstance(entity, Player):
                    if entity.discord_identity == id_user:
                        return entity
        return None

    def get_movable_entities(self):
        """returns all entities which are able to move"""
        movable_entities = []
        for entity_row in self.entities:
            for entity in entity_row:
                if isinstance(entity, Creature):
                    movable_entities.append(entity)
        return movable_entities

    def get_active_player(self):
        """returns current active player"""
        for entity_row in self.entities:
            for entity in entity_row:
                if isinstance(entity, Player) and entity.active:
                    return entity
