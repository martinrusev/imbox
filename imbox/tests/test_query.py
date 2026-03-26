from datetime import date

from imbox.messages import Messages
from imbox.query import build_search_query
from imbox.vendors.gmail import GmailMessages
from imbox.vendors.helpers import merge_two_dicts

IMAP_ATTRIBUTE_LOOKUP = Messages.IMAP_ATTRIBUTE_LOOKUP
GMAIL_ATTRIBUTE_LOOKUP = merge_two_dicts(
    IMAP_ATTRIBUTE_LOOKUP,
    GmailMessages.GMAIL_IMAP_ATTRIBUTE_LOOKUP_DIFF,
)


class TestQuery:
    def test_all(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP)
        assert res == "(ALL)"

    def test_subject(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, subject="hi")
        assert res == '(SUBJECT "hi")'

        res = build_search_query(GMAIL_ATTRIBUTE_LOOKUP, subject="hi")
        assert res == "(X-GM-RAW \"subject:'hi'\")"

    def test_unread(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, unread=True)
        assert res == "(UNSEEN)"

    def test_unflagged(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, unflagged=True)
        assert res == "(UNFLAGGED)"

    def test_flagged(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, flagged=True)
        assert res == "(FLAGGED)"

    def test_sent_from(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, sent_from="test@example.com")
        assert res == '(FROM "test@example.com")'

    def test_sent_to(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, sent_to="test@example.com")
        assert res == '(TO "test@example.com")'

    def test_date__gt(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, date__gt=date(2014, 12, 31))
        assert res == '(SINCE "31-Dec-2014")'

    def test_date__lt(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, date__lt=date(2014, 1, 1))
        assert res == '(BEFORE "01-Jan-2014")'

    def test_date__on(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, date__on=date(2014, 1, 1))
        assert res == '(ON "01-Jan-2014")'

    def test_uid__range(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, uid__range="1000:*")
        assert res == "(UID 1000:*)"

    def test_text(self):
        res = build_search_query(IMAP_ATTRIBUTE_LOOKUP, text="mail body")
        assert res == '(TEXT "mail body")'

    def test_gmail_raw(self):
        res = build_search_query(GMAIL_ATTRIBUTE_LOOKUP, raw='has:attachment subject:"hey"')
        assert res == "(X-GM-RAW \"has:attachment subject:'hey'\")"

    def test_gmail_label(self):
        res = build_search_query(GMAIL_ATTRIBUTE_LOOKUP, label="finance")
        assert res == '(X-GM-LABELS "finance")'
