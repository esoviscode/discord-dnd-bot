import nextcord
from nextcord.ext import commands
from nextcord import Intents
import os

from dnd_bot.database.database_connection import DatabaseConnection
from dnd_bot.dc.ui.messager import Messager

activity = nextcord.Activity(name='/help', type=nextcord.ActivityType.listening)
bot = commands.Bot(command_prefix='$', intents=Intents().all(), activity=activity)


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


# Error handling
@bot.event
async def on_command_error(interaction, error):
    """handles errors"""
    error_embed = nextcord.Embed(title="❌ The client has encountered an error while running this command!",
                                 description="😞 We are sorry for any inconveniences",
                                 color=0xFF5733)

    error_embed.set_author(name=interaction.bot.user.display_name, icon_url=interaction.bot.user.display_avatar)

    if isinstance(error, commands.errors.MissingRequiredArgument):
        error_embed.add_field(name="Error is described below.",
                              value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```")
    else:
        error_embed.add_field(name="Error is described below.", value=f"**Type:** {type(error)}\n\n```py\n{error}\n```")

    error_embed.add_field(name="__**What To do?**__",
                          value="Don't worry we will forward this message to the devs.",
                          inline=False)
    error_embed.set_footer(
        text=f"Command requested by {interaction.user.name}", icon_url=interaction.user.display_avatar)

    await interaction.response.send_message(embed=error_embed)
