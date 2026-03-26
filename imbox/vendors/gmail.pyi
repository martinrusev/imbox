import datetime
from email._policybase import Policy
from imaplib import IMAP4, IMAP4_SSL

from imbox.messages import Messages

class GmailMessages(Messages):
    def __init__(
        self,
        connection: IMAP4 | IMAP4_SSL,
        parser_policy: Policy,
        **kwargs: bool | str | datetime.date,
    ) -> None: ...
