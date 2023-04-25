from dnd_bot.logic.prototype.entity import Entity
from dnd_bot.logic.prototype.equipment import Equipment


class Creature(Entity):
    """represents a creature"""

    def __init__(self, x=0, y=0, sprite: str = '', name: str = 'Creature', hp: int = 0, strength: int = 0,
                 dexterity: int = 0, intelligence: int = 0, charisma: int = 0, perception: int = 0, initiative: int = 0,
                 action_points: int = 0, level: int = 0, equipment: Equipment = None, drop_money = None,
                 game_token: str = '', look_direction: str = 'down', experience: int = 0,
                 creature_class: str = '', drops=None, ai=0):
        super().__init__(x=x, y=y, sprite=sprite, name=name, fragile=True, game_token=game_token, look_direction=look_direction)
        if drop_money is None:
            drop_money = []
        if drops is None:
            drops = []
        self.hp = hp
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
        self.ai = self.ai_simple_move

    def ai_action(self):
        from dnd_bot.logic.prototype.multiverse import Multiverse
        from dnd_bot.logic.utils.utils import find_position_to_check

        foes = self.search_for_foes()
        if not foes:
            self.action_points = 0
            return self.ai()

        print(self.name, "has foes in range")
        path_exists = False
        for f in foes:
            path = Creature.a_star_path(self.x, self.y, f.x, f.y, Multiverse.get_game(self.game_token).entities)
            if path:
                path_exists = True
            print(f"Foe: {f.name}, path: {path}")

        if not path_exists:
            self.action_points = 0
            return self.ai()

        path = Creature.a_star_path(self.x, self.y, foes[0].x, foes[0].y, Multiverse.get_game(self.game_token).entities)
        path = path[1:]

        mod = 1
        try:
            if not self.equipment.right_hand:
                attack_range = 1
            else:
                attack_range = min(self.perception, self.equipment.right_hand.use_range)
        except Exception:
            attack_range = 1

        if 3 < attack_range < 6:
            mod = 4
        elif attack_range >= 6:
            mod = 5

        def attackable(from_x, from_y, to_x, to_y):
            positions = find_position_to_check(from_x, from_y, to_x, to_y)
            for pos in positions:
                if Multiverse.get_game(self.game_token).entities[pos[1]][pos[0]]:
                    return False
            return True

        while (not (attackable(self.x, self.y, path[-1][0], path[-1][1])
                    and ((self.x - path[-1][0]) ** 2 + (self.y - path[-1][1]) ** 2 <= attack_range ** 2 + mod))
               ) and (self.action_points > 0):
            if self.x - path[0][0] != 0:
                direction = "right" if self.x < path[0][0] else "left"
            else:
                direction = "down" if self.y < path[0][1] else "up"
            self.move_one_tile(direction, Multiverse.get_game(self.game_token))
            print(self.name, "moved to", (self.x, self.y))
            path.pop(0)
            self.action_points -= 1

        self.action_points = 0
        return "Pathing to target"

    def ai_simple_move(self):
        return "Made simple move"

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
