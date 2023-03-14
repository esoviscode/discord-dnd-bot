from dnd_bot.logic.prototype.item import Item


class Staff(Item):

    def __init__(self):
        # TODO load item attributes from a json
        name = 'Staff'
        intelligence = 5
        base_price = 20

        super().__init__(name=name, intelligence=intelligence, base_price=base_price)
