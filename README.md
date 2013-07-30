Imbox - Python IMAP for Humans
=======

Python library for reading IMAP mailboxes and converting the email content to human readable data

Installation
============

	pip install imbox


or 

	git clone git@github.com:martinrusev/imbox.git
	python setup.py install


Usage 
=====


	from imbox import Imbox

	imbox = Imbox('imap.gmail.com',
				  username='username', 
				  password='password',
				  ssl=True)
	
	# Gets all messages 
	all_messages = imbox.messages()
	
	# Unread messages 
	unread_messages = imbox.messages(unread=True)


	for message in all_messages:
		........
	# Every message is an object with the following keys
		
		message.sent_from
		message.sent_to
		message.subject
		message.headers
		message.message-id
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



