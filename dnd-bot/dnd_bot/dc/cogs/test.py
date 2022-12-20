from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command
import nextcord


class HelloButton(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Hello", style=nextcord.ButtonStyle.green)
    async def hello(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Clicked me!", ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Nara", style=nextcord.ButtonStyle.red)
    async def nara(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Nara", ephemeral=False)
        self.value = False
        self.stop()


class Test(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="gowno", description="Tests")
    async def gowno(self, interaction):
        view = HelloButton()
        await interaction.response.send_message(f"kurwo {interaction.user.mention}", view=view)
        await view.wait()

        if view.value is None:
            return
        elif view.value:
            print("Gratuluje")
        else:
            print("Żegnam")


def setup(bot):
    bot.add_cog(Test(bot))
    print("Setuped")
