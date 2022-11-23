import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands.");
    print('Bot has successfully started.')

@bot.tree.command(name="hello", description="Responds with greeting")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}")

def main():
    devpass_file = open("../devpass.cfg")
    devpass = devpass_file.read()
    devpass_file.close()

    bot.run(devpass)

main()