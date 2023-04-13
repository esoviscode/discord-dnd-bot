import nextcord
from nextcord import User, Forbidden, Embed

from dnd_bot.dc.utils.message_holder import MessageHolder
from dnd_bot.logic.utils.exceptions import DMCreationException, MessagerException


class Messager:
    """contains static methods to manage sending, editing and deleting messages on discord"""
    bot = None

    @staticmethod
    async def __send_message(channel_id: id, content: str):
        """
        internal function of messager to send a message to a channel
        :return: sent message object
        """
        channel = Messager.bot.get_channel(channel_id)
        try:
            sent_message = await channel.send(content=content)
        except Forbidden:
            raise MessagerException('No proper permissions!')
        except Exception:
            raise MessagerException('Something went wrong!')

        return sent_message

    @staticmethod
    async def send_message(channel_id: id, content: str):
        """send a normal message to a channel"""
        await Messager.__send_message(channel_id, content)

    @staticmethod
    async def send_error_message(channel_id: id, content: str):
        """send an error message to a channel
        note: message will be preceded by warning emoji"""
        await Messager.__send_message(channel_id, f'⚠️ {content}')

    @staticmethod
    async def send_information_message(channel_id: id, content: str):
        """send an information message to a channel
        note: message will be preceded by information emoji"""
        await Messager.__send_message(channel_id, f'ℹ️ {content}')

    @staticmethod
    async def __send_dm_message(user: User, content: str | None, embeds: list[Embed] = None, view=None, files=None):
        """
        internal function of Messager to send a dm message
        :param user: user object to which the message will be sent to
        :param embeds: list of zero or more embeds to attach to the message
        :param view: nextcord View will be attached to the message
        :param files: files to be attached
        :return: sent message object
        """

        if embeds is None:
            embeds = []
        await Messager.create_user_dm(user.id)

        # includes files; parameter files is a list of string file paths
        if files:
            sent_message = await user.send(content=content, embeds=embeds, view=view,
                                           files=[nextcord.File(f) for f in files])
        else:
            sent_message = await user.send(content=content, embeds=embeds, view=view)

        return sent_message

    @staticmethod
    async def send_dm_message(user_id: int, token: str, content: str | None, embeds=None, view=None, files=None):
        """
        method used to send a direct message to a user
        """
        if embeds is None:
            embeds = []
        user = Messager.bot.get_user(user_id)

        sent_message = await Messager.__send_dm_message(user, content, embeds, view, files)

        MessageHolder.register_last_message_data(user_id, token, user.dm_channel.id, sent_message.id)

    @staticmethod
    async def send_dm_error_message(user_id: int, token: str, content: str, embeds=None, view=None, files=None):
        """
        method used to send a direct error message to user
        note: content will be preceded by a warning emoji
        """
        if embeds is None:
            embeds = []
        await Messager.delete_last_user_error_message(user_id, token)

        user = Messager.bot.get_user(user_id)

        sent_message = await Messager.__send_dm_message(user, f'⚠️ {content}', embeds, view, files)

        MessageHolder.register_last_error_data(user_id, token, user.dm_channel.id, sent_message.id)

    @staticmethod
    async def send_dm_information_message(user_id: int, token: str, content: str, embeds=None, view=None, files=None):
        """
        method used to send a direct error message to user
        note: content will be preceded by an information emoji
        """
        if embeds is None:
            embeds = []
        await Messager.delete_last_user_error_message(user_id, token)

        user = Messager.bot.get_user(user_id)

        sent_message = await Messager.__send_dm_message(user, f'ℹ️ {content}', embeds, view, files)

        MessageHolder.register_last_error_data(user_id, token, user.dm_channel.id, sent_message.id)

    @staticmethod
    async def edit_message(channel_id: int, message_id: int, new_content: str):
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        await message.edit(content=new_content, embeds=message.embeds)

    @staticmethod
    async def edit_last_user_message(user_id: int, token: str, content: str = '', embeds: list[Embed] | None = None, view=None,
                                     files=None, retain_view=False):
        """
        edit message
        :param user_id: id of user to which the message will be sent to
        :param token: game token
        :param content: message as a string
        :param embeds: list of zero or more embeds to attach to the message
        :param view: nextcord View will be attached to the message
        :param files: files to be attached, do not pass them as an argument to leave the original files attached to the message
        :param retain_view: whether to retain the original view or not
        """
        if embeds is None:
            embeds = []

        channel_id, message_id = MessageHolder.read_last_message_data(user_id, token)

        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        if retain_view:
            view = nextcord.ui.View.from_message(message)

        if files:
            await message.edit(content=str(content), embeds=embeds, view=view, files=[nextcord.File(f) for f in files])
        else:
            await message.edit(content=str(content), embeds=embeds, view=view)

    @staticmethod
    async def edit_last_user_error_message(user_id: int, token: str, content: str):
        """
        edits last user error or information message
        """
        error_data = MessageHolder.read_last_error_data(user_id, token)
        if error_data is not None:
            MessageHolder.delete_last_error_data(user_id, token)
            await Messager.edit_message(error_data[0], error_data[1], f'⚠️ {content}')

    @staticmethod
    async def __delete_message(channel_id, message_id):
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()

    @staticmethod
    async def delete_last_user_message(user_id: int, token: str):
        channel_id, message_id = MessageHolder.read_last_message_data(user_id, token)
        channel = Messager.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.delete()

    @staticmethod
    async def delete_last_user_error_message(user_id: int, token: str):
        """deletes last user error message and data about it in MessageHolder.
        If there were no error messages the function does nothing"""
        # check for previous error messages
        error_data = MessageHolder.read_last_error_data(user_id, token)

        # delete error messages
        if error_data is not None:
            MessageHolder.delete_last_error_data(user_id, token)
            await Messager.__delete_message(error_data[0], error_data[1])

    @staticmethod
    async def create_user_dm(user_id: int):
        """creates a direct message channel with the user if it doesn't exist
        when dm creation is unsuccessful (e.g. user has dms disabled in privacy settings) throws DMCreationException"""

        user = Messager.bot.get_user(user_id)

        if user.dm_channel is None:
            channel = await user.create_dm()

            if channel is None:
                raise DMCreationException('Can\'t create a direct message channel with this user!')
