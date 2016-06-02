from imaplib import IMAP4, IMAP4_SSL

import logging
import ssl as pythonssllib

logger = logging.getLogger(__name__)


class ImapTransport(object):

    def __init__(self, hostname, port=None, ssl=True, ssl_context=None):
        self.hostname = hostname
        self.port = port
        kwargs = {}

        if ssl:
            self.transport = IMAP4_SSL
            if not self.port:
                self.port = 993
            if ssl_context is None:
                ssl_context = pythonssllib.create_default_context()
            kwargs["ssl_context"] = ssl_context
        else:
            self.transport = IMAP4
            if not self.port:
                self.port = 143

        self.server = self.transport(self.hostname, self.port, **kwargs)
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
