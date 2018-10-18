from imbox.messages import Messages
from imbox.vendors.helpers import merge_two_dicts


class GmailMessages(Messages):
    authentication_error_message = ('If you\'re not using an app-specific password, grab one here: '
                                    'https://myaccount.google.com/apppasswords')
    hostname = 'imap.gmail.com'
    name = 'gmail'
    FOLDER_LOOKUP = {

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

    GMAIL_IMAP_ATTRIBUTE_LOOKUP_DIFF = {
        'subject': '(X-GM-RAW "subject:\'{}\'")',
        'label': '(X-GM-LABELS "{}")',
        'raw': '(X-GM-RAW "{}")'
    }

    def __init__(self,
                 connection,
                 parser_policy,
                 **kwargs):

        self.IMAP_ATTRIBUTE_LOOKUP = merge_two_dicts(self.IMAP_ATTRIBUTE_LOOKUP,
                                                     self.GMAIL_IMAP_ATTRIBUTE_LOOKUP_DIFF)

        super().__init__(connection, parser_policy, **kwargs)
