from dnd_bot.logic.prototype.creature import Creature


class SkeletonMorningstar(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/skeleton_morningstar_sprite.png"
    creature_name = "Skeleton morningstar"

    def ai_action(self):
        return super().ai_action()
