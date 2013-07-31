def build_search_query(**kwargs):

	# Parse keyword arguments 
	unread = kwargs.get('unread', False)
	sent_from = kwargs.get('sent_from', False)
	sent_to = kwargs.get('sent_to', False)

	query = "(ALL)"

	if unread != False:
		query = "(UNSEEN)"

	if sent_from:
		query = '{0} (FROM "{1}")'.format(query, sent_from)

	if sent_to:
		query = '{0} (TO "{1}")'.format(query, sent_to)


	return str(query)