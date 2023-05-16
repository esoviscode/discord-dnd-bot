import asyncio

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

        await InitializeWorld.load_entities(game, 'dnd_bot/assets/maps/map.json', 'dnd_bot/assets/campaigns/campaign.json')





