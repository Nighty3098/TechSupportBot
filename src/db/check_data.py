from aiogram import types
from aiogram.types import Message

from config import bot, logger

async def get_data_url(message: types.Message) -> str:
    """
    Checks the message for attachments (documents, photos, videos) and returns file URLs.

    Args:
        message (types.Message): A message from the user.

    Returns:
        str: A string with file URLs separated by a newline. If there are no attachments, returns an empty string.    """
    files = []

    try:
        if message.document:
            file_url = await _get_file_url(message.document.file_id, "Document")
            files.append(file_url)

        if message.photo:
            file_url = await _get_file_url(message.photo[-1].file_id, "Photo")
            files.append(file_url)

        if message.video:
            file_url = await _get_file_url(message.video.file_id, "Video")
            files.append(file_url)

        if not files:
            logger.info("No attachments found in the message.")
            return ""

        result = "\n".join(files)
        logger.info(f"Attachments:\n{result}")
        return result

    except Exception as err:
        logger.error(f"Error processing attachments: {err}", exc_info=True)
        return ""

async def _get_file_url(file_id: str, file_type: str) -> str:
    """
    Gets the URL of the file by its ID.

    Args:
        file_id (str): The file ID.
        file_type (str): File type (for logging).

    Returns:
        str: The URL of the file.
    """
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
    logger.info(f"{file_type}: {file_url}")
    return file_url
