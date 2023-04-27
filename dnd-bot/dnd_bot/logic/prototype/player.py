from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.entities.misc.corpse import Corpse
from dnd_bot.logic.prototype.items.item import Item
from dnd_bot.logic.prototype.multiverse import Multiverse


class Player(Creature):
    """represents a player (which is controlled by a user)"""

    def __init__(self, entity_id=0, x=0, y=0, name: str = 'Player',
                 hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0, charisma: int = 0,
                 perception: int = 0, initiative: int = 0, action_points: int = 0, level: int = 1,
                 discord_identity: int = 0, alignment: str = '', backstory: str = '',
                 game_token: str = '', character_race: str = '', character_class: str = '', experience: int = 0,
                 backpack=None, money: int = 0):

        # request a sprite path for the player based on the user
        if backpack is None:
            backpack = []
        self.sprite = None
        game = Multiverse.get_game(game_token)
        if game is None:
            print('Warning: this player has no associated Game!')
        else:
            user = game.get_user_by_id(discord_identity)
            if user is None:
                print('Warning: this player has no associated User!')
            else:
                self.sprite = self.get_sprite_path_by_color(user.color, character_class)

        super().__init__(x=x, y=y, sprite=self.sprite, name=name, hp=hp, strength=strength, dexterity=dexterity,
                         intelligence=intelligence, charisma=charisma, perception=perception, initiative=initiative,
                         action_points=action_points, level=level, game_token=game_token, experience=experience,
                         creature_class=character_class)

        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.character_race = character_race
        self.active = False
        self.attack_mode = False
        self.backpack = backpack  # Player_item in database
        self.money = money

    def get_sprite_path_by_color(self, color: str, character_class: str):
        import os

        path = f'dnd_bot/assets/gfx/entities/{character_class.lower()}_sprite_{color}.png'
        if os.path.isfile(path):
            return path
        else:
            return 'dnd_bot/assets/gfx/entities/player.png'

    def get_entities_around(self, cross_only=False):
        """ returns all entities around(next to) the player.
        :param cross_only: if True function won't return entities on diagonal"""
        game = Multiverse.get_game(self.game_token)
        result = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0) or (cross_only and (x + y == 0 or x + y == -2 or x + y == 2)):
                    continue
                if game.entities[self.y + y][self.x + x]:
                    result.append(game.entities[self.y + y][self.x + x])

        return result

    @property
    def can_loot_corpse(self):
        for entity in self.get_entities_around(cross_only=True):
            if isinstance(entity, Corpse):
                return True
        return False

    def add_items(self, dropped_items):
        """ universal system for adding items
        :param dropped_items - LIST of items to add
        """
        self.backpack += dropped_items
        self.backpack.sort(key=Item.compare_items)

    def add_money(self, money):
        """ universal system for adding money """
        self.money += money
