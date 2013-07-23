from mailbox.imap import ImapTransport

class MailBox(object):

	def __init__(self, hostname, username=None, password=None, ssl=True):

		server = ImapTransport(hostname, ssl=ssl)
		self.connection = server.connect(username, password)


	def get_unread(self):
		return {}