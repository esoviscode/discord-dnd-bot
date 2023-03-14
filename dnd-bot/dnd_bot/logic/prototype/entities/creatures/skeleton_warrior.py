from dnd_bot.logic.prototype.creature import Creature


class SkeletonWarrior(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/skeleton_warrior_sprite.png"
    creature_name = "Skeleton warrior"

    def ai_action(self):
        return super().ai_action()
