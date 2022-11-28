import os
import discord
from discord.ext import commands

intents = discord.Intents().all()
client = commands.Bot(command_prefix= '!', intents=intents)

@client.event
async def on_ready():
    print('Bot has successfully started.')

@client.command()
async def hello(ctx):
    await ctx.send("Hello world!")

def main():
    env_token = "BOT_TOKEN"
    token = os.getenv(env_token)

    if token is None:
        raise KeyError(f'Failed to get configuration key. Env name: {env_token}')
    # devpass_file = open("../devpass.cfg")
    # devpass = devpass_file.read()
    # devpass_file.close()
    
    client.run(token)

main()
