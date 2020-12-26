from googlesearch import search

from storage import models as storage_models


def get_google_search_links(message):
    """
    Returns google search based links
    :param message: (Discord Message) message object
    :return: links
    """
    _, content = message.content.split(" ", 1)
    # First store the searched item in DB
    chat = storage_models.ChatHistory(discord_member_id=message.author.id, search_data=content)
    chat.insert()
    # google search
    search_results, output = search(content, stop=5), ""
    return "\n".join([url for url in search_results])


def get_recent_search_history(message):
    """
    Returns list of recent searches made
    :param message: (Discord message) message object
    :return: List of recent searched
    """
    _, content = message.content.split(" ", 1)
    chat = storage_models.ChatHistory(discord_member_id=message.author.id)
    return ", ".join(text[0].strip() for text in chat.filter(text=content))
