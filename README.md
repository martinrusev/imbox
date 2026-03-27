# Imbox - Python IMAP Library for Agentic Workflows

![workflow](https://github.com/martinrusev/imbox/actions/workflows/python-app.yml/badge.svg)

Python library for reading IMAP mailboxes and converting email content to machine readable data

## Requirements

Python (3.11, 3.12, 3.13)


## Installation

`pip install imbox`

## CLI Usage

Imbox includes a command-line interface that can be used to fetch emails directly from the terminal and saving the results to a JSON file. This is particularly useful for agentic workflows.


### Running with uv

The recommended way to run the CLI is with [uv](https://github.com/astral-sh/uv):

```bash
uv run imbox messages
```

### Configuration

The CLI reads configuration from environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `IMBOX_IMAP_URL` | IMAP server URL | `imap.gmail.com` |
| `IMBOX_USERNAME` | IMAP username | - |
| `IMBOX_PASSWORD` | IMAP password or app password | - |
| `IMBOX_SSL` | Enable SSL | `true` |
| `IMBOX_PORT` | IMAP port | `993` |
| `IMBOX_STARTTLS` | Enable STARTTLS | `false` |
| `DEBUG` | Enable debug logging | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_OUTPUT_TYPE` | Output format. Clean displays only email fields. Default includes imbox metadata (`default` or `clean`) | `default` |
| `OUTPUT` | Enable file output | `false` |
| `OUTPUT_FOLDER` | Output folder for downloaded messages | `output` |
| `OUTPUT_FILENAME` | Output filename for results | `imbox_results.json` |

### Messages Command

Fetch messages with optional filters:

```bash
# Basic usage (requires IMBOX_USERNAME and IMBOX_PASSWORD env vars)
uv run imbox messages

# Fetch from specific folder
uv run imbox messages --folder "Social"

# Fetch unread messages only
uv run imbox messages --unread

# Fetch flagged messages
uv run imbox messages --flagged

# Filter by sender
uv run imbox messages --sent-from "sender@example.com"

# Filter by recipient
uv run imbox messages --sent-to "recipient@example.com"

# Filter by subject
uv run imbox messages --subject "Newsletter"

# Filter by date range
uv run imbox messages --date-gt 2026-01-01 --date-lt 2026-12-31

# Filter by specific date
uv run imbox messages --date-on 2026-03-15

# Filter by UID range (e.g., messages with UID 1050 and above)
uv run imbox messages --uid-range "1050:*"

# Gmail-specific raw search (requires Gmail)
uv run imbox messages --raw "from:user has:attachment"

# Gmail-specific label filter (Gmail only)
uv run imbox messages --folder all --label "finance"

# Combine multiple filters
uv run imbox messages --folder "INBOX" --unread --sent-from "newsletter@example.com"
```

### Folders Command

List all folders on the IMAP server:

```bash
uv run imbox folders
```

### Debugging

Enable debug output for troubleshooting:

```bash
DEBUG=true LOG_LEVEL=DEBUG uv run imbox messages --unread
```

## Usage (Python Library)

``` python
from imbox import Imbox

# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context

with Imbox('imap.gmail.com',
        username='username',
        password='password',
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

    # Get all folders
    status, folders_with_additional_info = imbox.folders()

    # Gets all messages from the inbox
    all_inbox_messages = imbox.messages()

    # Unread messages
    unread_messages = imbox.messages(unread=True)

    # Flagged messages
    flagged_messages = imbox.messages(flagged=True)

    # Un-flagged messages
    unflagged_messages = imbox.messages(unflagged=True)

    # Messages sent FROM
    inbox_messages_from = imbox.messages(sent_from='sender@example.org')

    # Messages sent TO
    inbox_messages_to = imbox.messages(sent_to='receiver@example.org')

    # Messages received before specific date
    inbox_messages_received_before = imbox.messages(date__lt=datetime.date(2026, 7, 31))

    # Messages received after specific date
    inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2026, 7, 30))

    # Messages received on a specific date
    inbox_messages_received_on_date = imbox.messages(date__on=datetime.date(2026, 7, 30))

    # Messages whose subjects contain a string
    inbox_messages_subject_christmas = imbox.messages(subject='Christmas')

    # Messages whose UID is greater than 1050
    inbox_messages_uids_greater_than_1050 = imbox.messages(uid__range='1050:*')

    # Messages from a specific folder
    messages_in_folder_social = imbox.messages(folder='Social')

    # Some of Gmail's IMAP Extensions are supported (label and raw):
    all_messages_with_an_attachment_from_martin = imbox.messages(folder='all', raw='from:martin@amon.cx has:attachment')
    all_messages_labeled_finance = imbox.messages(folder='all', label='finance')

    for uid, message in all_inbox_messages:
    # Every message is an object with the following keys

        message.sent_from
        message.sent_to
        message.subject
        message.headers
        message.message_id
        message.date
        message.body.plain
```
