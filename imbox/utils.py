import datetime
import logging
from imaplib import Time2Internaldate

logger = logging.getLogger(__name__)


def str_encode(value="", encoding=None, errors="strict"):
    logger.debug(f"Encode str {value} with encoding {encoding} and errors {errors}")
    return str(value, encoding, errors)


def str_decode(value="", encoding=None, errors="strict"):
    if isinstance(value, str):
        return bytes(value, encoding, errors).decode("utf-8")
    if isinstance(value, bytes):
        return value.decode(encoding or "utf-8", errors=errors)
    raise TypeError(f"Cannot decode '{value.__class__}' object")


def date_to_date_text(date):
    """Return a date in the RFC 3501 date-text syntax"""
    tzutc = datetime.UTC
    dt = datetime.datetime.combine(date, datetime.time.min, tzutc)
    return Time2Internaldate(dt)[1:12]
