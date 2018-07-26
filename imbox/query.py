import datetime
import logging
# TODO - Validate query arguments

logger = logging.getLogger(__name__)


def format_date(date):
    if isinstance(date, datetime.date):
        return date.strftime('%d-%b-%Y')
    return date


def build_search_query(**kwargs):

    # Parse keyword arguments
    unread = kwargs.get('unread', False)
    unflagged = kwargs.get('unflagged', False)
    flagged = kwargs.get('flagged', False)
    sent_from = kwargs.get('sent_from', False)
    sent_to = kwargs.get('sent_to', False)
    date__gt = kwargs.get('date__gt', False)
    date__lt = kwargs.get('date__lt', False)
    date__on = kwargs.get('date__on', False)
    subject = kwargs.get('subject')

    query = []

    if unread:
        query.append("(UNSEEN)")

    if unflagged:
        query.append("(UNFLAGGED)")

    if flagged:
        query.append("(FLAGGED)")

    if sent_from:
        query.append('(FROM "%s")' % sent_from)

    if sent_to:
        query.append('(TO "%s")' % sent_to)

    if date__gt:
        query.append('(SINCE "%s")' % format_date(date__gt))

    if date__lt:
        query.append('(BEFORE "%s")' % format_date(date__lt))
    
    if date__on:
        query.append('(ON "%s")' % format_date(date__on))

    if subject is not None:
        query.append('(SUBJECT "%s")' % subject)

    if query:
        logger.debug("IMAP query: {}".format(" ".join(query)))
        return " ".join(query)

    logger.debug("IMAP query: {}".format("(ALL)"))
    return "(ALL)"
