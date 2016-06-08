Imbox - Python IMAP for Humans
=======

[![Build Status](https://travis-ci.org/martinrusev/imbox.svg?branch=master)](https://travis-ci.org/martinrusev/imbox)


Python library for reading IMAP mailboxes and converting email content to machine readable data



Installation
============

	pip install imbox


Usage 
=====

```python
from imbox import Imbox

# SSL Context docs https://docs.python.org/2/library/ssl.html#ssl.create_default_context

imbox = Imbox('imap.gmail.com',
		username='username', 
		password='password',
		ssl=True,
		ssl_context=None)

# Gets all messages 
all_messages = imbox.messages()

# Unread messages 
unread_messages = imbox.messages(unread=True)

# Messages sent FROM
messages_from = imbox.messages(sent_from='martin@amon.cx')

# Messages sent TO
messages_from = imbox.messages(sent_to='martin@amon.cx')

# Messages received before specific date
messages_from = imbox.messages(date__lt='31-July-2013')

# Messages received after specific date
messages_from = imbox.messages(date__gt='30-July-2013')

# Messages from a specific folder 
messages_folder = imbox.messages(folder='Social')



for uid, message in all_messages:
	........
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
	print message.keys()


# To check the whole object, just write

	print message

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
		'plain: ['ASCII'],
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
```


# [Changelog](https://github.com/martinrusev/imbox/blob/master/CHANGELOG.md)
