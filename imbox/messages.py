from .logger import get_logger

from .parser import EmailObject, parse_email, parse_flags
from .query import build_search_query

logger = get_logger(__name__)


class Messages:
    IMAP_ATTRIBUTE_LOOKUP = {
        "unread": "(UNSEEN)",
        "flagged": "(FLAGGED)",
        "unflagged": "(UNFLAGGED)",
        "sent_from": '(FROM "{}")',
        "sent_to": '(TO "{}")',
        "date__gt": '(SINCE "{}")',
        "date__lt": '(BEFORE "{}")',
        "date__on": '(ON "{}")',
        "subject": '(SUBJECT "{}")',
        "uid__range": "(UID {})",
        "text": '(TEXT "{}")',
    }

    FOLDER_LOOKUP: dict[str, str] = {}

    def __init__(self, connection, parser_policy, **kwargs):
        self.connection = connection
        self.parser_policy = parser_policy
        self.kwargs = kwargs
        self._uid_list = self._query_uids(**kwargs)

        logger.debug(f"Fetch all messages for UID in {self._uid_list}")

    def fetch_email_by_uid(self, uid):
        _, data = self.connection.uid("fetch", uid, "(BODY.PEEK[] FLAGS)")
        logger.debug(f"Fetched message for UID {int(uid)}")

        raw_headers = data[0][0] + data[1]
        raw_email = data[0][1]

        email = EmailObject(
            uid=int(uid),
            parsed=parse_email(raw_email, policy=self.parser_policy),
            flags=parse_flags(raw_headers.decode()),
        )

        return email

    def _fetch_email(self, uid):
        return self.fetch_email_by_uid(uid=uid)

    def _query_uids(self, **kwargs):
        query_ = build_search_query(self.IMAP_ATTRIBUTE_LOOKUP, **kwargs)
        _, data = self.connection.uid("search", None, query_)
        if data[0] is None:
            return []
        return data[0].split()

    def _fetch_email_list(self):
        for uid in self._uid_list:
            yield uid, self._fetch_email(uid)

    def __repr__(self):
        if len(self.kwargs) > 0:
            return "Messages({})".format("\n".join(f"{key}={value}" for key, value in self.kwargs.items()))
        return "Messages(ALL)"

    def __iter__(self):
        return self._fetch_email_list()

    def __next__(self):
        return self

    def __len__(self):
        return len(self._uid_list)

    def to_dict_filtered(self):
        result = {}

        for uid in self._uid_list:
            email = self._fetch_email(uid)
            result[uid] = email.filtered()

        return result

    def __getitem__(self, index):
        uids = self._uid_list[index]

        if not isinstance(uids, list):
            uid = uids
            return uid, self._fetch_email(uid)

        return [(uid, self._fetch_email(uid)) for uid in uids]
