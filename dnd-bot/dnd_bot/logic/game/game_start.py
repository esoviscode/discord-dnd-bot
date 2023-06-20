import time

from dnd_bot.database.database_game import DatabaseGame
from dnd_bot.logic.game.initialize_world import InitializeWorld
from dnd_bot.logic.prototype.multiverse import Multiverse


class GameStart:

    @staticmethod
    async def start(token):
        game = Multiverse.get_game(token)
        game_id = DatabaseGame.get_id_game_from_game_token(token)

        game.game_state = 'ACTIVE'
        DatabaseGame.update_game_state(game_id, 'ACTIVE')

        InitializeWorld.load_entities(game, 'dnd_bot/assets/maps/map.json',
                                            'dnd_bot/assets/campaigns/campaign.json')

        time_snapshot = time.time()
        await InitializeWorld.add_entities_to_database(game)
        print(f'   - adding entities to database - {round((time.time() - time_snapshot) * 1000, 2)} ms')





