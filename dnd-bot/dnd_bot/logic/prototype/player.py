from dnd_bot.logic.prototype.creature import Creature
from dnd_bot.logic.prototype.equipment import Equipment
from dnd_bot.logic.prototype.multiverse import Multiverse


class Player(Creature):
    """represents a player (which is controlled by a user)"""

    def __init__(self, entity_id=0, x=0, y=0, name: str = 'Player',
                 hp: int = 0, strength: int = 0, dexterity: int = 0, intelligence: int = 0, charisma: int = 0,
                 perception: int = 0, initiative: int = 0, action_points: int = 0, level: int = 1,
                 discord_identity: int = 0, alignment: str = '', backstory: str = '',
                 game_token: str = '', character_race: str = '', character_class: str = '', experience: int = 0):

        # request a sprite path for the player based on the user
        self.sprite = None
        game = Multiverse.get_game(game_token)
        if game is None:
            print('Warning: this player has no associated Game!')
        else:
            user = game.get_user_by_id(discord_identity)
            if user is None:
                print('Warning: this player has no associated User!')
            else:
                self.character_class = character_class
                self.sprite = self.get_sprite_path_by_color(user.color)

        super().__init__(x=x, y=y, sprite=self.sprite, name=name, hp=hp, strength=strength, dexterity=dexterity,
                         intelligence=intelligence, charisma=charisma, perception=perception, initiative=initiative,
                         action_points=action_points, level=level, game_token=game_token, experience=experience)

        self.discord_identity = discord_identity
        self.alignment = alignment
        self.backstory = backstory
        self.character_race = character_race
        self.character_class = character_class
        self.active = False

    def get_sprite_path_by_color(self, color: str):
        import os

        path = f'dnd_bot/assets/gfx/entities/{self.character_class.lower()}_sprite_{color}.png'
        if os.path.isfile(path):
            return path
        else:
            return 'dnd_bot/assets/gfx/entities/player.png'
