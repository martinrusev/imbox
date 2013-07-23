import email
from mailbox.imap import ImapTransport

class MailBox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)



	def parse_email(self, raw_email):

		email_message = email.message_from_string(raw_email)
		headers = dict(email_message.items())

		maintype = email_message.get_content_maintype()

		message = []
		
		if maintype == 'multipart':
			for part in email_message.get_payload():
				if part.get_content_maintype() == 'text':
					message.append(part.get_payload(decode=True))
		elif maintype == 'text':
			message.append(email_message.get_payload(decode=True))

		return {
			'message': message,
			'headers': headers,
			'maintype': maintype
		}


	def get_unread(self):

		result, data = self.connection.uid('search', None, "ALL") # search and return uids instead
		latest_email_uid = data[0].split()[-1]
		result, data = self.connection.uid('fetch', latest_email_uid, '(RFC822)')

		raw_email = data[0][1]

		print self.parse_email(raw_email)

	
		return {}