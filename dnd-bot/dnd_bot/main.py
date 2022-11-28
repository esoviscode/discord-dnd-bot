import os
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
    env_token = "BOT_TOKEN"
    token = os.getenv(env_token)

    if token is None:
        raise KeyError(f'Failed to get configuration key. Env name: {env_token}')
    # devpass_file = open("../devpass.cfg")
    # devpass = devpass_file.read()
    # devpass_file.close()
    
    bot.run(token)

main()
