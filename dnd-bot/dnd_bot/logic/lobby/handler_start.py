from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.logic.prototype.player import Player


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
        game_id = DatabaseConnection.get_id_game_from_game_token(token)

        if game_id is None:
            return False, [], ":no_entry: Error creating game!"
        for user in game.user_list:
            DatabaseConnection.add_user(game_id, user.discord_id)

        if game is None:
            return False, [], f':warning: Game of provided token doesn\'t exist!'

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if not game.all_users_ready():
            return False, [], f':warning: Not all the players are ready!'

        if game.game_state == 'LOBBY':
            game.game_state = "STARTING"
            DatabaseConnection.update_game_state(game_id, 'STARTING')

            if game_id is None:
                game.game_state = 'LOBBY'
                return False, [], ":warning: Error creating game!"
            for user in game.user_list:
                DatabaseConnection.add_user(game_id, user.discord_id)

            GameStart.start(token)
            GameLoop.prepare_queue(game)

            for creature in game.creatures_queue:
                if isinstance(creature, Player):
                    creature.active = True
                    break

            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: This game has already started!'
