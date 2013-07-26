import email
from email.header import decode_header

def decode_mail_header(value, default_charset='us-ascii'):
	"""
	Decode a header value into a unicode string. 
	"""
	try:
		headers=email.header.decode_header(value)
	except email.errors.HeaderParseError:
		return value.encode('us-ascii', 'replace').decode('us-ascii')
	else:
		for i, (text, charset) in enumerate(headers):
			try:
				headers[i]=text.decode(charset or 'us-ascii', 'replace')
			except LookupError:
				# if the charset is unknown, force default 
				headers[i]=text.decode(default_charset, 'replace')

		return u"".join(headers)


def get_mail_addresses(message, header_name):
	"""
	retrieve all email addresses from one message header

	""" 
	addresses = email.utils.getaddresses(h for h in message.get_all(header_name, []))

	for i, (address_name, address) in enumerate(addresses):
		addresses[i]={'name': decode_mail_header(address_name), 'email': address}

	return addresses
	