import email
from mailbox.imap import ImapTransport

class MailBox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)


	def parse_email(self, raw_email):

		email_message = email.message_from_string(raw_email)
		

		maintype = email_message.get_content_maintype()

		text_body = []
		
		if maintype == 'multipart':
			for part in email_message.walk():       
				if part.get_content_type() == "text/plain":
					text_body.append(part.get_payload(decode=True))
		elif maintype == 'text':
			text_body.append(email_message.get_payload(decode=True))

		email_dict = dict(email_message.items())

		from_dict = {}
		from_ = email.utils.parseaddr(email_dict['From'])
		if len(from_) == 2:
			from_dict = {'Name': from_[0], 'Email': from_[1]}

		to_dict = {}
		to_ =  email.utils.parseaddr(email_dict['To'])
		if len(to_) == 2:
			to_dict = {'Name': to_[0], 'Email': to_[1]}

		subject = email_dict.get('Subject', None)
		date = email_dict.get('Date', None)
		message_id = email_dict.get('Message-ID', None)

		# Get the headers
		headers = []
		headers_keys = ['Received-SPF', 
						'MIME-Version',
						'X-Spam-Status',
						'X-Spam-Score']

		for key in headers_keys:
			header_value = email_dict.get(key)

			if header_value:
				headers.append({'Name': key,
					'Value': header_value})

		return {
			'MesssageID': message_id,
			'From': from_dict,
			'To': to_dict, 
			'Subject': subject,
			'Date': date,
			'TextBody': text_body,
			'Headers': headers
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
