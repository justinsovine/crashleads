#!/usr/bin/env python

import sys
import smtplib
import time
import datetime
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mandrill

class Notify(object):
	"""Notifies recipients of new police reports"""

	def __init__(self, db, server):
		"""Initialization"""

		self.db = db
		self.server = server

	def fetchEmails(self):
		"""Fetches all recipients' email addresses"""

		self.emails = self.db.conn.cursor()
		self.emails.execute("SELECT fname, lname, data FROM notify_list WHERE type = 'email' AND active = 1")
		results = []
		for fname, lname, data in self.emails.fetchall():
			#results.append(fname + " " + lname + " <" + data + ">")
			results.append(data)

		
		self.emailList = results

	def fetchSMS(self):
		"""Fetches all recipients SMS addresses"""

		self.sms = self.db.conn.cursor()
		self.sms.execute("SELECT fname, lname, data FROM notify_list WHERE  type = 'sms' AND active = 1")
		results = []
		for fname, lname, data in self.sms.fetchall():
			#results.append(fname + " " + lname + " <" + data + ">")
			results.append(data)
		
		self.smsList = results

	def compileRecipients(self):
		"""Merges email and sms lists"""

		self.contactList = []
		if self.emailList is not None:
			for contact in self.emailList:
				self.contactList.append(contact)

		if self.smsList is not None:
			for contact in self.smsList:
				self.contactList.append(contact)

	def constructEmailBody(self, reports, runTime):
		"""Construct email body"""

		text  = "Please send any technical questions or concerns to Justin Sovine at jsovine@smagno.com\n\n"

		html = """\
		<html>
		  <head></head>
		  <body>
			<div style='font-family: arial, helvetica, sans-serif; font-size: 12px;'>
				<ul>
		"""

		pageVar = ""
		for key in sorted(reports.iterkeys()):
			for link in reports[key]:

				# First entry
				if pageVar == "":
					pageVar = key
					html += "</ul>"
					# Page stayed the same, new report
					html += "<p><strong>Reports from: " + pageVar + "</strong></p>\n"
					text += "Reports from: " + pageVar + "\n\n"
					html += "<ul>"
					text += link + "\n\n"        
					html += "<li style='margin-bottom: 10px;'><a href='" + link + "'>" + link + "</a></li>\n"
				
				# Page just changed
				elif pageVar != key:
					pageVar = key
					html += "</ul>"
					# Page stayed the same, new report
					html += "<p><strong>Reports from: " + pageVar + "</strong></p>\n"
					text += "Reports from: " + pageVar + "\n\n"
					html += "<ul>"
					text += link + "\n\n"        
					html += "<li style='margin-bottom: 10px;'><a href='" + link + "'>" + link + "</a></li>\n"
				else:
					# Page stayed the same, new report
					text += link + "\n\n"        
					html += "<li style='margin-bottom: 10px;'><a href='" + link + "'>" + link + "</a></li>\n"

			html += "</ul>"

		text += "This content was generated in " + str(runTime)

		html += "<p>&mdash;</p>"
		html += "<p><em><strong>This content was generated in " + str(runTime) + "</strong></em></p>"
		html += "<p><em>Please send any technical questions or concerns to <a href='mailto:jsovine@smagno.com'>Justin Sovine &lt;jsovine@smagno.com&gt;</a>, Developer & Administrator</em></p>"

		html += """
			</div>
		  </body>
		</html>
		"""

		return text, html

	def sendNotifications(self, reports, text, html):
		"""Sends notification emails to all recipients"""

		today = datetime.datetime.today()

		# Create date list\
		s = string.split(str(today), " ")
		date = s[0]
		time = s[1]
		s = string.split(time, ".")
		time = s[0]
		dateStamp = date + " @ " + time

		emailFrom = "GrabReports <grabreports@intellect37.com>"
		emailTo = self.contactList

		keyStore = ""
		keyList = []
		for key in reports.keys():
			if keyStore == "":
				keyStore = key
				keyList.append(key)
			elif keyStore != key:
				keyList.append(key)

		countyStr = ",".join(keyList)

		subject = "New reports from " + countyStr + " #" + dateStamp

		COMMASPACE = ', '
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = emailFrom
		msg['To'] = COMMASPACE.join(emailTo)

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')

		msg.attach(part1)
		msg.attach(part2)

		try:
			mandrill_client = mandrill.Mandrill('3N0wkizXJLE66DE2c33WPQ')
			message = {
				'from_email': 'grabreports@smagno.com',
				'from_name': 'Grab Reports',
				'headers': {'Reply-To': 'grabreports@intellect37.com'},
				'text': text,
				'html': html,
				'to': [{"email":contact} for contact in self.emailList],
				'subject': subject,
				'track_clicks': True,
				'track_opens': True,
				'url_strip_qs': None
			}
			result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')

		except mandrill.Error, e:
			# Mandrill errors are thrown as exceptions
			print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
			# A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
			raise
		
		"""
		try:
			s = smtplib.SMTP('localhost')
			s.sendmail(emailFrom, emailTo, msg.as_string())
			s.quit()
			return 0 # Success

		except:
			print sys.exc_info()
			return 1 # Failure
		"""
		
	def execute(self, reports, scriptStart):
		"""Executive function"""

		self.fetchEmails()
		self.fetchSMS()
		self.compileRecipients()

		scriptEnd = datetime.datetime.now()
		runTime = scriptEnd - scriptStart

		text, html = self.constructEmailBody(reports, runTime)
		status = self.sendNotifications(reports, text, html)
		
		if status == None:
			print 'Success!'
		else:
			print 'Failed!'

