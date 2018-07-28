import logging
logger = logging.getLogger(__name__)


def str_encode(value='', encoding=None, errors='strict'):
    logger.debug("Encode str {} with and errors {}".format(value, encoding, errors))
    return str(value, encoding, errors)


def str_decode(value='', encoding=None, errors='strict'):
    if isinstance(value, str):
        return bytes(value, encoding, errors).decode('utf-8')
    elif isinstance(value, bytes):
        return value.decode(encoding or 'utf-8', errors=errors)
    else:
        raise TypeError("Cannot decode '{}' object".format(value.__class__))
