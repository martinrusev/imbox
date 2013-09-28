from imbox.imap import ImapTransport
from imbox.parser import parse_email
from imbox.query import build_search_query
import re

class Imbox(object):

    def __init__(self, hostname, username=None, password=None, ssl=True):

        self.server = ImapTransport(hostname, ssl=ssl)
        self.connection = self.server.connect(username, password)
        self.username = username
        self.password = password

    def __enter__(self):
        self.connection()

    def __exit__(self, type, value, traceback):
        self.logout()

    def connect(self):
        username = self.username
        password = self.password
        self.connection = self.connection


    def logout(self):
        self.connection.logout()

    def query_uids(self, **kwargs):
        query = build_search_query(**kwargs)

        message, data = self.connection.uid('search', None, query)
        return data[0].split()

    def fetch_by_uid(self, uid):
        message, data = self.connection.uid('fetch', uid, '(X-GM-MSGID X-GM-THRID UID FLAGS BODY.PEEK[])') # Don't mark the messages as read, save bandwidth with PEEK
        raw_email = data[0][1]

        pattern = re.compile("^(\d+) \(X-GM-THRID (?P<gthrid>\d+) X-GM-MSGID (?P<gmsgid>\d+) UID (?P<uid>\d+) FLAGS \((?P<flags>[^\)]*)\)")
        self.maildata = {}
        headers = data[0][0]
        groups = pattern.match(headers).groups()
        self.maildata['GTHRID'] = groups[1]
        self.maildata['GMSGID'] = groups[2]
        self.maildata['UID'] = groups[3]
        self.maildata['FLAGS'] = groups[4]
        self.maildata['data'] = raw_email

        email_object = parse_email(self.maildata)
        return email_object

    def fetch_list(self, **kwargs):
        uid_list = self.query_uids(**kwargs)

        for uid in uid_list:
            yield (uid, self.fetch_by_uid(uid))

    def mark_seen(self, uid):
        self.connection.uid('STORE', uid, '+FLAGS', '\\Seen')

    def delete(self, uid):
        mov, data = self.connection.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        self.connection.expunge()

    def copy(self, uid, destination_folder):
        return self.connection.uid('COPY', uid, destination_folder)

    def move(self, uid, destination_folder):
        if self.copy(uid, destination_folder):
            self.delete(uid)

    def messages(self, *args, **kwargs):
        folder = kwargs.get('folder', False)
        read_only = kwargs.get('readonly', True)
        
        if folder:
            self.connection.select(folder, readonly=read_only)

        return self.fetch_list(**kwargs)
