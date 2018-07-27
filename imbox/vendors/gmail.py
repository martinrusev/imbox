from imbox.messages import Messages


class GmailMessages(Messages):
    authentication_error_message = ('If you\'re not using an app-specific password, grab one here: '
                                    'https://myaccount.google.com/apppasswords')
    hostname = 'imap.gmail.com'
    name = 'gmail'
    folder_lookup = {

        'all_mail': '"[Gmail]/All Mail"',
        'all': '"[Gmail]/All Mail"',
        'all mail': '"[Gmail]/All Mail"',
        'sent': '"[Gmail]/Sent Mail"',
        'sent mail': '"[Gmail]/Sent Mail"',
        'sent_mail': '"[Gmail]/Sent Mail"',
        'drafts': '"[Gmail]/Drafts"',
        'important': '"[Gmail]/Important"',
        'spam': '"[Gmail]/Spam"',
        'starred': '"[Gmail]/Starred"',
        'trash': '"[Gmail]/Trash"',

    }

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):
        super().__init__(connection, parser_policy, **kwargs)
