from nextcord import Guild


async def send_message(server: Guild, channel_id: id, content: str):
    channel = await server.fetch_channel(channel_id)
    await channel.send(content=content)


async def send_dm_message(server, user_id, content):
    await server.get_member(user_id).dm_channel.send(content=content)
