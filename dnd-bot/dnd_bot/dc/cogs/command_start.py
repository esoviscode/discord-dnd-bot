import nextcord
from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command
from dnd_bot.dc.ui.messager import Messager
from dnd_bot.logic.game.game_loop import GameLoop
from dnd_bot.logic.game.game_start import GameStart
from dnd_bot.logic.lobby.handler_start import HandlerStart
from dnd_bot.logic.utils.exceptions import DiscordDndBotException


class CommandStart(Cog):
    """game start command"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="start", description="Exits from lobby and starts game")
    async def start(self, interaction: nextcord.Interaction, token: str):
        caller_id = interaction.user.id

        # only these users can shut down the bot
        if caller_id == 349553403229110274 \
                or caller_id == 211188033968406530 \
                or caller_id == 444538116569825290 \
                or caller_id == 602785249025589259 \
                or caller_id == 544262699907809309:
            try:
                lobby_players_identities = await HandlerStart.start_game(token, interaction.user.id)

                partial_msg = await interaction.response.send_message('Starting the game!', ephemeral=True)

                # send messages about successful start operation
                for user in lobby_players_identities:
                    await Messager.send_dm_message(user, token, "Game has started successfully!\n")

                await GameStart.start(token)
                await GameLoop.start_loop(token)

                msg = await partial_msg.fetch()
                await msg.delete()
            except DiscordDndBotException as e:
                await interaction.response.send_message(f'{e}', ephemeral=True)
        else:
            await interaction.response.send_message("You have no permission quick start the game :man_gesturing_no:!")

            
def setup(bot):
    bot.add_cog(CommandStart(bot))
