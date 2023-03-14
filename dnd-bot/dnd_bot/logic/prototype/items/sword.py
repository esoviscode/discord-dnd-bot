from dnd_bot.logic.prototype.item import Item


class Sword(Item):

    def __init__(self):
        # TODO load item attributes from a json
        name = 'Sword'
        strength = 3
        base_price = 13

        super().__init__(name=name, strength=strength, base_price=base_price)
