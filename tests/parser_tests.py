import unittest
from imbox.parser import *

import os
import sys
if sys.version_info.minor < 3:
    SMTP = False
else:
    from email.policy import SMTP


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


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


raw_email_encoded_multipart = b"""Delivered-To: receiver@example.com
Return-Path: <kkoudelka@wallvet.com>
Date: Tue, 08 Aug 2017 08:15:11 -0700
From: <kkoudelka@wallvet.com>
To: interviews+347243@gethappie.me
Message-Id: <20170808081511.2b876c018dd94666bcc18e28cf079afb.99766f164b.wbe@email24.godaddy.com>
Subject: RE: Kari, are you open to this?
Mime-Version: 1.0
Content-Type: multipart/related;
	boundary="=_7c18e0b95b772890a22ed6c0f810a434"

--=_7c18e0b95b772890a22ed6c0f810a434
Content-Transfer-Encoding: quoted-printable
Content-Type: text/html; charset="utf-8"

<html><body><span style=3D"font-family:Verdana; color:#000; font-size:10pt;=
"><div>Hi Richie,</div></span></body></html>
--=_7c18e0b95b772890a22ed6c0f810a434
Content-Transfer-Encoding: base64
Content-Type: image/jpeg; charset=binary;
 name="sigimg0"; 
Content-Disposition: inline;
 filename="sigimg0"; 

/9j/4AAQSkZJRgABAQAAAQABAAD//gA+Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcg
jt0JaKhjm3xq23GR60UuZBZn/9k=
--=_7c18e0b95b772890a22ed6c0f810a434
Content-Transfer-Encoding: base64
Content-Type: image/jpeg; charset=binary;
 name="sigimg1"; 
Content-Disposition: inline;
 filename="sigimg1"; 

/9j/4AAQSkZJRgABAQAAAQABAAD//gA+Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcg
SlBFRyB2NjIpLCBkZWZhdWx0IHF1YWxpdHkK/9sAQwAIBgYHBgUIBwcHCQkICgwUDQwLCwwZEhMP
ooooA//Z
--=_7c18e0b95b772890a22ed6c0f810a434--

"""


raw_email_encoded_bad_multipart = b"""Delivered-To: receiver@example.com
Return-Path: <sender@example.com>
From: sender@example.com
To: "Receiver" <receiver@example.com>, "Second\r\n Receiver" <recipient@example.com>
Subject: Re: Looking to connect with you...
Date: Thu, 20 Apr 2017 15:32:52 +0000
Message-ID: <BN6PR16MB179579288933D60C4016D078C31B0@BN6PR16MB1795.namprd16.prod.outlook.com>
Content-Type: multipart/related;
	boundary="_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_";
	type="multipart/alternative"
MIME-Version: 1.0
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: multipart/alternative;
	boundary="_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_"
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64
SGkgRGFuaWVsbGUsDQoNCg0KSSBhY3R1YWxseSBhbSBoYXBweSBpbiBteSBjdXJyZW50IHJvbGUs
Y3J1aXRlciB8IENoYXJsb3R0ZSwgTkMNClNlbnQgdmlhIEhhcHBpZQ0KDQoNCg==
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: base64
PGh0bWw+DQo8aGVhZD4NCjxtZXRhIGh0dHAtZXF1aXY9IkNvbnRlbnQtVHlwZSIgY29udGVudD0i
CjwvZGl2Pg0KPC9kaXY+DQo8L2JvZHk+DQo8L2h0bWw+DQo=
--_000_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_--
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_
Content-Type: image/png; name="=?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?="
Content-Description: =?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?=
Content-Disposition: inline;
	filename="=?utf-8?B?T3V0bG9va0Vtb2ppLfCfmIoucG5n?="; size=488;
	creation-date="Thu, 20 Apr 2017 15:32:52 GMT";
	modification-date="Thu, 20 Apr 2017 15:32:52 GMT"
Content-ID: <254962e2-f05c-40d1-aa11-0d34671b056c>
Content-Transfer-Encoding: base64
iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJ
cvED9AIR3TCAAAMAqh+p+YMVeBQAAAAASUVORK5CYII=
--_004_BN6PR16MB179579288933D60C4016D078C31B0BN6PR16MB1795namp_--
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


raw_email_with_trailing_semicolon_to_disposition_content = b"""Delivered-To: receiver@example.com
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

