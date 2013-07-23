Mailbox
=======

Small Python library for reading IMAP email boxes and parsing the content to JSON


Usage 
=====


	from mailbox import MailBox

	mailbox = MailBox('imap.gmail.com',
				  username='username', 
				  password='password',
				  ssl=True)

	unread = mailbox.get_unread()

	for message in unread:
		print message.json()

