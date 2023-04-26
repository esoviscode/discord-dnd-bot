import copy
import dnd_bot.logic.prototype.player
from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""

    def __init__(self, x=0, y=0, sprite: str = '', name: str = 'Creature', hp: int = 0, strength: int = 0,
                 dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 0, equipment: Equipment = None, drop_money=None,
                 game_token: str = '', look_direction: str = 'down', experience: int = 0,
                 creature_class: str = '', drops=None, ai=0):
        super().__init__(x=x, y=y, sprite=sprite, name=name, fragile=True, game_token=game_token, look_direction=look_direction)
        if drop_money is None:
            drop_money = []
        if drops is None:
            drops = []
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.perception = perception
        self.initiative = initiative
        self.action_points = action_points
        self.level = level
        self.equipment = equipment
        self.drop_money = drop_money
        self.initial_action_points = action_points
        self.experience = experience
        self.creature_class = creature_class
        self.drops = drops

        # TODO set ai function depending on ai argument
        self.ai = ai
        self.move_queue = []

    async def ai_action(self):
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.game.handler_attack import HandlerAttack

        if not self.move_queue:
            self.move_queue = self.prepare_move_queue()

        while self.move_queue[0]:
            # creature movement
            if self.move_queue[0][0] == 'M':
                self.move_one_tile(self.move_queue[0][1], Multiverse.get_game(self.game_token))
                self.action_points -= 1
                self.move_queue.pop(0)
                return f"{self.name} has moved to ({self.x},{self.y})"

            elif self.move_queue[0][0] == 'A':
                if (self.equipment.right_hand and self.equipment.right_hand.action_points >= self.action_points) \
                        or self.action_points >= 2:
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

    def search_for_foes(self):
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

    @staticmethod
    def a_star_path(from_x, from_y, to_x, to_y, board):
        from pathfinding.core.grid import Grid
        from pathfinding.finder.a_star import AStarFinder

        matrix = [[0 if x else 1 for x in row] for row in board]
        matrix[to_y][to_x] = 1

        grid = Grid(matrix=matrix)
        start = grid.node(from_x, from_y)
        end = grid.node(to_x, to_y)

        return AStarFinder().find_path(start, end, grid)[0]

    def prepare_move_queue(self):
        if self.action_points == 0:
            return [None]

        from dnd_bot.logic.prototype.multiverse import Multiverse

        action_points = self.action_points
        foes = self.search_for_foes()
        if not foes:
            return [None]

        # artificial intelligence
        low_hp = 5
        if self.hp <= low_hp and self.ai == 2:
            actions = self.flee()
            if actions == list():
                return [None]
            elif actions:
                moves = []
                for i, p in enumerate(actions[:-1]):
                    if p[0] - actions[i + 1][0] != 0:
                        direction = "right" if p[0] < actions[i + 1][0] else "left"
                    else:
                        direction = "down" if p[1] < actions[i + 1][1] else "up"
                    moves.append(('M', direction))
                return moves + [None]

        target, path = self.choose_aggro(foes)
        if not target:
            return [None]

        move_queue = []
        if self.hp <= low_hp and self.ai == 1:
            actions = self.kite(target)
            if actions:
                return actions

        if self.equipment.right_hand:
            attack_range = min(self.perception, self.equipment.right_hand.use_range)
        else:
            attack_range = 1

        bias = 1
        if 3 < attack_range < 6:
            bias = 4
        elif attack_range >= 6:
            bias = 5

        while (not (Creature.attackable(path[0][0], path[0][1], path[-1][0], path[-1][1],
                                        Multiverse.get_game(self.game_token).entities)
                    and ((path[0][0] - path[-1][0]) ** 2 + (path[0][1] - path[-1][1]) ** 2 <= attack_range ** 2 + bias))
               ) and (action_points > 0):
            if path[0][0] - path[1][0] != 0:
                direction = "right" if path[0][0] < path[1][0] else "left"
            else:
                direction = "down" if path[0][1] < path[1][1] else "up"

            move_queue.append(('M', direction))
            path.pop(0)
            action_points -= 1

        move_queue.append(('A', foes[0]) if action_points > 0 else None)

        return move_queue

    def choose_aggro(self, foes):
        from dnd_bot.logic.prototype.multiverse import Multiverse

        intelligence = "high" if self.intelligence >= 10 else ("low" if self.intelligence <= 3 else "medium")
        if intelligence != "low":
            class_priority = ["Mage", "Ranger", "Warrior"]
        sorted_foes = []

        for f in foes:
            path = Creature.a_star_path(self.x, self.y, f.x, f.y, Multiverse.get_game(self.game_token).entities)
            path_len = len(path)
            if path:
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
                else:
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

        if sorted_foes:
            return sorted_foes[0]
        else:
            return None, []

    def flee(self):
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.utils.utils import generate_circle_points

        game = Multiverse.get_game(self.game_token)
        entities = game.entities
        initial = copy.deepcopy(entities)
        initial[self.y][self.x] = None

        safe_points = [[False if e else True for e in row] for row in initial]

        for row in initial:
            for e in row:
                if e and isinstance(e, dnd_bot.logic.prototype.player.Player):
                    # eliminate unsafe points
                    if e.equipment.right_hand:
                        attack_range = min(e.perception, e.equipment.right_hand.use_range)
                    else:
                        attack_range = 1
                    points = generate_circle_points(attack_range, attack_range)

                    for x, y in points:
                        if not (0 <= e.x - x < game.world_width and 0 <= e.y - y < game.world_height):
                            continue
                        if (not initial[e.y - y][e.x - x]) and Creature.attackable(e.x, e.y, e.x - x, e.y - y, initial):
                            safe_points[e.y - y][e.x - x] = False

        if safe_points[self.y][self.x]:
            return []

        best_path = [None] * (game.world_width * game.world_height)
        for y, row in enumerate(safe_points):
            for x, p in enumerate(row):
                if p:
                    path = Creature.a_star_path(self.x, self.y, x, y, entities)
                    if not path:
                        continue
                    if len(best_path) > len(path):
                        if self.action_points >= len(path) - 1:
                            print("prev", best_path, "curr", path)
                            best_path = path

        return best_path if len(best_path) < (game.world_width * game.world_height) else None

    def kite(self, target):
        from dnd_bot.logic.utils.utils import generate_circle_points
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
        initial = copy.deepcopy(entities)
        initial[self.y][self.x] = None

        for i, (x, y) in enumerate(points):
            if not initial[target.y - y][target.x - x] and \
                    Creature.attackable(target.x - x, target.y - y, target.x, target.y, initial) and \
                    (0 <= target.x - x < game.world_width and 0 <= target.y - y < game.world_height):
                # heuristics
                path_len = len(Creature.a_star_path(self.x, self.y, x, y, initial)) - 1
                if path_len > self.action_points:
                    continue
                wages[i] += 25
                wages[i] -= path_len if path_len >= 0 else game.world_width * game.world_height
                wages[i] += (len(Creature.a_star_path(x, y, target.x, target.y, initial)) - 1) ** 2  # dist from target
                if Creature.attackable(target.x, target.y, x, y, initial):  # in foe's range
                    wages[i] -= 10

        best_wage = max(wages)
        if best_wage == 0:
            return []
        best_pos = points[wages.index(best_wage)]
        path = Creature.a_star_path(self.x, self.y, target.x - best_pos[0], target.y - best_pos[1], entities)

        for i, p in enumerate(path[:-1]):
            if p[0] - path[i + 1][0] != 0:
                direction = "right" if p[0] < path[i + 1][0] else "left"
            else:
                direction = "down" if p[1] < path[i + 1][1] else "up"
            moves.append(('M', direction))
        moves.append(('A', target))

        return moves

    @staticmethod
    def attackable(from_x, from_y, to_x, to_y, board):
        from dnd_bot.logic.utils.utils import find_position_to_check

        positions = find_position_to_check(from_x, from_y, to_x, to_y)
        for pos in positions:
            if board[pos[1]][pos[0]]:
                return False
        return True
