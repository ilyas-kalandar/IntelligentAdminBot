from pyrogram import Client, errors


class UserBot:
    def __init__(self, api_hash, api_id):
        self.client = Client('session', api_id, api_hash)
        self.client.start()

    async def get_user(self, chat_id: int, username: str):
        """
        Converts username to user_id

        :param chat_id: An id of chat in telegram
        :param username: Username
        :return: An ID of user on telegram
        :rtype: int
        """
        try:
            _user = await self.client.get_chat_member(chat_id, username)
        except errors.UserNotParticipant:
            raise ValueError("User does not exist in this chat.")

        return _user.user

    async def get_message(self, chat_id: int, message_id: int):
        message = await self.client.get_messages(chat_id, message_id)
        return message
