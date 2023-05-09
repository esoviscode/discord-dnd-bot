from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""

    def __init__(self, x=0, y=0, sprite: str = '', name: str = 'Creature', hp: int = 0, strength: int = 0,
                 dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 0, equipment: Equipment = Equipment(), drop_money=None,
                 game_token: str = '', look_direction: str = 'down', experience: int = 0,
                 creature_class: str = '', drops=None, ai=-1):
        super().__init__(x=x, y=y, sprite=sprite, name=name, fragile=True, game_token=game_token, look_direction=look_direction)
        if drop_money is None:
            drop_money = []
        if drops is None:
            drops = []

        self.hp = hp
        self.max_hp = hp
        self.base_strength = strength
        self.base_dexterity = dexterity
        self.base_intelligence = intelligence
        self.base_charisma = charisma
        self.base_perception = perception

        self.initiative = initiative
        self.action_points = action_points
        self.initial_action_points = action_points
        self.equipment = equipment
        self.level = level
        self.experience = experience
        self.creature_class = creature_class

        self.drop_money = drop_money
        self.drops = drops

        self.ai = ai  # -1: passive, 0: Warrior, 1: Ranger, 2: Mage
        self.move_queue = []

# ----------------------------------------------------- properties -----------------------------------------------------
    def eq_stats(self, stat):
        """returns additional "stat" value that comes from items in equipment"""
        from dnd_bot.logic.prototype.items.item import Item
        return sum([i.__getattribute__(stat) for i in self.equipment.__dict__.values() if isinstance(i, Item)])

    # future development
    # def effects_stats(self, stat):
    #     return sum([e.__getattribute__(stat) for e in self.effects])

    @property
    def strength(self):
        return self.base_strength + self.eq_stats("strength")

    @property
    def dexterity(self):
        return self.base_dexterity + self.eq_stats("dexterity")

    @property
    def intelligence(self):
        return self.base_intelligence + self.eq_stats("intelligence")

    @property
    def charisma(self):
        return self.base_charisma + self.eq_stats("charisma")

    @property
    def perception(self):
        return self.base_perception + self.eq_stats("perception")

    @property
    def defence(self):
        return self.eq_stats("defence")
# ----------------------------------------------------- properties -----------------------------------------------------

    async def ai_action(self):
        """perform certain ai action and returns its response
        :return: string"""
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.game.handler_attack import HandlerAttack

        if self.ai == -1:
            self.move_queue = [None]

        # prepare chain of actions move_queue is empty
        if not self.move_queue:
            self.move_queue = self.prepare_move_queue()

        while self.move_queue[0]:  # while action is not None - None goes for end turn
            # creature movement
            if self.move_queue[0][0] == 'M':
                self.move_one_tile(self.move_queue[0][1], Multiverse.get_game(self.game_token))
                self.action_points -= 1
                self.move_queue.pop(0)
                return f"{self.name} has moved to ({self.x},{self.y})"
            # creature attack
            elif self.move_queue[0][0] == 'A':
                req_action_points = self.equipment.right_hand.action_points if self.equipment.right_hand else 2
                if self.action_points >= req_action_points:
                    # attack foe
                    if Multiverse.get_game(self.game_token).entities[self.move_queue[0][1].y][self.move_queue[0][1].x]:
                        resp = await HandlerAttack.handle_attack(self, self.move_queue[0][1], self.game_token)
                        return resp
                    # foe killed
                    else:
                        self.move_queue = self.prepare_move_queue()
                # end turn
                else:
                    self.move_queue = [None]

        self.action_points = 0
        self.move_queue = []
        return "Idle"

    def visible_for_players(self):
        """return if creature is visible for players"""
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.prototype.player import Player
        from dnd_bot.logic.utils.utils import in_range

        players = [p for p in sum(Multiverse.get_game(self.game_token).entities, []) if isinstance(p, Player)]
        for p in players:
            if in_range(self.x, self.y, p.x, p.y, min(p.perception, 4)):
                return True
        return False

    @staticmethod
    def attackable(from_x, from_y, to_x, to_y, board):
        """returns if position is attackable no matter what attack range is
        :param from_x: my x
        :param from_y: my y
        :param to_x: target's x
        :param to_y: target's y
        :param board: 2d matrix - True/object when tile is occupied, False/None when tile is empty
        :return: bool"""
        from dnd_bot.logic.utils.utils import find_position_to_check

        positions = find_position_to_check(from_x, from_y, to_x, to_y)
        for pos in positions[1:-1]:
            if board[pos[1]][pos[0]]:
                return False
        return True

    @staticmethod
    def a_star_path(from_x, from_y, to_x, to_y, board):
        """returns list of points of an A* path
        :param from_x: x of start point
        :param from_y: y of start point
        :param to_x: x of end point
        :param to_y: y of end point
        :param board: 2d matrix - True/object when tile is occupied, False/None when tile is empty
        :return path: list of tuples (x, y)"""
        from pathfinding.core.grid import Grid
        from pathfinding.finder.a_star import AStarFinder

        matrix = [[0 if x else 1 for x in row] for row in board]
        matrix[to_y][to_x] = 1

        grid = Grid(matrix=matrix)
        start = grid.node(from_x, from_y)
        end = grid.node(to_x, to_y)

        return AStarFinder().find_path(start, end, grid)[0]
