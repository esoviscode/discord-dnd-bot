from dnd_bot.database.database_entity import DatabaseEntity
from dnd_bot.database.database_player import DatabasePlayer
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.utils.exceptions import MovementException


class HandlerMovement:
    @staticmethod
    async def handle_movement(direction, num_tiles, id_user, token):
        """handler for moving x tiles in a direction"""

        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        if player is None:
            raise MovementException("This user doesn't have a player!")

        if game.active_creature != player:
            raise MovementException("You can't perform a move right now - another creature is active!")

        if player.action_points == 0:
            raise MovementException("You're out of action points!")

        if num_tiles == 1:
            if player.action_points is not None and player.action_points > 0:
                player.action_points -= 1
            try:
                player.move_one_tile(direction, game)
            except MovementException as e:
                raise e
        else:
            raise MovementException("Not implemented yet!")     # TODO implement moving >1 tiles

    @staticmethod
    async def handle_end_turn(id_user, token):
        """handles end of player's turn"""
        game = Multiverse.get_game(token)

        player = game.get_player_by_id_user(id_user)
        player.action_points = player.initial_action_points

        player.active = False
