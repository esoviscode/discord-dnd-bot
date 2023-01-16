from dnd_bot.logic.prototype.game import Game


class GameLoop:
    """This class manages all logic behind turns. The idea of usage is that when player invokes a command/action then
    the static method of this class is called.
    """
    @staticmethod
    def begin_turn(game_id):
        """does all the necessities to begin the turn"""
        pass

    @staticmethod
    def prepare_queue(game: Game):
        """puts all the creatures to the queue with order by initiative"""
        pass

    @staticmethod
    def get_game_object(game_id):
        """returns game object from given id"""
        return None

