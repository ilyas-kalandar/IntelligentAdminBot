from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class AdministrativePermissionsFilter(BoundFilter):
    """
    Checks permissions of ChatMember
    """

    def __init__(self, **permissions):
        """
        Initializes self
        :param permissions: A permissions of ChatMember
        """
        self.required_permissions = permissions

    async def check(self, message: types.Message):
        """
        Checks permissions of admin
        :param message:
        :return:
        """

        # firstly, get chat member
        member = await message.chat.get_member(message.from_user.id)

        if not isinstance(member, types.ChatMemberAdministrator) and not isinstance(member, types.ChatMemberOwner):
            # if member is not admin or owner, skip checking and return False
            await message.reply("You must be administrator of chat!")
            return False

        for perm in self.required_permissions:
            # check even permission

            if getattr(member, perm) is not self.required_permissions[perm]:
                # if needed permission was not found, return False
                await message.reply("You haven't needed permission, sorry")
                return False

        # if all was good, return True

        return True
