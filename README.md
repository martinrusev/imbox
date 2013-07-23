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


	# Gets all unread messages
	unread_messages = mailbox.get_unread()

	# Gets all messages 
	all_messages = mailbox.get_all()


	for message in all_messages:
		........

	# Every message is converted to a dictionary with the following keys:

	{
		'MesssageID': '22c74902-a0c1-4511-804f2-341342852c90',
		'From': {
			'Name': 'John Doe',
			'Email': 'jonhdoe@email.com'
		},
		'To': {
			'Name': 'Martin Rusev',
			'Email': 'martin@amon.cx'
		},
		'Date': 'Mon, 22 Jul 2013 23:21:39 +0000 (UTC)',
		'TextBody': ['ASCII'],
		'Subject': 'This is a message'

		'Headers': [{
			'Name': 'Received-SPF',
			'Value': 'pass (google.com: domain of bounces+......;'
		}, {
			'Name': 'MIME-Version',
			'Value': '1.0'
		}],
		
	}





