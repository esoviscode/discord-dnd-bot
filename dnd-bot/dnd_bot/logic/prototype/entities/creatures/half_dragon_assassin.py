from dnd_bot.logic.prototype.creature import Creature


class HalfDragonAssassin(Creature):
    sprite_path = "dnd_bot/assets/gfx/entities/creatures/half_dragon_assassin_sprite.png"
    creature_name = "Half dragon assassin"

    def ai_action(self):
        return super().ai_action()
