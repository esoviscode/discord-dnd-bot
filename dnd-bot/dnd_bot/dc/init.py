from nextcord.ext import commands
from nextcord import Intents
import os

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.send_message import Messager

bot = commands.Bot(command_prefix='$', intents=Intents().all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print('\nBot started successfully')


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'dnd_bot.dc.cogs.{extension}')
    await ctx.send(f'`dnd_bot.dc.cogs.{extension}` was loaded.')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'dnd_bot.dc.cogs.{extension}')
    await ctx.send(f'`dnd_bot.dc.cogs.{extension}` was unloaded. You can no longer use it until it is reloaded.')


def bot_run():
    env_token = "BOT_TOKEN"
    token = os.getenv(env_token)

    if token is None:
        raise KeyError(f'Failed to get configuration key. Env name: {env_token}')

    print('Loading extensions:')
    for filename in os.listdir('./dnd_bot/dc/cogs')[1:]:
        if filename.endswith('.py'):
            bot.load_extension(f'dnd_bot.dc.cogs.{filename[:-3]}')
            print(f'    {filename[:-3]}')

    Messager.bot = bot
    DatabaseConnection.connection_establish()

    bot.run(token)
