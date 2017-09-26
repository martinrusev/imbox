# Encoding: utf-8
from __future__ import unicode_literals
import unittest
from imbox.parser import *

import sys
if sys.version_info.major < 3 or sys.version_info.minor < 3:
    SMTP = False
else:
    from email.policy import SMTP


raw_email = """Delivered-To: johndoe@gmail.com
X-Originating-Email: [martin@amon.cx]
Message-ID: <test0@example.com>
Return-Path: martin@amon.cx
Date: Tue, 30 Jul 2013 15:56:29 +0300
From: Martin Rusev <martin@amon.cx>
MIME-Version: 1.0
To: John Doe <johndoe@gmail.com>
Subject: Test email - no attachment
Content-Type: multipart/alternative;
    boundary="------------080505090108000500080106"
X-OriginalArrivalTime: 30 Jul 2013 12:56:43.0604 (UTC) FILETIME=[3DD52140:01CE8D24]

--------------080505090108000500080106
Content-Type: text/plain; charset="ISO-8859-1"; format=flowed
Content-Transfer-Encoding: 7bit

Hi, this is a test email with no attachments

--------------080505090108000500080106
Content-Type: text/html; charset="ISO-8859-1"
Content-Transfer-Encoding: 7bit

<html><head>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1"></head><body
 bgcolor="#FFFFFF" text="#000000">
Hi, this is a test email with no <span style="font-weight: bold;">attachments</span><br>
</body>
</html>

--------------080505090108000500080106--
"""

raw_email_encoded = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
Date: Sat, 26 Mar 2016 13:55:30 +0300 (FET)
From: sender@example.com
To: receiver@example.com
Message-ID: <811170233.1296.1345983710614.JavaMail.bris@BRIS-AS-NEW.site>
Subject: =?ISO-8859-5?B?suvf2OHa0CDf3iDa0ODi1Q==?=
MIME-Version: 1.0
Content-Type: multipart/mixed; 
	boundary="----=_Part_1295_1644105626.1458989730614"

------=_Part_1295_1644105626.1458989730614
Content-Type: text/html; charset=ISO-8859-5
Content-Transfer-Encoding: quoted-printable

=B2=EB=DF=D8=E1=DA=D0 =DF=DE =DA=D0=E0=E2=D5 1234
------=_Part_1295_1644105626.1458989730614--
"""

raw_email_encoded_needs_refolding = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
Date: Sat, 26 Mar 2016 13:55:30 +0300 (FET)
From: sender@example.com
To: "Receiver" <receiver@example.com>, "Second\r\n Receiver" <recipient@example.com>
Message-ID: <811170233.1296.1345983710614.JavaMail.bris@BRIS-AS-NEW.site>
Subject: =?ISO-8859-5?B?suvf2OHa0CDf3iDa0ODi1Q==?=
MIME-Version: 1.0
Content-Type: multipart/mixed; 
    boundary="----=_Part_1295_1644105626.1458989730614"

------=_Part_1295_1644105626.1458989730614
Content-Type: text/html; charset=ISO-8859-5
Content-Transfer-Encoding: quoted-printable

=B2=EB=DF=D8=E1=DA=D0 =DF=DE =DA=D0=E0=E2=D5 1234
------=_Part_1295_1644105626.1458989730614--
"""


raw_email_encoded_another_bad_multipart = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
Mime-Version: 1.0
Date: Wed, 22 Mar 2017 15:21:55 -0500
Message-ID: <58D29693.192A.0075.1@wimort.com>
Subject: Re: Reaching Out About Peoples Home Equity
From: sender@example.com
To: receiver@example.com
Content-Type: multipart/alternative; boundary="____NOIBTUQXSYRVOOAFLCHY____"


--____NOIBTUQXSYRVOOAFLCHY____
Content-Type: text/plain; charset=iso-8859-15
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline;
	modification-date="Wed, 22 Mar 2017 15:21:55 -0500"

Chloe,
 
--____NOIBTUQXSYRVOOAFLCHY____
Content-Type: multipart/related; boundary="____XTSWHCFJMONXSVGPVDLY____"


