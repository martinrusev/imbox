from imbox.imap import ImapTransport
from imbox.parser import parse_email, fetch_email_by_uid
from imbox.query import build_search_query

import logging

logger = logging.getLogger(__name__)

__version_info__ = (0, 9, 5)
__version__ = '.'.join([str(x) for x in __version_info__])


class Imbox:

    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, policy=None, starttls=False):

        self.server = ImapTransport(hostname, ssl=ssl, port=port,
                                    ssl_context=ssl_context, starttls=starttls)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.parser_policy = policy
        self.connection = self.server.connect(username, password)
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
        logger.info("Mark UID {} with \\Deleted FLAG and expunge.".format(int(uid)))
        self.connection.expunge()

    def copy(self, uid, destination_folder):
        logger.info("Copy UID {} to {} folder".format(int(uid), str(destination_folder)))
        return self.connection.uid('COPY', uid, destination_folder)

    def move(self, uid, destination_folder):
        logger.info("Move UID {} to {} folder".format(int(uid), str(destination_folder)))
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def messages(self, **kwargs):
        folder = kwargs.get('folder', False)
        msg = ""

        if folder:
            self.connection.select(folder)
            msg = " from folder '{}'".format(folder)

        logger.info("Fetch list of messages{}".format(msg))
        return Messages(connection=self.connection,
                        parser_policy=self.parser_policy,
                        **kwargs)

    def folders(self):
        return self.connection.list()


class Messages:

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):

        self.connection = connection
        self.parser_policy = parser_policy
        self.kwargs = kwargs
        self.uid_list = self.query_uids(**kwargs)

        logger.debug("Fetch all messages for UID in {}".format(self.uid_list))

    def fetch_email(self, uid):
        return fetch_email_by_uid(uid=uid,
                                  connection=self.connection,
                                  parser_policy=self.parser_policy)

    def query_uids(self, **kwargs):
        query_ = build_search_query(**kwargs)
        message, data = self.connection.uid('search', None, query_)
        if data[0] is None:
            return []
        return data[0].split()

    def fetch_email_list(self):
        for uid in self.uid_list:
            yield uid, self.fetch_email(uid)

    def __repr__(self):
        if len(self.kwargs) > 0:
            return 'Messages({})'.format('\n'.join('{}={}'.format(key, value)
                                                   for key, value in self.kwargs.items()))
        return 'Messages(ALL)'

    def __iter__(self):
        return self.fetch_email_list()

    def __next__(self):
        return self

    def __len__(self):
        return len(self.uid_list)

    def __getitem__(self, index):
        uids = self.uid_list[index]

        if not isinstance(uids, list):
            uid = uids
            return uid, self.fetch_email(uid)

        return [(uid, self.fetch_email(uid))
                for uid in uids]
