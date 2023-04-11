from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import SkillException


class HandlerSkills:
    @staticmethod
    async def handle_use_skill(skill, id_user, token) -> str:
        """handler for using skill
           return: message describing skill using process"""

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            raise SkillException("This user doesn't have a player!")

        if not player.active:
            raise SkillException("You can't perform a move right now!")

        if player.action_points == 0:
            raise "You're out of action points!"

        # TODO implement using skill

        return "Skill used!"
