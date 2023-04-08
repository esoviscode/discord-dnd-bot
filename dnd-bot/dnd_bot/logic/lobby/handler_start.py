from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.logic.prototype.player import Player
from dnd_bot.logic.utils.exceptions import StartGameException


class HandlerStart:
    """handles starting of the game when all players in lobby are ready"""
    def __init__(self):
        pass

    @staticmethod
    async def start_game(token, user_id) -> (bool, list, str):
        """in lobby, starts a game; has an effect when used by the host of the lobby
                :param token: game token
                :param user_id: id of the user who ran the command or the host that pressed the start button
                :return: status, (if start was successful, users list, optional error message)
                """
        game = Multiverse.get_game(token)
        game_id = DatabaseGame.get_id_game_from_game_token(token)

        if game_id is None:
            raise StartGameException(':no_entry: Error creating game!')

        if game is None:
            raise StartGameException(':warning: Game of provided token doesn\'t exist!')

        if user_id != game.id_host:
            raise StartGameException(':warning: Only the host can start the game!')

        if not game.all_users_ready():
            raise StartGameException(':warning: Not all the players are ready!')

        if game.game_state == 'LOBBY':
            game.game_state = "STARTING"
            DatabaseGame.update_game_state(game_id, 'STARTING')

            if game_id is None:
                game.game_state = 'LOBBY'
                raise StartGameException(':warning: Error creating game!')

            users = [user.discord_id for user in game.user_list]
            return users
        else:
            raise StartGameException(':no_entry: This game has already started!')
