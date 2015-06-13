import datetime
import logging
# TODO - Validate query arguments

logger = logging.getLogger(__name__)

IMAP_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def format_date(date):

    return "%s-%s-%s" % (date.day, IMAP_MONTHS[date.month - 1], date.year)


def build_search_query(**kwargs):

    # Parse keyword arguments
    unread = kwargs.get('unread', False)
    sent_from = kwargs.get('sent_from', False)
    sent_to = kwargs.get('sent_to', False)
    date__gt = kwargs.get('date__gt', False)
    if type(date__gt) is datetime.date:
        date__gt = format_date(date__gt)
    date__lt = kwargs.get('date__lt', False)
    if type(date__lt) is datetime.date:
        date__lt = format_date(date__lt)
    subject = kwargs.get('subject')

    query = []

    if unread:
        query.append("(UNSEEN)")

    if sent_from:
        query.append('(FROM "%s")' % sent_from)

    if sent_to:
        query.append('(TO "%s")' % sent_to)

    if date__gt:
        query.append('(SINCE "%s")' % date__gt)

    if date__lt:
        query.append('(BEFORE "%s")' % date__lt)

    if subject is not None:
        query.append('(SUBJECT "%s")' % subject)

    if query:
        logger.debug("IMAP query: {}".format(" ".join(query)))
        return " ".join(query)

    logger.debug("IMAP query: {}".format("(ALL)"))
    return "(ALL)"
