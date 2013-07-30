import email
from email.header import decode_header

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
	