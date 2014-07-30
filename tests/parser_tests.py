import unittest
import email
from imbox.parser import *

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

class TestParser(unittest.TestCase):


	
	def test_parse_email(self):
		parsed_email = parse_email(raw_email)

		self.assertEqual(u'Test email - no attachment', parsed_email.subject)
		self.assertEqual(u'Tue, 30 Jul 2013 15:56:29 +0300', parsed_email.date)
		self.assertEqual(u'<test0@example.com>', parsed_email.message_id)


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
		self.assertEqual([{'email': 'johndoe@gmail.com', 'name': u'John Doe'}], get_mail_addresses(to_message_object, 'to'))

		from_message_object = email.message_from_string("From: John Smith <johnsmith@gmail.com>")
		self.assertEqual([{'email': 'johnsmith@gmail.com', 'name': u'John Smith'}], get_mail_addresses(from_message_object, 'from'))

