#!/usr/bin/env python

import sys
import re
import time
import datetime
import string
import MySQLdb
import ftputil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from bs4 import BeautifulSoup

from modules import download

class Search(object):
	"""Searches target sources for new police reports"""

	def __init__(self, driver, db):
		"""Initialization"""
		self.driver = driver
		self.db = db
		self.numDays = 30 # 1 month

	def check_franklinohio_org(self, target):
		"""Searches ftp.masonoh.org"""

		reports = []
		names = []
		d = download.Download()

		self.driver.get(target)

		print "Getting soup data"
		soup = BeautifulSoup(unicode(self.driver.page_source))

		for a in soup.findAll('a'):
			link = str(a['href'])
			try:
				if link.index('.pdf'):
					link = "http://franklinohio.org" + link
					arr = link.split('/')
					name = arr[-1]

					c = self.db.conn.cursor()
					c.execute("SELECT name FROM franklinohio_org WHERE name = %s", name)

					# Check if report already exists
					if not c.fetchone():
						# Download file
						results = d.single_franklinohio_org(link, name)
						if results != "":
							c = self.db.conn.cursor()
							c.execute("INSERT INTO franklinohio_org (name, link) VALUES (%s, %s)", [name, results])
							reports.append(results)
						else:
							print "There was a problem downloading a file from FTP"
			except:
				print "Not pdf"

		if len(reports) > 0:
			return reports
		else:
			return ""

	def check_mason_ftp(self, link):
		"""Searches ftp.masonoh.org"""

		links = []

		d = download.Download()

		# Connect and enter crash reports directory
		host = ftputil.FTPHost(link, 'anonymous', '')
		try:
			host.chdir('public download/mpd traffic crash reports/')
		except:
			print "The file structure has changed"

		# Iterate through folders
		folders = host.listdir(host.curdir)
		for folder in folders:
			statarr = host.stat(folder)
			# statarr[8] = date modified unix timestamp
			dmod = str(datetime.datetime.fromtimestamp(int(statarr[8])).strftime('%Y-%m-%d %H:%M:%S'))

			# Query date modified
			c = self.db.conn.cursor()
			c.execute("SELECT last_update FROM main_ftp_masonoh_org WHERE folder = %s", folder)
			for data in c.fetchone():
				storedDate = data

			# Folder is new
			if not storedDate:
				c = self.db.conn.cursor()
				c.execute("INSERT INTO main_ftp_masonoh_org (folder) VALUES (%s)", folder)
				storedDate = ""

			# Folder has new files
			if not storedDate == dmod:
				# Update datemodified
				c = self.db.conn.cursor()
				c.execute("UPDATE main_ftp_masonoh_org SET last_update = %s WHERE folder = %s", [dmod, folder])

				# Enter folder
				print "Entering %s" % folder
				host.chdir(folder)
				files = host.listdir(host.curdir)
				
				# Iterate through files
				for file in files:
					if host.path.isfile(file):

						c = self.db.conn.cursor()
						c.execute("SELECT name FROM reports_ftp_masonoh_org WHERE name = %s", file)

						# Check if report already exists
						if not c.fetchone():
							# Download file
							results = d.single_mason_ftp(host, file, folder)
							if results != "":
								links.append(results)
								c = self.db.conn.cursor()
								c.execute("INSERT INTO reports_ftp_masonoh_org (name, link) VALUES (%s, %s)", [file, results])
							else:
								print "There was a problem downloading a file from FTP"

					else:
						print "There was a folder when a file was expected"

				print "Exiting %s" % folder
				host.chdir("../")

		if len(links) > 0:
			return links
		else:
			return ""

	def check_police_reports_us(self, target, county):
		"""Searches http://policereports.us"""

		# Load target website
		try:
			print "Loading target ", target
			self.driver.get(target)

		except:
			print "Failed to load target"

		# Find "Last Report Upload at" string in <center></center>
		try:
			print "Parsing target for last update string"
			soup = BeautifulSoup(self.driver.page_source)
			wwwLastUpdate = soup.findAll('center') # Possibly volatile

		except:
			print "Failed to find last update string"


		# Detects if they've used more than one <center></center> and uses the right one
		try:
			print "Detecting if more than one <center></center>"
			if len(wwwLastUpdate) > 1:
				print "wwwLastUpdate length = ", len(wwwLastUpdate)
				for data in wwwLastUpdate:
					data = unicode(data)

					try:
						if data.index("Last Report Upload at "):
							wwwSoup = BeautifulSoup(data)
							wwwLastUpdate = wwwSoup.find(text=True)
							wwwLastUpdate = wwwLastUpdate.replace("Last Report Upload at ", "")
							print "\nPage was last updated on " + str(wwwLastUpdate) + "\n"
						else:
							print "There was an issue finding the string"
							print unicode(data)

					except ValueError:
						variable = True
						#print "Correct string not selected, moving to next"

			else:
				wwwLastUpdate = unicode(wwwLastUpdate[0])
				wwwSoup = BeautifulSoup(wwwLastUpdate)
				wwwLastUpdate = wwwSoup.find(text=True)
				wwwLastUpdate = wwwLastUpdate.replace("Last Report Upload at ", "")

				print "\nPage was last updated on " + str(wwwLastUpdate) + "\n"

		except:
			print "Failed while detecting duplicate tags"
			print sys.exc_info()

		# Search for last stored update
		c = self.db.conn.cursor()
		c.execute("SELECT last_update FROM site_list WHERE link = %s", target)
		dbLastUpdate = c.fetchone()

		# Compares local and remote update records
		if wwwLastUpdate != dbLastUpdate[0]:
			# New reports are available
			updateResults = self.scan_police_reports_us(target, county)
			c.execute("UPDATE site_list SET last_update = %s WHERE link = %s", [wwwLastUpdate, target])
			return updateResults
		else:
			print "This is legitimately up-to-date"
			return ""

	def scan_police_reports_us(self, target, county):
		"""Performs a full 30 day scan on target"""

		print "Performing a full 30 day scan on ", target
		# Calculate date range
		numDays = 30
		today = datetime.datetime.today()
		dateTimeList = [ today - datetime.timedelta(days=x) for x in range(0, numDays) ]
		dateRange = []

		# Create date list
		for dateTime in dateTimeList:
			s = string.split(str(dateTime), " ")
			date = s[0]
			dateRange.append(date)

		print "Preparing old reports for comparison"
		# Prepare list of old reports
		c = self.db.conn.cursor()
		c.execute("SELECT report_id, link FROM police_reports_us ORDER BY report_id ASC")
		oldReports = {}
		for report_id, link in c.fetchall():
			oldReports[str(report_id)] = str(link)

		newReports = dict()
		print "Iterating through daterange"

		d = download.Download()

		for date in dateRange:
			# Prepare date
			dateArr = string.split(date, "-")
			year = dateArr[0]
			year = year[2:] # Crops first two digits
			month = dateArr[1]
			day = dateArr[2]
			date = month + "/" + day + "/" + year

			# Do search
			print "Submitting search for ", date
			self.driver.execute_script("$('input#mDate').val('" + date + "')")
			self.driver.execute_script("$('#searchform').submit()")

			try:
				# Wait for the search results to appear
				#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
				WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.PARTIAL_LINK_TEXT, "<< Go Back"))

			except:
				print "Browser Timed Out!"
				#print sys.exc_info()

			#print "Grabbing SID"
			# Grab sid for links
			sid = re.search( "sid=[a-z0-9]*", self.driver.page_source)
			sid = sid.group(0) # Grabs the first instance

			#print "Parsing all search results"
			# Check for new reports
			soup = BeautifulSoup(unicode(self.driver.page_source))
			rid = 0

			#links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "View Online PDF")

			for row in soup.find_all("tr", { "class" : "searchresult"}):
				col = row.find_all("td")
				if len(col) == 4:
					# Store data for mass computation
					# Report Number, Report Date, Driver, Location, sid, rid
					#newReports.append(col[0] + " ### " + col[1] + " ### " + col[2] + " ### " + col[3] + " ### " + sid + " ### " + str(rid))
					
					#columnString = unicode(col[0]) + "***" + unicode(col[1]) + "***" + unicode(col[2]) + "***" + unicode(col[3])

					# Forget about everything, just make report checking work
					columnString = unicode(col[0])
					reportNumber = BeautifulSoup(columnString)
					reportNumber = reportNumber.find(text=True)
					reportNumber = str(reportNumber)

					# Check if new or old report
					if not reportNumber in oldReports.keys():
						# New report
						#print "New report => " + reportNumber
						link = d.single_police_reports_us(target, reportNumber, sid, rid, date)
						#print "Link => " + link
						if link > "":
							# Report was downloaded
							newReports[str(reportNumber)] = str(link)
					#print newReports
					#print newReports.get(col[0])
					#newReports = sorted(newReports, key=lambda new_report: new_report[0])
					#print "\n\n\n Report Number => " + tdSoup + "\n SID => " + str(rid) + "\n\n\n"
					rid = int(rid) + 1

		print "All pages have been scanned"
		print "Comparing results"
		# All reports have been scanned, compare results

		newReportsSet = set(newReports)
		oldReportsSet = set(oldReports)    
		diff = [ a for a in newReports.keys() if a not in oldReports.keys() ]
		
		print "Finished comparing results\n\n"
		
		if len(diff) > 0:
			diffList = []
			for key in diff:
				link = newReports[key]
				c.execute("INSERT INTO police_reports_us (report_id, link, location) VALUES (%s, %s, %s)", [key, link, county])
				diffList.append(link)

			return diffList
		else:
			return ""

	def ext_dps_state_oh_us(self, cid, county):
		"""Searches ext.dps.state.oh.us"""

		dateTime = datetime.datetime.today()
		dateTimeArr = string.split(str(dateTime), " ")
		date = dateTimeArr[0]
		dateArr = string.split(str(date), "-")        
		year = dateArr[0]
		month = dateArr[1]
		day = dateArr[2]
		date = month + "/" + day + "/" + year
		#date = "11/28/2012" # Temporary

		target = "https://ext.dps.state.oh.us/CrashRetrieval/OHCrashRetrieval.aspx"

		print "Grabbing old reports"
		c = self.db.conn.cursor()
		c.execute("SELECT report_id, link FROM ext_dps_state_ohio_us ORDER BY report_id ASC")
		newReports = {}
		oldReports = {}
		for report_id, link in c.fetchall():
			oldReports[str(report_id)] = str(link)

		d = download.Download()

		# Load target website
		try:
			print "Loading target " + target
			self.driver.get(target)

		except:
			print "Failed to load target"
			return ""

		# Do search
		print "Submitting search for %s => %s" % (cid, county)
		
		# find the element that's name attribute is q (the google search box)
		inputCounty = Select(self.driver.find_element_by_id("main_cboCounty"))

		print "Selecting county, waiting for __doPostBack()"
		inputCounty.select_by_value(cid)

		try:
			# Wait for the search results to appear
			#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
			WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("Footer"))

		except:
			print "Browser Timed Out!"
			return ""

		print "Getting spoof image value"
		spoof = re.search("rndval=[A-Z0-9]{5}", self.driver.page_source)
		spoof = spoof.group(0)

		spoof = spoof.replace("rndval=", "")

		inputDate = self.driver.find_element_by_id("main_txtCrashAddDate")
		inputSpoof = self.driver.find_element_by_id("main_txtSpoofText")
		inputSubmit = self.driver.find_element_by_id("main_btnGetData")

		inputDate.send_keys(date)
		inputSpoof.send_keys(spoof)

		print "County => %s" % county
		print "Date Added => %s" % date
		print "Spoof => %s" % spoof

		print "Submitting form"
		# submit the form (although google automatically searches now without submitting)
		inputSubmit.click()

		try:
			# Wait for the search results to appear
			#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
			WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("Footer"))

		except:
			print "Browser Timed Out!"
			return ""

		print "Getting soup data"
		soup = BeautifulSoup(unicode(self.driver.page_source))
		try:
			reportTable = soup.find("table", { "id" : "main_gvCrashInfo"})
		except:
			reportTable = None

		results = []
		if reportTable is not None:
			for row in reportTable.find_all("tr"):
				col = row.find_all("td")
				if len(col) > 0:
					docNo = BeautifulSoup(unicode(col[8]))
					docNo = docNo.find(text=True)
					docNo = str(docNo)

					if not docNo in oldReports.keys():
						link = d.single_ext_dps_state_oh_us(docNo, date)
						if link > "":
							# Report was downloaded
							newReports[docNo] = link

			for key in newReports.keys():
				link = newReports[key]
				# Rename table to ext_dps_stat_oh_us instead of _ohio_
				c.execute("INSERT INTO ext_dps_state_ohio_us (report_id, link, location) VALUES (%s, %s, %s)", [key, link, county])
				results.append(link)

			return results
		else:
			return ""