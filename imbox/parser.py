from __future__ import unicode_literals
from six import BytesIO, binary_type

import re
import email
import base64
import quopri
import time
from datetime import datetime
from email.header import decode_header
from imbox.utils import str_encode, str_decode

import logging
logger = logging.getLogger(__name__)


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def keys(self):
        return self.__dict__.keys()

    def __repr__(self):
        return str(self.__dict__)


def decode_mail_header(value, default_charset='us-ascii'):
    """
    Decode a header value into a unicode string.
    """
    try:
        headers = decode_header(value)
    except email.errors.HeaderParseError:
        return str_decode(str_encode(value, default_charset, 'replace'), default_charset)
    else:
        for index, (text, charset) in enumerate(headers):
            logger.debug("Mail header no. {}: {} encoding {}".format(index, str_decode(text, charset or 'utf-8'), charset))
            try:
                headers[index] = str_decode(text, charset or default_charset,
                                            'replace')
            except LookupError:
                # if the charset is unknown, force default
                headers[index] = str_decode(text, default_charset, 'replace')

        return ''.join(headers)


def get_mail_addresses(message, header_name):
    """
    Retrieve all email addresses from one message header.
    """
    headers = [h for h in message.get_all(header_name, [])]
    addresses = email.utils.getaddresses(headers)

    for index, (address_name, address_email) in enumerate(addresses):
        addresses[index] = {'name': decode_mail_header(address_name),
                            'email': address_email}
        logger.debug("{} Mail addressees in message: <{}> {}".format(header_name.upper(), address_name, address_email))
    return addresses


def decode_param(param):
    name, v = param.split('=', 1)
    values = v.split('\n')
    value_results = []
    for value in values:
        match = re.search(r'=\?((?:\w|-)+)\?(Q|B)\?(.+)\?=', value)
        if match:
            encoding, type_, code = match.groups()
            if type_ == 'Q':
                value = quopri.decodestring(code)
            elif type_ == 'B':
                value = base64.decodestring(code)
            value = str_encode(value, encoding)
            value_results.append(value)
            if value_results:
                v = ''.join(value_results)
    logger.debug("Decoded parameter {} - {}".format(name, v))
    return name, v


def parse_attachment(message_part):
    # Check again if this is a valid attachment
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition is not None and not message_part.is_multipart():
        dispositions = content_disposition.strip().split(";")

        if dispositions[0].lower() in ["attachment", "inline"]:
            file_data = message_part.get_payload(decode=True)

            attachment = {
                'content-type': message_part.get_content_type(),
                'size': len(file_data),
                'content': BytesIO(file_data)
            }
            filename = message_part.get_param('name')
            if filename:
                attachment['filename'] = filename

            for param in dispositions[1:]:
                name, value = decode_param(param)

                if 'file' in name:
                    attachment['filename'] = value

                if 'create-date' in name:
                    attachment['create-date'] = value

            return attachment

    return None


def decode_content(message):
    content = message.get_payload(decode=True)
    charset = message.get_content_charset('utf-8')
    try:
        return content.decode(charset)
    except AttributeError:
        return content


def parse_email(raw_email):
    if isinstance(raw_email, binary_type):
        raw_email = str_encode(raw_email, 'utf-8')
    try:
        email_message = email.message_from_string(raw_email)
    except UnicodeEncodeError:
        email_message = email.message_from_string(raw_email.encode('utf-8'))
    maintype = email_message.get_content_maintype()
    parsed_email = {}

    parsed_email['raw_email'] = raw_email

    body = {
        "plain": [],
        "html": []
    }
    attachments = []

    if maintype in ('multipart', 'image'):
        logger.debug("Multipart message. Will process parts.")
        for part in email_message.walk():
            content_type = part.get_content_type()
            part_maintype = part.get_content_maintype()
            content_disposition = part.get('Content-Disposition', None)
            if content_disposition or not part_maintype == "text":
                content = part.get_payload(decode=True)
            else:
                content = decode_content(part)

            is_inline = content_disposition is None \
                or content_disposition == "inline"
            if content_type == "text/plain" and is_inline:
                body['plain'].append(content)
            elif content_type == "text/html" and is_inline:
                body['html'].append(content)
            elif content_disposition:
                attachment = parse_attachment(part)
                if attachment:
                    attachments.append(attachment)

    elif maintype == 'text':
        payload = decode_content(email_message)
        body['plain'].append(payload)

    parsed_email['attachments'] = attachments

    parsed_email['body'] = body
    email_dict = dict(email_message.items())

    parsed_email['sent_from'] = get_mail_addresses(email_message, 'from')
    parsed_email['sent_to'] = get_mail_addresses(email_message, 'to')
    parsed_email['cc'] = get_mail_addresses(email_message, 'cc')
    parsed_email['bcc'] = get_mail_addresses(email_message, 'bcc')

    value_headers_keys = ['subject', 'date', 'message-id']
    key_value_header_keys = ['received-spf',
                             'mime-version',
                             'x-spam-status',
                             'x-spam-score',
                             'content-type']

    parsed_email['headers'] = []
    for key, value in email_dict.items():

        if key.lower() in value_headers_keys:
            valid_key_name = key.lower().replace('-', '_')
            parsed_email[valid_key_name] = decode_mail_header(value)

        if key.lower() in key_value_header_keys:
            parsed_email['headers'].append({'Name': key,
                                            'Value': value})

    if parsed_email.get('date'):
        timetuple = email.utils.parsedate(parsed_email['date'])
        parsed_date = datetime.fromtimestamp(time.mktime(timetuple)) \
            if timetuple else None
        parsed_email['parsed_date'] = parsed_date

    logger.info("Downloaded and parsed mail '{}' with {} attachments".format(
        parsed_email.get('subject'), len(parsed_email.get('attachments'))))
    return Struct(**parsed_email)
