from dnd_bot.dc.utils.message_holder import MessageHolder
import nextcord


class Messager:
    """contains static methods to manage sending, editing and deleting messages on discord"""
    bot = None

    @staticmethod
    async def send_message(channel_id: id, content: str):
        channel = Messager.bot.get_channel(channel_id)
        await channel.send(content=content)

    @staticmethod
    async def send_dm_message(user_id: int, content: str | None, embed=None, view=None, files=None):
        user = Messager.bot.get_user(user_id)

        # includes files; parameter files is a list of string file paths
        if files:
            sent_message = await user.send(content=content, embed=embed, view=view,
                                           files=[nextcord.File(f) for f in files])
        else:
            sent_message = await user.send(content=content, embed=embed, view=view)
        MessageHolder.register_last_message_data(user_id, user.dm_channel.id, sent_message.id)

    @staticmethod
    async def edit_message(channel_id: int, message_id: int, new_content: str):
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.edit(content=new_content, embeds=message.embeds)

    @staticmethod
    async def edit_last_user_message(user_id: int, content="", embed=None, view=None, files=None):
        channel_id, message_id = MessageHolder.read_last_message_data(user_id)

        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        # includes files
        if files:
            await message.edit(content=content, embed=embed, view=view, files=[nextcord.File(f) for f in files])
        else:
            await message.edit(content=content, embed=embed, view=view)

    @staticmethod
    async def delete_last_user_message(user_id: int):
        channel_id, message_id = MessageHolder.read_last_message_data(user_id)
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()

    @staticmethod
    async def delete_message(channel_id, message_id):
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()
