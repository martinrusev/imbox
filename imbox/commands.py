from .logger import get_logger
from .settings import settings
from .imbox import Imbox

logger = get_logger(__name__)


def messages_run(filters: dict) -> None:
    """Fetch messages from IMAP server with optional filters.

    Args:
        config: Configuration object with IMAP connection details
        filters: Dictionary of message filters
    """
    with Imbox(config=settings.config, policy=None) as imbox:
        messages = imbox.messages(**filters)

        for uid, message in messages:
            logger.info(
                f"Message UID={uid}, "
                f"From={message.sent_from}, "
                f"Subject={message.subject}"
            )