# Imbox - Python IMAP for Humans

![workflow](https://github.com/martinrusev/imbox/actions/workflows/python-app.yml/badge.svg)

Python library for reading IMAP mailboxes and converting email content
to machine readable data

## Requirements

Python (3.6, 3.7, 3.8, 3.9)

## Installation

`pip install imbox`

## Usage

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
    unread_inbox_messages = imbox.messages(unread=True)

    # Flagged messages
    inbox_flagged_messages = imbox.messages(flagged=True)

    # Un-flagged messages
    inbox_unflagged_messages = imbox.messages(unflagged=True)

    # Flagged messages
    flagged_messages = imbox.messages(flagged=True)

    # Un-flagged messages
    unflagged_messages = imbox.messages(unflagged=True)

    # Messages sent FROM
    inbox_messages_from = imbox.messages(sent_from='sender@example.org')

    # Messages sent TO
    inbox_messages_to = imbox.messages(sent_to='receiver@example.org')

    # Messages received before specific date
    inbox_messages_received_before = imbox.messages(date__lt=datetime.date(2018, 7, 31))

    # Messages received after specific date
    inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2018, 7, 30))

    # Messages received on a specific date
    inbox_messages_received_on_date = imbox.messages(date__on=datetime.date(2018, 7, 30))

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
