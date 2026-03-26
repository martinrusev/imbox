import imaplib
import logging

from .imap import ImapTransport
from .messages import Messages
from .vendors import GmailMessages, hostname_vendorname_dict, name_authentication_string_dict

logger = logging.getLogger(__name__)


class Imbox:
    authentication_error_message = None

    def __init__(
        self,
        hostname,
        username=None,
        password=None,
        ssl=True,
        port=None,
        ssl_context=None,
        policy=None,
        starttls=False,
        vendor=None,
    ):
        self.server = ImapTransport(hostname, ssl=ssl, port=port, ssl_context=ssl_context, starttls=starttls)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.parser_policy = policy
        self.vendor = vendor or hostname_vendorname_dict.get(self.hostname)

        if self.vendor is not None:
            self.authentication_error_message = name_authentication_string_dict.get(self.vendor)

        try:
            self.connection = self.server.connect(username, password)
        except imaplib.IMAP4.error as e:
            if self.authentication_error_message is None:
                raise
            raise imaplib.IMAP4.error(
                self.authentication_error_message + "\n" + str(e),
            ) from e

        ssl_info = " over SSL" if ssl or starttls else ""
        logger.info(
            f"Connected to IMAP Server with user {username} on {hostname}{ssl_info}",
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        self.logout()

    def logout(self):
        self.connection.close()
        self.connection.logout()
        logger.info(f"Disconnected from IMAP Server {self.username}@{self.hostname}")

    def mark_seen(self, uid):
        logger.info(f"Mark UID {int(uid)} with \\Seen FLAG")
        self.connection.uid("STORE", uid, "+FLAGS", "(\\Seen)")

    def mark_flag(self, uid):
        logger.info(f"Mark UID {int(uid)} with \\Flagged FLAG")
        self.connection.uid("STORE", uid, "+FLAGS", "(\\Flagged)")

    def delete(self, uid):
        logger.info(f"Mark UID {int(uid)} with \\Deleted FLAG and expunge.")
        self.connection.uid("STORE", uid, "+FLAGS", "(\\Deleted)")
        self.connection.expunge()

    def copy(self, uid, destination_folder):
        logger.info(f"Copy UID {int(uid)} to {destination_folder!s} folder")
        return self.connection.uid("COPY", uid, destination_folder)

    def move(self, uid, destination_folder):
        logger.info(f"Move UID {int(uid)} to {destination_folder!s} folder")
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def messages(self, **kwargs):
        folder = kwargs.get("folder", False)

        messages_class = Messages

        if self.vendor == "gmail":
            messages_class = GmailMessages

        if folder:
            status, data = self.connection.select(messages_class.FOLDER_LOOKUP.get(folder.lower()) or folder)
            if status != "OK":
                raise imaplib.IMAP4.error(data[-1])
            msg = f" from folder '{folder}'"
            del kwargs["folder"]
        else:
            msg = " from inbox"

        logger.info(f"Fetch list of messages{msg}")

        return messages_class(connection=self.connection, parser_policy=self.parser_policy, **kwargs)

    def folders(self):
        return self.connection.list()
