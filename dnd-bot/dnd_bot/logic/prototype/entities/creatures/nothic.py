from dnd_bot.logic.prototype.creature import Creature


class Nothic(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/nothic_sprite.png"
    creature_name = "Nothic"

    def ai_action(self):
        return super().ai_action()
