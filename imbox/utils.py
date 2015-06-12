from __future__ import unicode_literals
from six import PY3

import logging
logger = logging.getLogger(__name__)

if PY3:
    def str_encode(value='', encoding=None, errors='strict'):
        logger.debug("Encode str {} with and errors {}".format(value, encoding, errors))
        return str(value, encoding, errors)

    def str_decode(value='', encoding=None, errors='strict'):
        return bytes(value, encoding, errors).decode('utf-8')
else:
    def str_encode(string='', encoding=None, errors='strict'):
        return unicode(string, encoding, errors)

    def str_decode(value='', encoding=None, errors='strict'):
        return value.decode(encoding, errors)
