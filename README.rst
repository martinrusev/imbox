Imbox - Python IMAP for Humans
==============================


.. image:: https://travis-ci.org/martinrusev/imbox.svg?branch=master
   :target: https://travis-ci.org/martinrusev/imbox
   :alt: Build Status


Python library for reading IMAP mailboxes and converting email content to machine readable data

Requirements
------------

Python (3.3, 3.4, 3.5, 3.6, 3.7)


Installation
------------

``pip install imbox``


Usage 
-----

.. code:: python

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
            message.body.html
            message.attachments

        # To check all available keys
            print(message.keys())


        # To check the whole object, just write

            print(message)

            {
            'headers':
                [{
                    'Name': 'Received-SPF',
                    'Value': 'pass (google.com: domain of ......;'
                },
                {
                    'Name': 'MIME-Version',
                    'Value': '1.0'
                }],
            'body': {
                'plain': ['ASCII'],
                'html': ['HTML BODY']
            },
            'attachments':  [{
                'content': <StringIO.StringIO instance at 0x7f8e8445fa70>,
                'filename': "avatar.png",
                'content-type': 'image/png',
                'size': 80264
            }],
            'date': u 'Fri, 26 Jul 2013 10:56:26 +0300',
            'message_id': u '51F22BAA.1040606',
            'sent_from': [{
                'name': u 'Martin Rusev',
                'email': 'martin@amon.cx'
            }],
            'sent_to': [{
                'name': u 'John Doe',
                'email': 'john@gmail.com'
            }],
            'subject': u 'Hello John, How are you today'
            }

        # With the message id, several actions on the message are available:
        # delete the message
        imbox.delete(uid)

        # mark the message as read
        imbox.mark_seen(uid)



Changelog
---------

`Changelog <https://github.com/martinrusev/imbox/blob/master/CHANGELOG.md>`_


Running the tests
-----------------

You can run the imbox tests with ``tox``.

Requirements:
 * the supported python versions
 * ``tox``. Tox is packaged in Debian and derivatives distributions.

On Ubuntu, you can install several python versions with:

.. code:: sh

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.X
