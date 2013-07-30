from imbox.imap import ImapTransport
from imbox.parser import parse_email

class Imbox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)

	def fetch_by_uid(self, uid):
		message, data = self.connection.uid('fetch', uid, '(BODY.PEEK[])') # Don't mark the messages as read
		raw_email = data[0][1]

		email_object = parse_email(raw_email)

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
		
