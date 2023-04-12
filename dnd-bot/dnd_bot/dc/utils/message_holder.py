class MessageHolder:
    """This class holds data of the last message that was sent to each user"""

    # keys of this dict are tuples of user discord ids and game tokens; values are couples of channel id and message_id
    user_last_message_data: dict[(int, str), (int, int)] = {}
    user_last_error_message_data: dict[(int, str), (int, int)] = {}

    @staticmethod
    def register_last_message_data(user_id: int, token: str, channel_id: int, message_id: int):
        """save last message data for given discord user id and game token"""
        MessageHolder.user_last_message_data[(user_id, token)] = (channel_id, message_id)

    @staticmethod
    def read_last_message_data(user_id: int, token: str):
        """read last message data for given discord user id and game token"""
        if not (user_id, token) in MessageHolder.user_last_message_data:
            return None
        else:
            return MessageHolder.user_last_message_data[(user_id, token)]

    @staticmethod
    def register_last_error_data(user_id: int, token: str, channel_id: int, message_id: int):
        """save last error data for given discord user id and game token"""
        MessageHolder.user_last_error_message_data[(user_id, token)] = (channel_id, message_id)

    @staticmethod
    def read_last_error_data(user_id: int, token: str):
        """read last error data for given discord user id and game token"""
        if not (user_id, token) in MessageHolder.user_last_error_message_data:
            return None
        else:
            return MessageHolder.user_last_error_message_data[(user_id, token)]

    @staticmethod
    def delete_last_error_data(user_id: int, token: str):
        MessageHolder.user_last_error_message_data[(user_id, token)] = None

