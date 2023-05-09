import copy
import dnd_bot.logic.prototype.player
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

        # prepare chain of actions move_queue is empty
        if not self.move_queue:
            self.move_queue = self.prepare_move_queue()

        if self.ai == -1:
            self.move_queue = [None]

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

    def visible_for_players(self):
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.prototype.player import Player
        from dnd_bot.logic.utils.utils import in_range

        players = [p for p in sum(Multiverse.get_game(self.game_token).entities, []) if isinstance(p, Player)]
        for p in players:
            if in_range(self.x, self.y, p.x, p.y, min(p.perception, 4)):
                return True
        return False

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

    def prepare_move_queue(self):
        """prepare chain of creature's actions depending on current game state
        M dir - stands for move to direction dir
        A target - stands for attack the target"""
        if self.action_points == 0:
            return [None]

        from dnd_bot.logic.prototype.multiverse import Multiverse

        action_points = self.action_points
        foes = self.search_for_foes()
        if not foes:
            return [None]

        low_hp = 5
        if self.hp <= low_hp and self.ai == 2:  # low hp behaviour for Mages
            actions = self.flee()
            if actions == list():  # is safe
                return [None]
            elif actions:  # pathing to escape danger
                moves = []
                for i, p in enumerate(actions[:-1]):
                    if p[0] - actions[i + 1][0] != 0:
                        direction = "right" if p[0] < actions[i + 1][0] else "left"
                    else:
                        direction = "down" if p[1] < actions[i + 1][1] else "up"
                    moves.append(('M', direction))
                return moves + [None]
            # can't run away

        # normal actions find target and path to it
        target, path = self.choose_aggro(foes)
        if not target:
            return [None]

        move_queue = []
        if self.hp <= low_hp and self.ai == 1:  # low hp behaviour for rangers
            actions = self.kite(target)
            if actions:
                return actions

        if self.equipment.right_hand:
            attack_range = min(self.perception, self.equipment.right_hand.use_range)
        else:
            attack_range = 1

        from dnd_bot.logic.utils.utils import in_range

        # while (not(target is attackable) and (target is in attack range)) and enough actions points
        while (not (Creature.attackable(path[0][0], path[0][1], path[-1][0], path[-1][1],
                                        Multiverse.get_game(self.game_token).entities)
                    and in_range(path[0][0], path[0][1], path[-1][0], path[-1][1], attack_range))
               ) and (action_points > 0):
            if path[0][0] - path[1][0] != 0:
                direction = "right" if path[0][0] < path[1][0] else "left"
            else:
                direction = "down" if path[0][1] < path[1][1] else "up"

            move_queue.append(('M', direction))
            path.pop(0)
            action_points -= 1

        # can attack
        req_action_points = self.equipment.right_hand.action_points if self.equipment.right_hand else 2
        move_queue.append(('A', target) if action_points >= req_action_points else None)

        return move_queue

    def search_for_foes(self):
        """returns list of Players in creature's view range
        :return: list of Player objects"""
        from dnd_bot.logic.utils.utils import generate_circle_points
        from dnd_bot.logic.prototype.player import Player
        from dnd_bot.logic.prototype.multiverse import Multiverse

        game = Multiverse.get_game(self.game_token)
        points = generate_circle_points(self.perception, self.perception)
        foes = []

        for p in points:
            x, y = self.x - p[0], self.y - p[1]
            if 0 <= x < game.world_width and 0 <= y < game.world_height and isinstance(game.entities[y][x], Player):
                foes.append(game.entities[y][x])
        return foes

    def choose_aggro(self, foes):
        """choose which Player from foes to attack
        :param foes: list of Player objects
        :return target: tuple (Player object, path)"""
        from dnd_bot.logic.prototype.multiverse import Multiverse

        intelligence = "high" if self.intelligence >= 10 else ("low" if self.intelligence <= 3 else "medium")
        if intelligence != "low":
            class_priority = ["Mage", "Ranger", "Warrior"]
        sorted_foes = []

        def sort_foes():
            """adds foe to the list with specific priority"""
            i = 0
            if intelligence == "low":
                while i < len(sorted_foes):
                    if len(sorted_foes[i][1]) < path_len:
                        i += 1
                    else:
                        break
                sorted_foes.insert(i, (f, path))
            elif intelligence == "medium":
                while i < len(sorted_foes):
                    if class_priority.index(sorted_foes[i][0].creature_class) < \
                            class_priority.index(f.creature_class):
                        i += 1
                    elif len(sorted_foes[i][1]) < path_len:
                        i += 1
                    else:
                        break
                sorted_foes.insert(i, (f, path))
            else:  # high
                while i < len(sorted_foes):
                    if sorted_foes[i][0].hp < f.hp:
                        i += 1
                    elif class_priority.index(sorted_foes[i][0].creature_class) < \
                            class_priority.index(f.creature_class):
                        i += 1
                    elif len(sorted_foes[i][1]) < path_len:
                        i += 1
                    else:
                        break
                sorted_foes.insert(i, (f, path))

        # add foes to list and order them by specific priority
        for f in foes:
            path = Creature.a_star_path(self.x, self.y, f.x, f.y, Multiverse.get_game(self.game_token).entities)
            path_len = len(path)
            if path:  # if there is a path to the foe
                sort_foes()
            else:
                from dnd_bot.logic.prototype.multiverse import Multiverse
                from dnd_bot.logic.utils.utils import generate_circle_points
                game = Multiverse.get_game(f.game_token)
                best_path = [None] * (game.world_width * game.world_height)
                attack_range = min(self.perception, self.equipment.right_hand.use_range
                                   if self.equipment.right_hand else 1)
                points = generate_circle_points(attack_range, attack_range)

                entities = copy.deepcopy(game.entities)
                entities[self.y][self.x] = None
                for x, y in points:
                    if not (0 <= f.x - x < game.world_width and 0 <= f.y - y < game.world_height):
                        continue
                    if not entities[f.y - y][f.x - x]:
                        path = Creature.a_star_path(self.x, self.y, f.x - x, f.y - y, entities)
                        if (not path) or (not Creature.attackable(f.x - x, f.y - y, f.x, f.y, entities)):
                            continue
                        if len(best_path) > len(path):
                            if self.action_points >= len(path) - 1:
                                best_path = path
                # if there is a pos where you can't path to the foe, but can attack him
                if len(best_path) < game.world_width * game.world_height:
                    sort_foes()

        if sorted_foes:  # highest priority
            return sorted_foes[0]
        else:  # no pathing to any of foes
            return None, []

    def flee(self):
        """run away from danger
        :return: path or None"""
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.utils.utils import generate_circle_points

        game = Multiverse.get_game(self.game_token)
        entities = game.entities
        simulation = copy.deepcopy(entities)
        simulation[self.y][self.x] = None

        # points safe from any player's attack range
        safe_points = [[False if e else True for e in row] for row in simulation]

        # eliminate unsafe points
        for row in simulation:
            for e in row:
                if e and isinstance(e, dnd_bot.logic.prototype.player.Player):
                    if e.equipment.right_hand:
                        attack_range = min(e.perception, e.equipment.right_hand.use_range)
                    else:
                        attack_range = 1
                    points = generate_circle_points(attack_range, attack_range)

                    for x, y in points:
                        if not (0 <= e.x - x < game.world_width and 0 <= e.y - y < game.world_height):
                            continue
                        if (not simulation[e.y - y][e.x - x]) and Creature.attackable(e.x, e.y, e.x - x, e.y - y, simulation):
                            safe_points[e.y - y][e.x - x] = False

        if safe_points[self.y][self.x]:  # if current position is safe
            return []

        # choose path to the nearest safe point
        best_path = [None] * (game.world_width * game.world_height)
        for y, row in enumerate(safe_points):
            for x, p in enumerate(row):
                if p:
                    path = Creature.a_star_path(self.x, self.y, x, y, entities)
                    if not path:
                        continue
                    if len(best_path) > len(path):
                        if self.action_points >= len(path) - 1:
                            best_path = path

        return best_path if len(best_path) < (game.world_width * game.world_height) else None

    def kite(self, target):
        """kite away the chosen target
        :param target: Player object
        :return moves: chain of actions"""
        from dnd_bot.logic.utils.utils import generate_circle_points, in_range
        from dnd_bot.logic.prototype.multiverse import Multiverse

        moves = []
        if self.equipment.right_hand:
            attack_range = max(self.equipment.right_hand.use_range, self.perception)
        else:
            attack_range = 1
        points = generate_circle_points(attack_range, attack_range)
        wages = [0 for _ in points]

        game = Multiverse.get_game(self.game_token)
        entities = game.entities
        simulation = copy.deepcopy(entities)
        simulation[self.y][self.x] = None

        # choose best position
        for i, (x, y) in enumerate(points):
            if not simulation[target.y - y][target.x - x] and \
                    Creature.attackable(target.x - x, target.y - y, target.x, target.y, simulation) and \
                    (0 <= target.x - x < game.world_width and 0 <= target.y - y < game.world_height):
                # heuristics
                path_len = len(Creature.a_star_path(self.x, self.y, x, y, simulation)) - 1
                if path_len > self.action_points:
                    continue

                wages[i] += 25  # point in my attack range

                # path's length to that point
                wages[i] -= path_len if path_len >= 0 else game.world_width * game.world_height

                # dist from target
                wages[i] += (len(Creature.a_star_path(x, y, target.x, target.y, simulation)) - 1) ** 2

                # in target's attack range
                if Creature.attackable(target.x, target.y, x, y, simulation) \
                        and in_range(target.x, target.y, x, y,
                                     min(target.perception, target.equipment.right_hand.use_range)):
                    wages[i] -= 10

        best_wage = max(wages)
        if best_wage == 0:  # all are bad
            return []
        best_pos = points[wages.index(best_wage)]
        path = Creature.a_star_path(self.x, self.y, target.x - best_pos[0], target.y - best_pos[1], entities)

        # prepare chain of actions
        for i, p in enumerate(path[:-1]):
            if p[0] - path[i + 1][0] != 0:
                direction = "right" if p[0] < path[i + 1][0] else "left"
            else:
                direction = "down" if p[1] < path[i + 1][1] else "up"
            moves.append(('M', direction))
        moves.append(('A', target))

        return moves
