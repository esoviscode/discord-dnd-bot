import random

from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.multiverse import Multiverse


class Player(Creature):
    """represents a player (which is controlled by a user)"""

    def __init__(self, entity_id=0, x=0, y=0, sprite="dnd_bot/assets/gfx/entities/player.png", name: str = 'Player',
                 hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0, charisma: int = 0,
                 perception: int = 0, initiative: int = 0, action_points: int = 0, level: int = 1,
                 discord_identity: int = 0, alignment: str = '', backstory: str = '', equipment: Equipment = None,
                 game_token: str = ''):

        # TODO remove this - it generates some random values for now
        hp = random.randint(15, 30)
        strength = random.randint(1, 5)
        dexterity = random.randint(1, 5)
        intelligence = random.randint(1, 5)
        charisma = random.randint(1, 5)
        perception = random.randint(2, 4)
        initiative = random.randint(1, 5)
        action_points = random.randint(5, 10)
        # TODO remove above

        self.sprite = Player.get_sprite_path_by_color(Multiverse.get_game(game_token).
                                                      get_user_by_id(discord_identity).color)

        super().__init__(x=x, y=y, sprite=self.sprite, name=name, hp=hp, strength=strength, dexterity=dexterity,
                         intelligence=intelligence, charisma=charisma, perception=perception, initiative=initiative,
                         action_points=action_points, level=level, game_token=game_token)

        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.equipment = equipment
        self.active = False
        self.initial_action_points = action_points

    @staticmethod
    def get_sprite_path_by_color(color: str):
        if color == 'red':
            return 'dnd_bot/assets/gfx/entities/ranger_sprite_red.png'
        elif color == 'blue':
            return 'dnd_bot/assets/gfx/entities/wizard_sprite_blue.png'
        elif color == 'green':
            return 'dnd_bot/assets/gfx/entities/ranger_sprite_green.png'
        elif color == 'orange':
            return 'dnd_bot/assets/gfx/entities/warrior_sprite_orange.png'
        elif color == 'yellow':
            return 'dnd_bot/assets/gfx/entities/warrior_sprite_yellow.png'
        elif color == 'purple':
            return 'dnd_bot/assets/gfx/entities/wizard_sprite_purple.png'
        else:
            return 'dnd_bot/assets/gfx/entities/player.png'
