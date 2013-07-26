Mailbox - Python IMAP for Humans
=======

Python library for reading IMAP mailboxes and converting the email content to human readable data

Installation
============

	pip install mailbox


or 

	git clone git@github.com:martinrusev/mailbox.git
	python setup.py install


Usage 
=====


	from mailbox import MailBox

	mailbox = MailBox('imap.gmail.com',
				  username='username', 
				  password='password',
				  ssl=True)
	
	# Gets all messages 
	all_messages = mailbox.messages()
	
	# Unread messages 
	unread_messages = mailbox.messages(unread=True)


	for message in all_messages:
		........
	# Every message is an object with the following keys
		
		message.sent_from
		message.sent_to
		message.subject
		message.headers
		message.message-id
		message.date
		message.text_body

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
		'text_body': ['ASCII'],
		'date': u 'Fri, 26 Jul 2013 10:56:26 +0300',
		'message-id': u '51F22BAA.1040606',
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

TODO
======

- Replace the dictionaries with objects and generators
- Add logging and exceptions 
- Implement smarter header parsing



