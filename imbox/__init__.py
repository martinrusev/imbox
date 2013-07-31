from imbox.imap import ImapTransport
from imbox.parser import parse_email
from imbox.query import build_search_query

class Imbox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)

	def fetch_by_uid(self, uid):
		message, data = self.connection.uid('fetch', uid, '(BODY.PEEK[])') # Don't mark the messages as read, save bandwidth with PEEK
		raw_email = data[0][1]

		email_object = parse_email(raw_email)

		return email_object

	def fetch_list(self, data):
		uid_list = data[0].split()

		for uid in uid_list:
			yield self.fetch_by_uid(uid)

	def messages(self, *args, **kwargs):

		# Check for folder argument
		folder = kwargs.get('folder', False)
		
		if folder:
			self.connection.select(folder)

		query = build_search_query(**kwargs)

		message, data = self.connection.uid('search', None, query)


		return self.fetch_list(data)
		
