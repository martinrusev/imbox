import re
import StringIO
import email
import base64, quopri
import time 
from datetime import datetime
from email.header import Header, decode_header


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


def decode_param(param):
	name, v = param.split('=', 1)
	values = v.split('\n')
	value_results = []
	for value in values:
		match = re.search(r'=\?(\w+)\?(Q|B)\?(.+)\?=', value)
		if match:
			encoding, type_, code = match.groups()
			if type_ == 'Q':
				value = quopri.decodestring(code)
			elif type_ == 'B':
				value = base64.decodestring(code)
			value = unicode(value, encoding)
			value_results.append(value)
	if value_results: v = ''.join(value_results)
	return name, v 



def parse_attachment(message_part):
	content_disposition = message_part.get("Content-Disposition", None) # Check again if this is a valid attachment
	if content_disposition != None:
		dispositions = content_disposition.strip().split(";")
		
		if dispositions[0].lower() in ["attachment", "inline"]:
			file_data = message_part.get_payload(decode=True)

			attachment = {
				'content-type': message_part.get_content_type(),
				'size': len(file_data),
				'content': StringIO.StringIO(file_data)
			}

			for param in dispositions[1:]:
				name, value = decode_param(param)

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
				attachment = parse_attachment(part)
				if attachment: attachments.append(attachment)
	
	elif maintype == 'text':
		body['plain'].append(email_message.get_payload(decode=True))

	parsed_email['attachments'] = attachments

	parsed_email['body'] = body
	email_dict = dict(email_message.items())

	parsed_email['sent_from'] = get_mail_addresses(email_message, 'from')
	parsed_email['sent_to'] = get_mail_addresses(email_message, 'to')


	value_headers_keys = ['subject', 'date','message-id']
	key_value_header_keys = ['received-spf', 
							'mime-version',
							'x-spam-status',
							'x-spam-score',
							'content-type']

	parsed_email['headers'] = []
	for key, value in email_dict.iteritems():
		
		if key.lower() in value_headers_keys:
			valid_key_name = key.lower().replace('-', '_')
			parsed_email[valid_key_name] = decode_mail_header(value)
		
		if key.lower() in key_value_header_keys:
			parsed_email['headers'].append({'Name': key,
				'Value': value})

	if parsed_email.get('date'):
		timetuple = email.utils.parsedate(parsed_email['date'])
		parsed_email['parsed_date'] = datetime.fromtimestamp(time.mktime(timetuple)) if timetuple else None

	return Struct(**parsed_email)

