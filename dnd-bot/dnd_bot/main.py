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
    devpass_file = open("../devpass.cfg")
    devpass = devpass_file.read()
    devpass_file.close()
    
    client.run(devpass)

main()