Hello Chloe

--____NOIBTUQXSYRVOOAFLCHY____
Content-Type: multipart/related; boundary="____XTSWHCFJMONXSVGPVDLY____"


--____XTSWHCFJMONXSVGPVDLY____
Content-Type: text/html; charset=iso-8859-15
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline;
	modification-date="Wed, 22 Mar 2017 15:21:55 -0500"

<HTML xmlns=3D"http://www.w3.org/1999/xhtml">
<BODY>
<DIV>Hello Chloe</DIV>
</BODY>
</HTML>
--____XTSWHCFJMONXSVGPVDLY____
Content-Type: application/octet-stream; name="abc.xyz"
Content-Description: abc.xyz
Content-Disposition: attachment; filename="abc.xyz";
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

raw_email_with_long_filename_attachment = b"""Delivered-To: receiver@example.com
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

Hello Chloe

--____NOIBTUQXSYRVOOAFLCHY____
Content-Type: multipart/related; boundary="____XTSWHCFJMONXSVGPVDLY____"


--____XTSWHCFJMONXSVGPVDLY____
Content-Type: text/html; charset=iso-8859-15
Content-Transfer-Encoding: quoted-printable
Content-Disposition: inline;
	modification-date="Wed, 22 Mar 2017 15:21:55 -0500"

<HTML xmlns=3D"http://www.w3.org/1999/xhtml">
<BODY>
<DIV>Hello Chloe</DIV>
</BODY>
</HTML>
--____XTSWHCFJMONXSVGPVDLY____
Content-Type: application/octet-stream; name="abc.xyz"
Content-Description: abcefghijklmnopqrstuvwxyz01234567890abcefghijklmnopqrstuvwxyz01234567890abcefghijklmnopqrstuvwxyz01234567890.xyz
Content-Disposition: attachment; filename*0="abcefghijklmnopqrstuvwxyz01234567890abcefghijklmnopqrstuvwxyz01234567890abce"; filename*1="fghijklmnopqrstuvwxyz01234567890.xyz";
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

raw_email_encoded_encoding_charset_contains_a_minus = b"""Delivered-To: <receiver@example.org>
Return-Path: <sender@example.org>
Message-ID: <74836CF6FF9B1965927DE7EE8A087483@NXOFGRQFQW2>
From: <sender@example.org>
To: <sender@example.org>
Subject: Salut, mon cher.
Date: 30 May 2018 22:47:37 +0200
MIME-Version: 1.0
Content-Type: multipart/alternative;
	boundary="----=_NextPart_000_0038_01D3F85C.02934C4A"

------=_NextPart_000_0038_01D3F85C.02934C4A
Content-Type: text/plain;
	charset="cp-850"
Content-Transfer-Encoding: quoted-printable

spam here


cliquez ici
------=_NextPart_000_0038_01D3F85C.02934C4A
Content-Type: text/html;
	charset="cp-850"
