from dnd_bot.logic.prototype.creature import Creature


class FrostMage(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/frost_mage_sprite.png"
    creature_name = "Frost mage"

    def ai_action(self):
        return super().ai_action()


