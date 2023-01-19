class Messager:
    """contains static methods to manage sending, editing and deleting messages on discord"""
    bot = None

    @staticmethod
    async def send_message(channel_id: id, content: str):
        channel = Messager.bot.get_channel(channel_id)
        await channel.send(content=content)

    @staticmethod
    async def send_dm_message(user_id: int, content: str | None, embed=None, view=None):
        await Messager.bot.get_user(user_id).send(content=content, embed=embed, view=view)

    @staticmethod
    async def edit_message(channel_id: int, message_id: int, new_content: str):
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.edit(content=new_content, embeds=message.embeds)