Content-Transfer-Encoding: quoted-printable

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML><HEAD>
<META http-equiv=3DContent-Type content=3D"text/html; charset=3Dcp-850">
<META content=3D"MSHTML 6.00.2900.2456" name=3DGENERATOR>
<STYLE></STYLE>
</HEAD>
<BODY bgColor=3D#ffffff>
spam here<br>
<br>
<a href=3D"http://spammer-url"><b>cliquez =
ici</b></a></br></BODY></HTML>
------=_NextPart_000_0038_01D3F85C.02934C4A--
"""

raw_email_attachment_only = """Delivered-To: johndoe@gmail.com
X-Originating-Email: [martin@amon.cx]
Message-ID: <test1@example.com>
Return-Path: martin@amon.cx
Date: Tue, 30 Jul 2013 15:56:29 +0300
From: Martin Rusev <martin@amon.cx>
MIME-Version: 1.0
To: John Doe <johndoe@gmail.com>
Subject: Test email - only pdf in body
Content-Type: application/pdf;
	name="=?utf-8?B?YV9sb25nX2ZpbGVuYW1lX3dpdGhfc3BlY2lhbF9jaGFyX8O2w6Rf?=
	=?utf-8?B?LTAxX28ucGRm?="
Content-Transfer-Encoding: base64
Content-Disposition: attachment;
	filename="=?utf-8?B?YV9sb25nX2ZpbGVuYW1lX3dpdGhfc3BlY2lhbF9jaGFyX8O2w6Rf?=
	=?utf-8?B?LTAxX28ucGRm?="

