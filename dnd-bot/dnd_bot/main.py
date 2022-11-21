import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print('Bot has successfully started.')

@tree.command(name="hello", description="Responds with greeting")#, guild=discord.Object(id=913375693864308797))
async def hello(interaction):
    await interaction.response.send_message("Hello")

def main():
    devpass_file = open("../devpass.cfg")
    devpass = devpass_file.read()
    devpass_file.close()

    client.run(devpass)

main()