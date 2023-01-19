import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext.commands import Bot, Cog

from dnd_bot.dc.ui.message_templates import MessageTemplates


class CommandTmpGameView(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="tmpview", description="Temporary map view for testing")
    async def tmpview(self, interaction: Interaction):

        tmp_view_embed = MessageTemplates.tmp_view_template()

        await interaction.response.send_message(embed=tmp_view_embed, files=[nextcord.File('dnd_bot/assets/gfx/map_view.png')])

        return


def setup(bot):
    bot.add_cog(CommandTmpGameView(bot))
