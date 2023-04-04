from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerMovement:
    @staticmethod
    async def handle_movement(direction, num_tiles, id_user, token):
        """handler for moving x tiles in a direction"""

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            raise Exception("This user doesn't have a player!")

        if game.active_creature != player:
            raise Exception("You can't perform a move right now - another creature is active!")

        if player.action_points == 0:
            raise Exception("You're out of action points!")

        if num_tiles == 1:
            if player.action_points is not None and player.action_points > 0:
                player.action_points -= 1
            try:
                player.move_one_tile(direction, game)
            except Exception as e:
                raise e
        else:
            raise Exception("Not implemented yet!")     # TODO implement moving >1 tiles

    @staticmethod
    async def handle_end_turn(id_user, token):
        """handles end of player's turn"""
        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        player.action_points = player.initial_action_points

        player.active = False

        return True, ''
