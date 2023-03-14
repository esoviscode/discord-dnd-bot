from dnd_bot.logic.prototype.creature import Creature


class LizardfolkArcher(Creature):

    sprite_path = "dnd_bot/assets/gfx/entities/creatures/lizardfolk_archer.png"
    creature_name = "Lizardfolk archer"

    def ai_action(self):
        return super().ai_action()
