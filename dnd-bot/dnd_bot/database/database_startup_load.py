from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.logic.prototype.game import Game
from dnd_bot.logic.prototype.multiverse import Multiverse
from dnd_bot.dc.utils.utils import get_user_name_by_id
from dnd_bot.dc.utils.utils import get_user_dm_channel_by_id


class MultiverseStartupLoad:

    @staticmethod
    def load_data():
        game_tokens = DatabaseConnection.get_all_game_tokens()
        for token in game_tokens:
            game_tuple = DatabaseConnection.find_game_by_token(token)
            game = Game(token=game_tuple['token'], id_host=game_tuple['id_host'], id_campaign=game_tuple['id_campaign'],
                        game_state=game_tuple['game_state'])
            for player_tuple in game_tuple['players']:
                username = get_user_name_by_id(player_tuple['discord_id'])
                dm_channel_id = get_user_dm_channel_by_id(player_tuple['discord_id'])
                if player_tuple['user_id'] == game_tuple['host_id']:
                    game.add_host(user_id=player_tuple['user_id'], username=username,user_channel_id=dm_channel_id)
                else:
                    game.add_player(user_id=player_tuple['user_id'], username=username,user_channel_id=dm_channel_id)

            Multiverse.add_game(game)
