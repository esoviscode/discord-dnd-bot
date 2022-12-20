class Messager:

    bot = None

    @staticmethod
    async def send_message(channel_id: id, content: str):
        channel = Messager.bot.get_channel(channel_id)
        await channel.send(content=content)

    @staticmethod
    async def send_dm_message(user_id, content):
        await Messager.bot.get_user(user_id).send(content=content)
