from .output import save_to_json
from .logger import get_logger
from .settings import settings
from .imbox import Imbox

logger = get_logger(__name__)


def messages_run(filters: dict) -> None:
    """Fetch messages from IMAP server with optional filters.

    Args:
        filters: Dictionary of message filters
    """
    with Imbox(config=settings.config, policy=None) as imbox:
        messages = imbox.messages(**filters)

        if settings.output:
            save_to_json(messsages=messages)
        else:
            for _, message in messages:
                logger.info(
                    f"UID: {message.uid} | " f"Date: {message.parsed.date} | " f"Subject: {message.parsed.subject}\n"
                )


def folders_run() -> None:
    """List all folders on the IMAP server."""
    with Imbox(config=settings.config, policy=None) as imbox:
        _, folders_list = imbox.folders()
        for folder in folders_list:
            logger.info(folder)
