from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerMovement:
    @staticmethod
    async def handle_movement(direction, num_tiles, id_user, token) -> (bool, str):
        """handler for moving x tiles in a direction"""

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            return False, 'This user doesn\'t have a player!'

        player.active = True  # TODO remove, testing purposes
        if not player.active:
            return False, 'You can\'t perform a move right now!'
        player.active = False  # TODO remove, testing purposes

        if num_tiles == 1:
            status, error_message = player.move_one_tile(direction, num_tiles, game)
        else:
            return False, 'Not implemented yet!'  # TODO implement moving >1 tiles

        if not status:
            return False, error_message

        return True, ''
