from unittest.mock import Mock

import pytest

from imbox.imbox import Imbox


@pytest.mark.parametrize("status", ["NO", "BAD"])
def test_failed_copy_does_not_delete_original(status):
    mailbox = object.__new__(Imbox)
    mailbox.connection = Mock()
    mailbox.connection.uid.return_value = (status, [b"copy failed"])
    mailbox.move(b"42", "Archive")
    mailbox.connection.uid.assert_called_once_with("COPY", b"42", "Archive")
    mailbox.connection.expunge.assert_not_called()


def test_successful_copy_deletes_original():
    mailbox = object.__new__(Imbox)
    mailbox.connection = Mock()
    mailbox.connection.uid.return_value = ("OK", [b"copied"])
    mailbox.move(b"42", "Archive")
    assert [call.args for call in mailbox.connection.uid.call_args_list] == [
        ("COPY", b"42", "Archive"),
        ("STORE", b"42", "+FLAGS", "(\\Deleted)"),
    ]
    mailbox.connection.expunge.assert_called_once_with()
