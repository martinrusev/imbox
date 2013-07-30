import email
import re
import StringIO
from imbox.imap import ImapTransport
from imbox.parser import get_mail_addresses, decode_mail_header


class Struct(object):
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def keys(self):
		return self.__dict__.keys()

	def __repr__(self):
		return str(self.__dict__)


class Imbox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)

	def parse_attachment(self, message_part):
		content_disposition = message_part.get("Content-Disposition", None) # Check again if this is a valid attachment
		if content_disposition != None:
			dispositions = content_disposition.strip().split(";")
			
			if dispositions[0].lower() == "attachment":
				file_data = message_part.get_payload(decode=True)

				attachment = {
					'content-type': message_part.get_content_type(),
					'size': len(file_data),
					'content': StringIO.StringIO(file_data)
				}

				
				for param in dispositions[1:]:
					name,value = param.split("=")
					name = name.lower()

					if 'file' in  name:
						attachment['filename'] = value
					
					if 'create-date' in name:
						attachment['create-date'] = value
				
				return attachment

		return None


	def parse_email(self, raw_email):
		email_message = email.message_from_string(raw_email)
		maintype = email_message.get_content_maintype()
		parsed_email = {}
		
		body = {
			"plain": [],
			"html": []
		}
		attachments = []

		if maintype == 'multipart':
			for part in email_message.walk():
				content = part.get_payload(decode=True)
				content_type = part.get_content_type()
				content_disposition = part.get('Content-Disposition', None)
				
				if content_type == "text/plain" and content_disposition == None:
					body['plain'].append(content)
				elif content_type == "text/html" and content_disposition == None:
					body['html'].append(content)
				elif content_disposition:
					attachments.append(self.parse_attachment(part))
		
		elif maintype == 'text':
			body['plain'].append(email_message.get_payload(decode=True))

		if len(attachments) > 0:
			parsed_email['attachments'] = attachments

		parsed_email['body'] = body
		email_dict = dict(email_message.items())

		parsed_email['sent_from'] = get_mail_addresses(email_message, 'from')
		parsed_email['sent_to'] = get_mail_addresses(email_message, 'to')


		value_headers_keys = ['Subject', 'Date','Message-ID']
		key_value_header_keys = ['Received-SPF', 
								'MIME-Version',
								'X-Spam-Status',
								'X-Spam-Score',
								'Content-Type']

		parsed_email['headers'] = []
		for key, value in email_dict.iteritems():
			
			if key in value_headers_keys:
				valid_key_name = key.lower()
				parsed_email[valid_key_name] = decode_mail_header(value)
			
			if key in key_value_header_keys:
				parsed_email['headers'].append({'Name': key,
					'Value': value})

		return Struct(**parsed_email)

	def fetch_by_uid(self, uid):
		message, data = self.connection.uid('fetch', uid, '(BODY.PEEK[])') # Don't mark the messages as read
		raw_email = data[0][1]

		email_object = self.parse_email(raw_email)

		return email_object

	def fetch_list(self, data):
		uid_list = data[0].split()

		for uid in uid_list:
			yield self.fetch_by_uid(uid)

	def messages(self, *args, **kwargs):

		query = "ALL"

		# Parse keyword arguments 
		unread = kwargs.get('unread', False)
		folder = kwargs.get('folder', False)
		sent_from = kwargs.get('sent_from', False)
		sent_to = kwargs.get('sent_to', False)

		if unread != False:
			query = "UNSEEN"

		message, data = self.connection.uid('search', None, query)

		return self.fetch_list(data)
		
