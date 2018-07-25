from imaplib import IMAP4, IMAP4_SSL

import logging
import ssl as pythonssllib

logger = logging.getLogger(__name__)


class ImapTransport:

    def __init__(self, hostname, port=None, ssl=True, ssl_context=None, starttls=False):
        self.hostname = hostname

        if ssl:
            self.port = port or 993
            if ssl_context is None:
                ssl_context = pythonssllib.create_default_context()
            self.server = IMAP4_SSL(self.hostname, self.port, ssl_context=ssl_context)
        else:
            self.port = port or 143
            self.server = IMAP4(self.hostname, self.port)

        if starttls:
            self.server.starttls()
        logger.debug("Created IMAP4 transport for {host}:{port}"
                     .format(host=self.hostname, port=self.port))

    def list_folders(self):
        logger.debug("List all folders in mailbox")
        return self.server.list()

    def connect(self, username, password):
        self.server.login(username, password)
        self.server.select()
        logger.debug("Logged into server {} and selected mailbox 'INBOX'"
                     .format(self.hostname))
        return self.server
