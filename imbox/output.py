import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .logger import get_logger
from .settings import settings
from .messages import Messages

logger = get_logger()


def save_to_json(
    messsages: Messages,
) -> None:
    """Save results to a JSON file.

    Args:
        messages: Dictionary of messages to save

    Returns:
        Path to the saved JSON file

    Raises:
        OSError: If file cannot be written
        ValueError: If output_dir is None
    """
    filename = settings.output_filename

    if not filename.endswith(".json"):
        filename += ".json"

    output_path = Path(settings.output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename

    logger.info(f"Saving results to {filepath}")

    logger.info(messsages.to_dict())

    # try:
    #     filepath.write_text(
    #         json.dumps(messsages.to_dict(), indent=2, ensure_ascii=False),
    #         encoding="utf-8",
    #     )

    #     logger.info("Results saved to: %s", filepath)
    #     return str(filepath)

    # except OSError:
    #     logger.exception("Failed to save results to %s", filepath)
    #     raise
