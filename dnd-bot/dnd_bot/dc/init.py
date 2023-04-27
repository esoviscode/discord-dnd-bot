import logging
import os
import sys
import traceback

import nextcord
from nextcord import Intents
from nextcord.ext import commands

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.messager import Messager

activity = nextcord.Activity(name='/help', type=nextcord.ActivityType.listening)
bot = commands.Bot(command_prefix='/', intents=Intents().all(), activity=activity)


@bot.event
async def on_ready():
    print('\nBot started successfully')


@bot.command()
async def load(ctx, extension):
    """loads nextcord cogs"""
    bot.load_extension(f'dnd_bot.dc.cogs.{extension}')
    await ctx.send(f'`dnd_bot.dc.cogs.{extension}` was loaded.')


@bot.command()
async def unload(ctx, extension):
    """unloads nextcord cogs"""
    bot.unload_extension(f'dnd_bot.dc.cogs.{extension}')
    await ctx.send(f'`dnd_bot.dc.cogs.{extension}` was unloaded. You can no longer use it until it is reloaded.')


def bot_run():
    """starts basic bot configuration like setting commands, establishing connection to the database and setting
    crucial variables """
    env_token = "BOT_TOKEN"
    token = os.getenv(env_token)

    # set up logging
    logger = logging.getLogger('nextcord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord-dnd-bot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    if token is None:
        raise KeyError(f'Failed to get configuration key. Env name: {env_token}')

    print('Loading extensions:')
    for filename in os.listdir('./dnd_bot/dc/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'dnd_bot.dc.cogs.{filename[:-3]}')
            print(f'    {filename[:-3]}')

    Messager.bot = bot
    DatabaseConnection.connection_establish()

    bot.run(token)


# Error handling
@bot.event
async def on_command_error(interaction, error):
    """handles errors"""
    await on_application_command_error(interaction, error)


@bot.event
async def on_application_command_error(interaction, error):
    """handles errors"""

    print(f'ERROR: {error}', file=sys.stderr)

    error_embed = nextcord.Embed(title="❌ The client has encountered an error while running this command!",
                                 color=0xFF5733)

    error_embed.set_author(name=bot.user.display_name, icon_url=bot.user.display_avatar)
    error_embed.add_field(name="__What To do?__",
                          value="Check if you use the correct command arguments",
                          inline=False)
    error_embed.set_footer(
        text=f"Command requested by {interaction.user.name}", icon_url=interaction.user.display_avatar)

    await interaction.response.send_message(embed=error_embed)


@bot.event
async def on_error(event_name, *args, **kwargs):
    print(f"Exception in {event_name}", file=sys.stderr)
    traceback.print_exc()

    interaction = args[1]

    error_embed = nextcord.Embed(title="❌ The client has encountered an unexpected error!",
                                 color=0xFF5733)

    error_embed.set_author(name=bot.user.display_name, icon_url=bot.user.display_avatar)
    error_embed.add_field(name="__What To do?__",
                          value="Try repeating the interaction in case error was caused by Discord\n\n"
                                "Otherwise, wait for a patch that fixes this bug.\n"
                                "We are sorry for any inconveniences 😓\n\n"
                                "You can report the issue here:\n https://github.com/esoviscode/discord-dnd-bot/issues",
                          inline=False)
    error_embed.set_footer(
        text=f"Command requested by {interaction.user.name}", icon_url=interaction.user.display_avatar)

    await interaction.response.defer()

    await Messager.send_dm_error_message(user_id=interaction.user.id, content='', embeds=[error_embed])
