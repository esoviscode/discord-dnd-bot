import math
from collections import deque

from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.database_object import DatabaseObject
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.prototype.user import User


class Game(DatabaseObject):
    """class represents particular games and lobbies"""

    def __init__(self, token: str = None, id_host: int = None, campaign_name: str = "", game_state: str = "LOBBY",
                 user_list=None, events=None, queue=None, world_width: int = 0, world_height: int = 0):
        super().__init__(DatabaseGame.get_id_game_from_game_token(token))
        if user_list is None:
            user_list = []
        if events is None:
            events = []
        self.id_host = id_host
        self.token = token
        self.campaign_name = campaign_name
        self.game_state = game_state
        self.user_list = user_list
        self.entities = []
        self.game_loop_thread = None
        self.sprite = None
        self.world_width = world_width
        self.world_height = world_height
        self.active_creature = None
        self.players_views = dict()  # this dict is to save the view non-active player is looking at;
        # key values are stringified discord ids and values are particular views

        # this queue contains all the creatures in current map that can possibly make move in a turn
        if queue is None:
            self.creatures_queue = deque()
        else:
            self.creatures_queue = queue
        self.events = events

    def add_player(self, user_id, user_channel_id, username, color):
        """adds player to the game
        :param user_id: users discord id
        :param user_channel_id: private discord channel id
        :param username: username
        :param color: string representing color
        :return: None
        """
        self.user_list.append(User(self.token, user_id, user_channel_id, username, color))

    def add_host(self, user: User):
        """ adds player as the host to the game
        :param user: user that is the host of the game
        :return: None
        """
        self.id_host = user.discord_id
        self.user_list.append(user)

    def find_user(self, discord_id):
        """returns user by discord id, returns None if not successful"""
        for u in self.user_list:
            if u.discord_id == discord_id:
                return u

        return None

    def get_entity_by_id(self, entity_id):
        for entity_row in self.entities:
            for entity in entity_row:
                if entity and entity.id == int(entity_id):
                    return entity
        return None

    def delete_entity(self, entity_id):
        entity = self.get_entity_by_id(entity_id)
        x = entity.x
        y = entity.y

        self.entities[y].remove(entity)
        self.entities[y].insert(x, None)

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

    def get_user_by_id(self, id_user) -> User | None:
        """finds user by his id"""
        for user in self.user_list:
            if user.discord_id == id_user:
                return user

        return None

    def get_movable_entities(self):
        """returns all entities which are able to move"""
        movable_entities = []
        for entity_row in self.entities:
            for entity in entity_row:
                if isinstance(entity, Creature):
                    movable_entities.append(entity)
        return movable_entities

    def get_active_creature(self):
        """returns current active player"""
        return self.active_creature

    def get_attackable_enemies_for_player(self, player):
        creatures = self.get_movable_entities()
        result = []
        weapon = player.equipment.right_hand
        if weapon is None:
            return result

        def find_position_to_check(x_src=0, y_src=0, x_dest=1, y_dest=1):
            result = []

            def find_positions(x1, y1, x2, y2, dx, dy, decide):
                pk = 2 * dy - dx
                for i in range(0, dx + 1):
                    if decide == 0:
                        result.append((x1, y1))
                    else:
                        result.append((y1, x1))

                    if x1 < x2:
                        x1 = x1 + 1
                    else:
                        x1 = x1 - 1
                    if pk < 0:

                        if decide == 0:
                            pk = pk + 2 * dy
                        else:
                            pk = pk + 2 * dy
                    else:
                        if y1 < y2:
                            y1 = y1 + 1
                        else:
                            y1 = y1 - 1

                        pk = pk + 2 * dy - 2 * dx

            dx = abs(x_dest - x_src)
            dy = abs(y_dest - y_src)

            # If slope is less than one
            if dx > dy:
                find_positions(x_src, y_src, x_dest, y_dest, dx, dy, 0)
            # if slope is greater than or equal to 1
            else:
                find_positions(y_src, x_src, y_dest, x_dest, dy, dx, 1)

            return result[1:-1]

        attack_range = min(weapon.use_range, player.perception)
        for creature in creatures:
            if not isinstance(creature, Player):
                # check if creature is in player's range circle
                # mod is conditional variable which defines proper circles
                mod = 1
                if 3 <= attack_range < 6:
                    mod = 3
                elif attack_range >= 6:
                    mod = 4
                if (player.x - creature.x)**2 + (player.y - creature.y)**2 <= attack_range**2 + mod:
                    add = True
                    positions = find_position_to_check(player.x, player.y, creature.x, creature.y)
                    for pos in positions:
                        if self.entities[pos[1]][pos[0]]:
                            add = False
                            break
                    if add:
                        result.append(creature)

        return result
