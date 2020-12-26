from bot import utils as bot_utils


def preprocess_message(message):
    """
    Pre-processing message before processing data
    :param message: Discord message
    :return: Preprocessed Discord message
    """
    # Trim whitespaces
    message.content = message.content.strip()

    return message


def process_chat(message):
    """
    Process input message arrived and reply accordingly
    :param message: Discord message type
    :return: (message): Reply after processing
    """
    message = preprocess_message(message)
    if message.content == "hi":
        return "hey"

    elif message.content.startswith("!google"):
        return bot_utils.get_google_search_links(message)

    elif message.content.startswith("!recent"):
        return bot_utils.get_recent_search_history(message)
