import imaplib
from unittest.mock import Mock

import pytest

from imbox.messages import Messages


@pytest.mark.parametrize("status", ["NO", "BAD"])
def test_search_failure_is_not_treated_as_message_uids(status):
    connection = Mock()
    connection.uid.return_value = (status, [b"search failed"])
    with pytest.raises(imaplib.IMAP4.error, match="search failed"):
        Messages(connection, parser_policy=None)
    connection.uid.assert_called_once_with("search", None, "(ALL)")


@pytest.mark.parametrize("data", [[b""], [None]])
def test_successful_empty_search(data):
    connection = Mock()
    connection.uid.return_value = ("OK", data)
    assert list(Messages(connection, parser_policy=None)) == []
