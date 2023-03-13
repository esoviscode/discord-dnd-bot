from dnd_bot.logic.prototype.creature import Creature


class SkeletonWarrior(Creature):

    def __init__(self, x=0, y=0, game_token='', look_direction='down', action_points=0):
        super().__init__(x=x, y=y, sprite="dnd_bot/assets/gfx/entities/creatures/skeleton_warrior_sprite.png",
                         name="Skeleton warrior", game_token=game_token, look_direction=look_direction, action_points=action_points)
