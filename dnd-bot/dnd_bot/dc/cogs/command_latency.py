from datetime import datetime, timezone

from nextcord import slash_command, InteractionMessage
from nextcord.ext.commands import Cog, Bot


class CommandLatency(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='latency', description='Shows you the current latency')
    async def latency(self, interaction):
        original_time = interaction.created_at
        await interaction.response.send_message(
            f'🏓 Latency is {round((datetime.now(timezone.utc) - original_time).total_seconds() * 1000, 2)} ms')


def setup(bot):
    bot.add_cog(CommandLatency(bot))
