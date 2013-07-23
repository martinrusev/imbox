import sys
sys.path.insert(0, '/home/martin/mailbox')

from mailbox import MailBox

mailbox = MailBox('imap.gmail.com',
				  username='username',
				  password='password')

unread = mailbox.get_unread()

for message in unread:
	print message.json()