--____XTSWHCFJMONXSVGPVDLY____
Content-Type: text/html; charset=iso-8859-15
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline;
	modification-date="Wed, 22 Mar 2017 15:21:55 -0500"

<HTML xmlns=3D"http://www.w3.org/1999/xhtml">
<BODY style=3D"COLOR: black; FONT: 10pt Segoe UI; MARGIN: 4px 4px 1px" =
leftMargin=3D0 topMargin=3D0 offset=3D"0" marginwidth=3D"0" marginheight=3D=
"0">
<DIV>Chloe,</DIV>
<IMG src=3D"cid:VFXVGHA=
GXNMI.36b3148cbf284ba18d35bdd8386ac266" width=3D1 height=3D1> </BODY></HTML=
>
--____XTSWHCFJMONXSVGPVDLY____
Content-ID: <TLUACRGXVUBY.IMAGE_3.gif>
Content-Type: image/gif
Content-Transfer-Encoding: base64

R0lGODlhHgHCAPf/AIOPr9GvT7SFcZZjVTEuMLS1tZKUlJN0Znp4eEA7PV1aWvz8+8V6Zl1BNYxX
HvOZ1/zmOd95agUEADs=
--____XTSWHCFJMONXSVGPVDLY____
Content-ID: <VFXVGHAGXNMI.36b3148cbf284ba18d35bdd8386ac266>
Content-Type: image/xxx
Content-Transfer-Encoding: base64

R0lGODlhAQABAPAAAAAAAAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==
--____XTSWHCFJMONXSVGPVDLY____--

--____NOIBTUQXSYRVOOAFLCHY____--
"""


class TestParser(unittest.TestCase):

    def test_parse_email(self):
        parsed_email = parse_email(raw_email)

        self.assertEqual(raw_email, parsed_email.raw_email)
        self.assertEqual('Test email - no attachment', parsed_email.subject)
        self.assertEqual('Tue, 30 Jul 2013 15:56:29 +0300', parsed_email.date)
        self.assertEqual('<test0@example.com>', parsed_email.message_id)

    def test_parse_email_encoded(self):
        parsed_email = parse_email(raw_email_encoded)

        self.assertEqual('Выписка по карте', parsed_email.subject)
        self.assertEqual('Выписка по карте 1234', parsed_email.body['html'][0])

    def test_parse_email_inline_body(self):
        parsed_email = parse_email(raw_email_encoded_another_bad_multipart)
        self.assertEqual("Re: Reaching Out About Peoples Home Equity", parsed_email.subject)
        self.assertTrue(parsed_email.body['plain'])
        self.assertTrue(parsed_email.body['html'])

    def test_parse_email_ignores_header_casing(self):
        self.assertEqual('one', parse_email('Message-ID: one').message_id)
        self.assertEqual('one', parse_email('Message-Id: one').message_id)
        self.assertEqual('one', parse_email('Message-id: one').message_id)
        self.assertEqual('one', parse_email('message-id: one').message_id)

    # TODO - Complete the test suite
    def test_parse_attachment(self):
        pass

    def test_decode_mail_header(self):
        pass

    def test_get_mail_addresses(self):

        to_message_object = email.message_from_string("To: John Doe <johndoe@gmail.com>")
        self.assertEqual([{'email': 'johndoe@gmail.com', 'name': 'John Doe'}], get_mail_addresses(to_message_object, 'to'))

        from_message_object = email.message_from_string("From: John Smith <johnsmith@gmail.com>")
        self.assertEqual([{'email': 'johnsmith@gmail.com', 'name': 'John Smith'}], get_mail_addresses(from_message_object, 'from'))

    def test_parse_email_with_policy(self):
        if not SMTP:
            return

        message_object = email.message_from_bytes(
            raw_email_encoded_needs_refolding,
            policy=SMTP.clone(refold_source='all')
        )

        self.assertEqual([
            {'email': 'receiver@example.com', 'name': 'Receiver'},
            {'email': 'recipient@example.com', 'name': 'Second Receiver'}
        ], get_mail_addresses(message_object, 'to'))
