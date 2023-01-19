from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.logic.prototype.multiverse import Multiverse


class ShutdownCommand(Cog):
    """Handles shutting down the bot with all its threads"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="shutdown", description="Shutdowns bot")
    async def shutdown(self, interaction):
        caller_id = interaction.user.id
        # only these users can shut down the bot
        if caller_id == 349553403229110274 \
                or caller_id == 211188033968406530 \
                or caller_id == 444538116569825290 \
                or caller_id == 602785249025589259 \
                or caller_id == 544262699907809309:
            await interaction.response.send_message("Shutting down... :coffin:")

            # stop all running game threads
            for game in Multiverse.games.values():
                game.game_state = "INACTIVE"
                game.get_active_player().active = False
                game.game_loop_thread.join()

            await self.bot.close()
        else:
            await interaction.response.send_message("You have no permission to shutdown me :man_gesturing_no:!")


def setup(bot):
    bot.add_cog(ShutdownCommand(bot))