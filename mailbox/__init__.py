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

	def fetch_by_uid(self, uid):
		message, data = self.connection.uid('fetch', uid, '(RFC822)')

		raw_email = data[0][1]

		email_metadata = self.parse_email(raw_email)

		return email_metadata

	def fetch_list(self, data):
		uid_list = data[0].split()

		messages_list = []
		for uid in uid_list:
			messages_list.append(self.fetch_by_uid(uid))
			

	def get_all(self):
		message, data = self.connection.uid('search', None, "ALL")

		return self.fetch_list(data)


	def get_unread(self):
		message, data = self.connection.uid('search', None, "UNSEEN")

		return self.fetch_list(data)
		