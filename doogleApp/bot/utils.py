from googlesearch import search

from storage import models as storage_models


def validate_command(message, supported_flags):
    """
    Validate command
    :param message: (Message) message object
    :param supported_flags: (List) List of flags supported by command
    :return: (String) error
    """
    # Validate content length
    content_length = len(message.content)
    if content_length < 4:
        return "Content length should be more than 3."
    elif content_length > 20:
        return "Please enter content length less or equal to than 20."

    # Validate flags
    unknown_flags = set(message.flags.keys()) - set(supported_flags)
    if unknown_flags:
        return f"Unknown flags: {unknown_flags}."

    # Validate limit of results
    limit = message.flags.get("limit")
    if limit is not None:
        if limit < 1:
            return "Limit cannot be less than 1."
        if limit > 10:
            return "Limit cannot be more than 10."


def get_google_search_links(message):
    """
    Returns google search based links
    :param message: (Message) message object
    :return: links
    """
    error = validate_command(message, ["limit"])
    if error:
        return error

    # First store the searched item in DB
    chat = storage_models.ChatHistory(discord_member_id=message.author_id, search_data=message.content)
    chat.insert()
    # google search
    limit = message.flags.get("limit", 5)
    search_results = [url for url in search(message.content, stop=limit)]
    print(f"Fetched {len(search_results)} results.")
    return "\n".join(search_results) if search_results else "No data fetched."


def get_recent_search_history(message):
    """
    Returns list of recent searches made
    :param message: (Message) message object
    :return: List of recent searched
    """
    error = validate_command(message, ["limit", "quick_search"])
    if error:
        return error

    limit = message.flags.get("limit", 10)
    chat, params = storage_models.ChatHistory(discord_member_id=message.author_id), {
        "text": message.content, "limit": limit
    }
    # If flag is 'quick_search', execute vector search, else normal search
    search_list = chat.quick_filter(**params) if message.flags.get("quick_search") else chat.filter(**params)
    print(f"{len(search_list)} results found.")
    return ", ".join(result[0].strip() for result in search_list) if search_list else "No data found."
