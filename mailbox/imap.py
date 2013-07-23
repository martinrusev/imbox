import email
from imaplib import IMAP4, IMAP4_SSL


class ImapTransport(object):
	
	def __init__(self, hostname, port=None, ssl=False):
		self.hostname = hostname
		self.port = port
		
		if ssl:
			self.transport = IMAP4_SSL
			if not self.port:
				self.port = 993
		else:
			self.transport = IMAP4
			if not self.port:
				self.port = 143


	def list_folders(self):
		return self.server.list()

	def connect(self, username, password):
		self.server = self.transport(self.hostname, self.port)
		typ, msg = self.server.login(username, password)

		self.server.select()

		return self.server
	

