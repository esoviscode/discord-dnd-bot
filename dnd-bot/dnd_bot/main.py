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
    client.run('MTA0NDMwNzg2NzI2OTg2MTQwOA.G-6xOG.6OOnxia9luYir_dugHSITRxeZcRbBcbPuFXQ1E')

main()