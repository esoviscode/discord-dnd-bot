from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command


class Hello(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="hello", description="Greets")
    async def hello(self, interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}")


def setup(bot):
    bot.add_cog(Hello(bot))
