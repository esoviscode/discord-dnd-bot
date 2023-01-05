from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command

from dnd_bot.logic.lobby.handler_join import HandlerJoin


class CommandJoin(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="join", description="Joins to the lobby by its id")
    async def join(self, interaction, token: str):
        if interaction.user.dm_channel is None:
            await interaction.user.create_dm()
        await interaction.response.send_message("Check direct message!", ephemeral=True)
        await HandlerJoin.join_lobby(token, interaction.user.id, interaction.user.name)


def setup(bot):
    bot.add_cog(CommandJoin(bot))
