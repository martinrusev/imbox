from imaplib import IMAP4, IMAP4_SSL
from ssl import SSLContext
from typing import Optional, Union, Tuple, List


class ImapTransport:

    def __init__(self, hostname: str, port: Optional[int], ssl: bool,
                 ssl_context: Optional[SSLContext], starttls: bool) -> None: ...

    def list_folders(self) -> Tuple[str, List[bytes]]: ...

    def connect(self, username: str, password: str) -> Union[IMAP4, IMAP4_SSL]: ...
