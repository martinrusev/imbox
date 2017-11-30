import unittest
from imbox.query import build_search_query
from datetime import date


class TestQuery(unittest.TestCase):

    def test_all(self):

        res = build_search_query()
        self.assertEqual(res, "(ALL)")

    def test_unread(self):

        res = build_search_query(unread=True)
        self.assertEqual(res, "(UNSEEN)")

    def test_unflagged(self):

        res = build_search_query(unflagged=True)
        self.assertEqual(res, "(UNFLAGGED)")

    def test_flagged(self):

        res = build_search_query(flagged=True)
        self.assertEqual(res, "(FLAGGED)")

    def test_sent_from(self):

        res = build_search_query(sent_from='test@example.com')
        self.assertEqual(res, '(FROM "test@example.com")')

    def test_sent_to(self):

        res = build_search_query(sent_to='test@example.com')
        self.assertEqual(res, '(TO "test@example.com")')

    def test_date__gt(self):

        res = build_search_query(date__gt=date(2014, 12, 31))
        self.assertEqual(res, '(SINCE "31-Dec-2014")')

    def test_date__lt(self):

        res = build_search_query(date__lt=date(2014, 1, 1))
        self.assertEqual(res, '(BEFORE "01-Jan-2014")')

    def test_date__on(self):
        res = build_search_query(date__on=date(2014, 1, 1))
        self.assertEqual(res, '(ON "01-Jan-2014")')
