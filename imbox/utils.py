import datetime
import logging
from imaplib import Time2Internaldate
logger = logging.getLogger(__name__)


def str_encode(value='', encoding=None, errors='strict'):
    logger.debug("Encode str {value} with encoding {encoding} and errors {errors}".format(
        value=value,
        encoding=encoding,
        errors=errors))
    return str(value, encoding, errors)


def str_decode(value='', encoding=None, errors='strict'):
    if isinstance(value, str):
        return bytes(value, encoding, errors).decode('utf-8')
    elif isinstance(value, bytes):
        return value.decode(encoding or 'utf-8', errors=errors)
    else:
        raise TypeError("Cannot decode '{}' object".format(value.__class__))


def date_to_date_text(date):
    """Return a date in the RFC 3501 date-text syntax"""
    tzutc = datetime.timezone.utc
    dt = datetime.datetime.combine(date, datetime.time.min, tzutc)
    return Time2Internaldate(dt)[1:12]
