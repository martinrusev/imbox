import imaplib

from imbox.imap import ImapTransport
from imbox.messages import Messages

import logging

from imbox.vendors import GmailMessages, hostname_vendorname_dict, name_authentication_string_dict

logger = logging.getLogger(__name__)


class Imbox:

    authentication_error_message = None

    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, policy=None, starttls=False,
                 vendor=None):

        self.server = ImapTransport(hostname, ssl=ssl, port=port,
                                    ssl_context=ssl_context, starttls=starttls)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.parser_policy = policy
        self.vendor = vendor or hostname_vendorname_dict.get(self.hostname)

        if self.vendor is not None:
            self.authentication_error_message = name_authentication_string_dict.get(
                self.vendor)

        try:
            self.connection = self.server.connect(username, password)
        except imaplib.IMAP4.error as e:
            if self.authentication_error_message is None:
                raise
            raise imaplib.IMAP4.error(
                self.authentication_error_message + '\n' + str(e))

        logger.info("Connected to IMAP Server with user {username} on {hostname}{ssl}".format(
            hostname=hostname, username=username, ssl=(" over SSL" if ssl or starttls else "")))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def logout(self):
        self.connection.close()
        self.connection.logout()
        logger.info("Disconnected from IMAP Server {username}@{hostname}".format(
            hostname=self.hostname, username=self.username))

    def mark_seen(self, uid):
        logger.info("Mark UID {} with \\Seen FLAG".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Seen)')

    def mark_flag(self, uid):
        logger.info("Mark UID {} with \\Flagged FLAG".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Flagged)')

    def delete(self, uid):
        logger.info(
            "Mark UID {} with \\Deleted FLAG and expunge.".format(int(uid)))
        self.connection.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        self.connection.expunge()

    def copy(self, uid, destination_folder):
        logger.info("Copy UID {} to {} folder".format(
            int(uid), str(destination_folder)))
        return self.connection.uid('COPY', uid, destination_folder)

    def move(self, uid, destination_folder):
        logger.info("Move UID {} to {} folder".format(
            int(uid), str(destination_folder)))
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def messages(self, **kwargs):
        folder = kwargs.get('folder', False)

        messages_class = Messages

        if self.vendor == 'gmail':
            messages_class = GmailMessages

        if folder:
            self.connection.select(
                messages_class.FOLDER_LOOKUP.get((folder.lower())) or folder)
            msg = " from folder '{}'".format(folder)
            del kwargs['folder']
        else:
            msg = " from inbox"

        logger.info("Fetch list of messages{}".format(msg))

        return messages_class(connection=self.connection,
                              parser_policy=self.parser_policy,
                              **kwargs)

    def folders(self):
        return self.connection.list()
