from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerAttack:
    @staticmethod
    async def handle_attack(enemy, id_user, token) -> (bool, [], str):
        """handler for attacking enemy with main weapon"""

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            return False, [], 'This user doesn\'t have a player!'

        if not player.active:
            return False, [], 'You can\'t perform a move right now!'

        if player.action_points == 0:
            return False, [], 'You\'re out of action points!'

        enemies = []
        # TODO implement attacking and getting new list of enemies

        return True, enemies, ''
