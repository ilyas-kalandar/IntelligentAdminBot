from aiogram import Dispatcher
from .can_restrict_members import CanRestrictMembers
from .is_admin import IsAdmin
from .read_only import IsReadOnly


def setup_filters(dp: Dispatcher):
    """
    Setups the filters
    :param dp: An dispatcher instance
    :return:None
    """
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(CanRestrictMembers)
    dp.filters_factory.bind(IsReadOnly)
