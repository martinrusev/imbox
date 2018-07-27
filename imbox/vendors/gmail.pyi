import datetime
from email._policybase import Policy
from imaplib import IMAP4, IMAP4_SSL
from typing import Union

from imbox.messages import Messages


class GmailMessages(Messages):

    def __init__(self,
                 connection: Union[IMAP4, IMAP4_SSL],
                 parser_policy: Policy,
                 **kwargs: Union[bool, str, datetime.date]) -> None: ...
