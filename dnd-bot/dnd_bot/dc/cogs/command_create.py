from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.logic.lobby.handler_create import HandlerCreate


class CommandCreate(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="create", description="Creates new lobby")
    async def create(self, interaction):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()
        await HandlerCreate.create_lobby(self.bot, interaction.channel_id, interaction.user.id)


def setup(bot):
    bot.add_cog(CommandCreate(bot))
