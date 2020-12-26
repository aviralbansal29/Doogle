import re

from bot import utils as bot_utils
from storage import models as storage_models


def preprocess_message(message):
    """
    Pre-processing message before processing data
    :param message: Discord message
    :return: Preprocessed Message object
    """
    # Initialize variables
    local_message = storage_models.Message()
    local_message.author_id = message.author.id

    # Trim whitespaces
    local_message.content = message.content.strip()

    # Check for supported commands
    if local_message.content == "hi":
        local_message.command_type = storage_models.HI_COMMAND

    regex_data = re.findall("^((\w+=\d+ )*)!((google)|(recent)) (.*)", message.content)
    if regex_data:
        regex_data = regex_data[0]
        # regex_data will have format as:
        # regex_data[0] -> flags
        # regex_data[2] -> command type
        # regex_data[-1] -> content
        exec(f"local_message.flags = dict({regex_data[0].replace(' ', ',')[:-1].lower()})")
        local_message.command_type = {
            "google": storage_models.SEARCH_COMMAND, "recent": storage_models.HISTORY_COMMAND
        }.get(regex_data[2], storage_models.UNKNOWN_COMMAND)
        local_message.content = regex_data[-1]

    return local_message


def process_chat(message):
    """
    Process input message arrived and reply accordingly
    :param message: Discord message type
    :return: (message): Reply after processing
    """
    message = preprocess_message(message)
    # If content is not a valid command, maybe the command is not for user
    if message.command_type == storage_models.UNKNOWN_COMMAND:
        return

    if message.content == "hi":
        return "hey"

    elif message.command_type == storage_models.SEARCH_COMMAND:
        return bot_utils.get_google_search_links(message)

    elif message.command_type == storage_models.HISTORY_COMMAND:
        return bot_utils.get_recent_search_history(message)
