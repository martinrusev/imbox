import datetime


def build_search_query(imap_attribute_lookup, **kwargs):
    query = []
    for name, value in kwargs.items():
        if value is not None:
            if isinstance(value, datetime.date):
                value = value.strftime('%d-%b-%Y')
            if isinstance(value, str) and '"' in value:
                value = value.replace('"', "'")
            query.append(imap_attribute_lookup[name].format(value))

    if query:
        return " ".join(query)

    return "(ALL)"
