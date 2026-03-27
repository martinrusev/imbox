import datetime
from typing import Any

import click

from .logger import get_logger
from .commands import messages_run, folders_run

logger = get_logger(__name__)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cli() -> None:
    """Imbox - Python IMAP Library for Agentic Workflow."""
    pass


@cli.command(name="messages")
@click.option(
    "--folder",
    default=None,
    help="Folder to fetch messages from (default: inbox).",
)
@click.option(
    "--unread/--no-unread",
    default=False,
    help="Fetch only unread messages.",
)
@click.option(
    "--flagged/--no-flagged",
    default=False,
    help="Fetch only flagged messages.",
)
@click.option(
    "--unflagged/--no-unflagged",
    default=False,
    help="Fetch only unflagged messages.",
)
@click.option(
    "--sent-from",
    default=None,
    help="Filter messages sent from this email address.",
)
@click.option(
    "--sent-to",
    default=None,
    help="Filter messages sent to this email address.",
)
@click.option(
    "--subject",
    default=None,
    help="Filter messages with subject containing this string.",
)
@click.option(
    "--date-lt",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Fetch messages received before this date (YYYY-MM-DD).",
)
@click.option(
    "--date-gt",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Fetch messages received after this date (YYYY-MM-DD).",
)
@click.option(
    "--date-on",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Fetch messages received on this date (YYYY-MM-DD).",
)
@click.option(
    "--uid-range",
    default=None,
    help="Filter messages by UID range (e.g., '1050:*').",
)
@click.option(
    "--raw",
    default=None,
    help="Gmail raw search query (e.g., 'from:user has:attachment').",
)
@click.option(
    "--label",
    default=None,
    help="Gmail label to filter by (Gmail only).",
)
def messages(
    folder: str | None,
    unread: bool,
    flagged: bool,
    unflagged: bool,
    sent_from: str | None,
    sent_to: str | None,
    subject: str | None,
    date_lt: datetime.datetime | None,
    date_gt: datetime.datetime | None,
    date_on: datetime.datetime | None,
    uid_range: str | None,
    raw: str | None,
    label: str | None,
) -> None:
    """Fetch messages from IMAP server with filtering options."""

    # Build filter kwargs
    filters: dict[str, Any] = {}
    if unread:
        filters["unread"] = True
    if flagged:
        filters["flagged"] = True
    if unflagged:
        filters["unflagged"] = True
    if sent_from:
        filters["sent_from"] = sent_from
    if sent_to:
        filters["sent_to"] = sent_to
    if subject:
        filters["subject"] = subject
    if date_lt:
        filters["date__lt"] = date_lt.date()
    if date_gt:
        filters["date__gt"] = date_gt.date()
    if date_on:
        filters["date__on"] = date_on.date()
    if uid_range:
        filters["uid__range"] = uid_range
    if raw:
        filters["raw"] = raw
    if label:
        filters["label"] = label
    if folder:
        filters["folder"] = folder

    messages_run(filters)


@cli.command(name="folders")
def folders() -> None:
    """List all folders on the IMAP server."""
    folders_run()
