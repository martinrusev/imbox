from imbox.vendors.gmail import GmailMessages


hostname_vendorname_dict = {GmailMessages.hostname: GmailMessages.name}

__all__ = ['GmailMessages',
           'hostname_vendorname_dict']