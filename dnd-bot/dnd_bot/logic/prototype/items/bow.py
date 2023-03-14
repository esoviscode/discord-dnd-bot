from dnd_bot.logic.prototype.item import Item


class Bow(Item):
    
    def __init__(self):
        # TODO load item attributes from a json
        name = 'Bow'
        dexterity = 4
        base_price = 15

        super().__init__(name=name, dexterity=dexterity, base_price=base_price)
