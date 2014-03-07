from imaplib2 import IMAP4, IMAP4_SSL


class ImapTransport(object):
    """
    ssl should be None, SSL or STARTTLS
    """

    def __init__(self, hostname, port=None, ssl=None):
        self.hostname = hostname
        self.port = port

        if ssl == 'SSL':
            self.transport = IMAP4_SSL
            if not self.port:
                self.port = 993
        else:
            self.transport = IMAP4
            if not self.port:
                self.port = 143

        self.server = self.transport(self.hostname, self.port)
        if ssl == 'STARTTLS':
            self.server.starttls()

    def list_folders(self):
        return self.server.list()

    def connect(self, username, password):
        self.server.login(username, password)
        self.server.select()
        return self.server

