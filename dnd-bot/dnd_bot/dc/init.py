from nextcord.ext import commands
from nextcord import Intents
import os

bot = commands.Bot(command_prefix='$', intents=Intents().all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Bot started successfully')


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'dc.commands.{extension}')
    await ctx.send(f'`dc.commands.{extension}` was loaded.')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'dc.commands.{extension}')
    await ctx.send(f'`dc.commands.{extension}` was unloaded. You can no longer use it until it is reloaded.')


def bot_run():
    env_token = "BOT_TOKEN"
    token = os.getenv(env_token)

    if token is None:
        raise KeyError(f'Failed to get configuration key. Env name: {env_token}')

    for filename in os.listdir('./dc/cogs')[1:]:
        if filename.endswith('.py'):
            bot.load_extension(f'dc.cogs.{filename[:-3]}')

    bot.run(token)
