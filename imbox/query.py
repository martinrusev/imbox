# TODO - Validate query arguments
import datetime


def format_date(date):
    if isinstance(date, datetime.date):
        return date.strftime('%d-%b-%Y')
    else:
        return date


def build_search_query(**kwargs):
    #TODO implement OR

    # Parse keyword arguments
    unread = kwargs.get('unread', False)
    sent_from = kwargs.get('sent_from', False)
    sent_to = kwargs.get('sent_to', False)
    date__gt = kwargs.get('date__gt', False)
    date__lt = kwargs.get('date__lt', False)
    date_on = kwargs.get('date_on', False)

    query = "(ALL)"

    if unread:
        query = "(UNSEEN)"

    if sent_from:
        query = '{0} (FROM "{1}")'.format(query, sent_from)

    if sent_to:
        query = '{0} (TO "{1}")'.format(query, sent_to)

    if date__gt:
        query = '{0} (SINCE "{1}")'.format(query, format_date(date__gt))

    if date__lt:
        query = '{0} (BEFORE "{1}")'.format(query, format_date(date__lt))

    if date_on:
        query = '{0} (ON "{1}")'.format(query, format_date(date_on))

    return query
