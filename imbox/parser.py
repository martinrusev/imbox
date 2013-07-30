import re
import StringIO
import email
from email.header import decode_header


class Struct(object):
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def keys(self):
		return self.__dict__.keys()

	def __repr__(self):
		return str(self.__dict__)


def decode_mail_header(value, default_charset='us-ascii'):
	"""
	Decode a header value into a unicode string. 
	"""
	try:
		headers=decode_header(value)
	except email.errors.HeaderParseError:
		return value.encode(default_charset, 'replace').decode(default_charset)
	else:
		for index, (text, charset) in enumerate(headers):
			try:
				headers[index]=text.decode(charset or default_charset, 'replace')
			except LookupError:
				# if the charset is unknown, force default 
				headers[index]=text.decode(default_charset, 'replace')

		return u"".join(headers)


def get_mail_addresses(message, header_name):
	"""
	Retrieve all email addresses from one message header.
	""" 
	addresses = email.utils.getaddresses(header for header in message.get_all(header_name, []))

	for index, (address_name, address_email) in enumerate(addresses):
		addresses[index]={'name': decode_mail_header(address_name), 'email': address_email}

	return addresses

def parse_attachment(message_part):
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

def parse_email(raw_email):
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
				attachments.append(parse_attachment(part))
	
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