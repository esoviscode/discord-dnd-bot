from dnd_bot.logic.prototype.multiverse import Multiverse


class HandlerStart:

    def __init__(self):
        pass

    @staticmethod
    async def start_game(token, user_id) -> (bool, list, str):

        game = Multiverse.get_game(token)
        if game is None:
            return False, [], f':no_entry: Game of provided token doesn\'t exist!'

        if user_id != game.id_host:
            return False, [], f':warning: Only the host can start the game!'

        if game.game_state == 'LOBBY' or game.game_state == 'STARTING':
            users = [user.discord_id for user in game.user_list]
            return True, users, ''
        else:
            return False, [], f':no_entry: The game has already started!'
