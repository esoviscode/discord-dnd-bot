from dnd_bot.logic.prototype.creature import Creature


class HalfDragonWarrior(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/half_dragon_warrior_sprite.png"
    creature_name = "Half dragon warrior"

    def ai_action(self):
        return super().ai_action()
