Mailbox
=======

Python library for reading IMAP email boxes


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