JVBERi0xLjQKJcOiw6PDj8OTCjUgMCBvYmoKPDwKL0xlbmd0aCAxCj4+CnN0cmVhbQogCmVuZHN0
cmVhbQplbmRvYmoKNCAwIG9iago8PAovVHlwZSAvUGFnZQovTWVkaWFCb3ggWzAgMCA2MTIgNzky
XQovUmVzb3VyY2VzIDw8Cj4+Ci9Db250ZW50cyA1IDAgUgovUGFyZW50IDIgMCBSCj4+CmVuZG9i
agoyIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovS2lkcyBbNCAwIFJdCi9Db3VudCAxCj4+CmVuZG9i
agoxIDAgb2JqCjw8Ci9UeXBlIC9DYXRhbG9nCi9QYWdlcyAyIDAgUgo+PgplbmRvYmoKMyAwIG9i
ago8PAovQ3JlYXRvciAoUERGIENyZWF0b3IgaHR0cDovL3d3dy5wZGYtdG9vbHMuY29tKQovQ3Jl
YXRpb25EYXRlIChEOjIwMTUwNzAxMTEyNDQ3KzAyJzAwJykKL01vZERhdGUgKEQ6MjAyMjA2MDcx
ODM2MDIrMDInMDAnKQovUHJvZHVjZXIgKDMtSGVpZ2h0c1wyMjIgUERGIE9wdGltaXphdGlvbiBT
aGVsbCA2LjAuMC4wIFwoaHR0cDovL3d3dy5wZGYtdG9vbHMuY29tXCkpCj4+CmVuZG9iagp4cmVm
CjAgNgowMDAwMDAwMDAwIDY1NTM1IGYKMDAwMDAwMDIyNiAwMDAwMCBuCjAwMDAwMDAxNjkgMDAw
MDAgbgowMDAwMDAwMjc1IDAwMDAwIG4KMDAwMDAwMDA2NSAwMDAwMCBuCjAwMDAwMDAwMTUgMDAw
MDAgbgp0cmFpbGVyCjw8Ci9TaXplIDYKL1Jvb3QgMSAwIFIKL0luZm8gMyAwIFIKL0lEIFs8MUMz
NTAwQ0E5RjcyMzJCOTdFMEVGM0Y3ODlFOEI3RjI+IDwyNTRDOEQxNTNGNjU1RDQ5OTQ1RUFENjhE
ODAxRTAxMT5dCj4+CnN0YXJ0eHJlZgo1MDUKJSVFT0Y=
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

    def test_parse_email_invalid_unicode(self):
        parsed_email = parse_email(open(os.path.join(TEST_DIR, '8422.msg'), 'rb').read())
        self.assertEqual("Following up Re: Looking to connect, let's schedule a call!", parsed_email.subject)

    def test_parse_email_inline_body(self):
        parsed_email = parse_email(raw_email_encoded_another_bad_multipart)
        self.assertEqual("Re: Reaching Out About Peoples Home Equity", parsed_email.subject)
        self.assertTrue(parsed_email.body['plain'])
        self.assertTrue(parsed_email.body['html'])

    def test_parse_email_multipart(self):
        parsed_email = parse_email(raw_email_encoded_multipart)
        self.assertEqual("RE: Kari, are you open to this?", parsed_email.subject)

    def test_parse_email_bad_multipart(self):
        parsed_email = parse_email(raw_email_encoded_bad_multipart)
        self.assertEqual("Re: Looking to connect with you...", parsed_email.subject)

    def test_parse_email_ignores_header_casing(self):
        self.assertEqual('one', parse_email('Message-ID: one').message_id)
        self.assertEqual('one', parse_email('Message-Id: one').message_id)
        self.assertEqual('one', parse_email('Message-id: one').message_id)
        self.assertEqual('one', parse_email('message-id: one').message_id)

    def test_parse_attachment(self):
        parsed_email = parse_email(raw_email_with_trailing_semicolon_to_disposition_content)
        self.assertEqual(1, len(parsed_email.attachments))
        attachment = parsed_email.attachments[0]
        self.assertEqual('application/octet-stream', attachment['content-type'])
        self.assertEqual(71, attachment['size'])
        self.assertEqual('abc.xyz', attachment['filename'])
        self.assertTrue(attachment['content'])

    def test_parse_attachment_with_long_filename(self):
        parsed_email = parse_email(raw_email_with_long_filename_attachment)
        self.assertEqual(1, len(parsed_email.attachments))
        attachment = parsed_email.attachments[0]
        self.assertEqual('application/octet-stream', attachment['content-type'])
        self.assertEqual(71, attachment['size'])
        self.assertEqual('abcefghijklmnopqrstuvwxyz01234567890abcefghijklmnopqrstuvwxyz01234567890abcefghijklmnopqrstuvwxyz01234567890.xyz', attachment['filename'])
        self.assertTrue(attachment['content'])
    
    def test_parse_email_single_attachment(self):
        parsed_email = parse_email(raw_email_attachment_only)
        self.assertEqual(1, len(parsed_email.attachments))
        attachment = parsed_email.attachments[0]
        self.assertEqual('application/pdf', attachment['content-type'])
        self.assertEqual(773, attachment['size'])
        self.assertEqual('a_long_filename_with_special_char_öä_-01_o.pdf', attachment['filename'])
        self.assertTrue(attachment['content'])

    def test_parse_email_accept_if_declared_charset_contains_a_minus_character(self):
        parsed_email = parse_email(raw_email_encoded_encoding_charset_contains_a_minus)
        self.assertEqual("Salut, mon cher.", parsed_email.subject)
        self.assertTrue(parsed_email.body['plain'])
        self.assertTrue(parsed_email.body['html'])

    # TODO - Complete the test suite
    def test_decode_mail_header(self):
        pass

    def test_get_mail_addresses(self):

        to_message_object = email.message_from_string("To: John Doe <johndoe@gmail.com>")
        self.assertEqual([{'email': 'johndoe@gmail.com', 'name': 'John Doe'}], get_mail_addresses(to_message_object, 'to'))

        from_message_object = email.message_from_string("From: John Smith <johnsmith@gmail.com>")
        self.assertEqual([{'email': 'johnsmith@gmail.com', 'name': 'John Smith'}], get_mail_addresses(from_message_object, 'from'))

        invalid_encoding_in_from_message_object = email.message_from_string("From: =?UTF-8?Q?C=E4cilia?= <caciliahxg827m@example.org>")
        self.assertEqual([{'email': 'caciliahxg827m@example.org', 'name': 'C�cilia'}], get_mail_addresses(invalid_encoding_in_from_message_object, 'from'))

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
