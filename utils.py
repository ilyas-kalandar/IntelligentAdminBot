def mention_user(full_name: str, user_id: int) -> str:
    """
    Returns a mention-link to user
    :param full_name: A fullname of user
    :param user_id: An ID of user in telegram
    :return: Link
    :rtype: str
    """
    return f"<a href='tg://user?id={user_id}'>{full_name}</a>"
