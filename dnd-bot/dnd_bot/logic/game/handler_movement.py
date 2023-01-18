from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerMovement:
    @staticmethod
    async def handle_movement(direction, id_user, token) -> (bool, str):

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            return False, 'This user doesn\'t have a player!'

        if not player.active:
            return False, 'You can\'t perform a move right now!'

        if direction == 'right':
            player.x += 1
        elif direction == 'left':
            player.x -= 1
        elif direction == 'up':
            player.y += 1
        elif direction == 'down':
            player.y -= 1
        else:
            raise SyntaxError('This direction doesn\'t exist!')

        return True, ''

