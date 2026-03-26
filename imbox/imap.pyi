from imaplib import IMAP4, IMAP4_SSL
from ssl import SSLContext

class ImapTransport:
    def __init__(
        self,
        hostname: str,
        port: int | None,
        ssl: bool,
        ssl_context: SSLContext | None,
        starttls: bool,
    ) -> None: ...
    def list_folders(self) -> tuple[str, list[bytes]]: ...
    def connect(self, username: str, password: str) -> IMAP4 | IMAP4_SSL: ...
