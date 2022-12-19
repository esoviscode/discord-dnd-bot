from nextcord import Guild


async def send_message(server: Guild, channel_id: id, content: str):
    channel = await server.fetch_channel(channel_id)
    await channel.send(content=content)
