#!/usr/bin/env python

import re
import sys
import time
import ftputil
import string
import datetime
import MySQLdb
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select

from modules import download

import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

reload(sys)  
sys.setdefaultencoding('utf8')

#import codecs

class Search(object):
	"""Searches target sources for new police reports"""

	def __init__(self, driver, db):
		"""Initialization"""
		self.driver = driver
		self.db = db
		self.numDays = 3 # 1 month


	def ext_dps_state_oh_us(self, source, cid, county):
		"""Searches ext.dps.state.oh.us"""

		dateTime = datetime.datetime.today()
		dateTimeArr = string.split(str(dateTime), " ")
		date = dateTimeArr[0]
		dateArr = string.split(str(date), "-")        
		year = dateArr[0]
		month = dateArr[1]
		day = dateArr[2]
		date = month + "/" + day + "/" + year
		#date = "03/05/2017" # Temporary

		target = "https://services.dps.ohio.gov/CrashRetrieval/OHCrashRetrieval.aspx"

		#print "Grabbing old reports"
		c = self.db.conn.cursor()
		c.execute("SELECT title, local_link FROM reports WHERE source = %s ORDER BY id DESC", source)
		oldReports = {}
		for title, link in c.fetchall():
			oldReports[str(title)] = str(link)

		d = download.Download()


		#
		# Load target page
		#
		try:
			print "Loading target " + target
			self.driver.get(target)

		except:
			print "Failed to load target"
			return ""
		
		print "Retrieved source code"

		
		#
		# Search target page
		#
		print "Submitting search for %s => %s" % (cid, county)
		inputCounty = Select(self.driver.find_element_by_id("main_cboCounty"))

		print "Selecting county, waiting for __doPostBack()"
		inputCounty.select_by_value(cid)

		try:
			# Wait for the search results to appear
			#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
			WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("Footer"))
			print "Results have appeared"

		except:
			print "Browser Timed Out!"
			return ""

		print "Entering crash date"
		inputDate = self.driver.find_element_by_id("main_txtCrashAddDate")
		print date
		inputDate.send_keys(date)

		print "Solving CAPTCHA...",
		spoof = re.search("rndval=[A-Z0-9]{5}", self.driver.page_source)
		spoof = spoof.group(0)
		spoof = spoof.replace("rndval=", "")
		inputSpoof = self.driver.find_element_by_id("main_txtSpoofText")
		inputSpoof.send_keys(spoof)
		print "DONE"

		print "Submitting form..."
		print "County => %s" % county
		print "Date Added => %s" % date
		print "Spoof => %s" % spoof
		inputSubmit = self.driver.find_element_by_id("main_btnGetData")
		inputSubmit.click()

		try:
			# Wait for the search results to appear
			#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
			WebDriverWait(self.driver, 15).until(lambda x: x.find_element_by_id("Footer"))

		except:
			print "Browser Timed Out!"
			return ""

		try:
			pageCountText = self.driver.find_element_by_id("main_lblPageCount")
		except:
			print "No page count listed, probably no reports for this county yet"
			return ""

		pageCountArr  = pageCountText.text.split(' ')
		currentPage   = int(pageCountArr[1])
		numOfPages    = int(pageCountArr[4])

		#
		# Iterate through available pages
		#
		results = []
		while currentPage <= numOfPages:
			print "\n\nScanning page %s of %s\n" % (str(currentPage), str(numOfPages))

			newReports = {} # starts fresh for every page
			soup = BeautifulSoup(unicode(self.driver.page_source))

			try:
				reportTable = soup.find("table", { "id" : "main_gvCrashInfo"})
			except:
				reportTable = None.text

			if reportTable is not None:
				for row in reportTable.find_all("tr"):
					col = row.find_all("td")
					if len(col) == 13:
						#print "Columns - 13"

						docNo = BeautifulSoup(unicode(col[12]))
						docNo = str(docNo.find(text=True))

						systemV = BeautifulSoup(unicode(col[11]))
						systemV = str(systemV.find(text=True))

						#print "Entered - " + systemV

						if not docNo in oldReports.keys():
							link = d.single_ext_dps_state_oh_us(docNo, date, systemV)
							if link > "":
								# Report was downloaded
								newReports[docNo] = link

					elif len(col) == 1:

						print "Time to search the next page if there is one"


				for key in newReports.keys():
					dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
					link = newReports[key]
					
					c.execute("INSERT INTO reports (title, local_link, location, datetime_posted, source) VALUES (%s, %s, %s, %s, %s)", [key, link, county, dateTimePostedUnix, source])
					results.append(link)

				print "Stored %s reports in database" % str(len(newReports))

				if currentPage != numOfPages:
					print "Clicking Next>"
					goToNextPage = self.driver.find_element_by_link_text("Next>")
					goToNextPage.click()

					try:
						# Wait for the search results to appear
						#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
						WebDriverWait(self.driver, 15).until(lambda x: x.find_element_by_id("Footer"))

					except:
						print "Browser Timed Out!"
						return ""

					print "Successfully loaded next page"

				else:
					print "Done scanning all pages"

				currentPage = currentPage + 1

		print "Returning results: " + str(len(results))
		return results

    # Offline
	def check_egovlink_com_vandalia(self, source, location, target):
		"""Searches http://www.egovlink.com/vandalia/docs/menu/home_ada.asp"""

		reports = []
		names = []
		d = download.Download()

		theTarget = "http://www.egovlink.com/vandalia/docs/menu/home_ada.asp"

		self.driver.get(theTarget)

		print "Getting soup data"
		soup = BeautifulSoup(unicode(self.driver.page_source))

		for a in soup.findAll('a'):
			link = str(a['href'])
			link = link.replace(' ', '%20')

			try:
				if link.index('.pdf'):
					try:
						if link.index('Crash%20Report'):
							isCorrectPdf = True
					except:
						isCorrectPdf = False
			except:
				isCorrectPdf = False

			if isCorrectPdf is True:
				# links are full links to PDF
				#link = link
				arr = link.split('/')
				name = arr[-1]
				name = name.replace('%20', '-')

				c = self.db.conn.cursor()
				c.execute("SELECT title FROM reports WHERE title = %s AND source = %s", [name, source])

				# Check if report already exists
				if not c.fetchone():
					# Download file
					results = d.single_egovlink_com_vandalia(link, name)
					if results != "":
						dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
						c = self.db.conn.cursor()
						c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [name, results, source, location, dateTimePostedUnix])
						reports.append(results)

		if len(reports) > 0:
			return reports
		else:
			return ""

	def check_butlertownship_com(self, source, location, target):
		"""Searches http://www.butlertownship.com/departments-services/police-department/reports-crash"""

		reports = []
		names = []
		d = download.Download()

		self.driver.get('http://www.butlertownship.com/departments-services/police-department/reports-crash')

		print "Getting soup data"
		soup = BeautifulSoup(unicode(self.driver.page_source))

		for a in soup.findAll('a'):
			link = str(a['href'])
			link = link.replace(' ', '%20')

			try:
				if link.index('.pdf'):
					isPdf = True
			except:
				isPdf = False

			if isPdf is True:
				# links are full links to PDF
				#link = link
				arr = link.split('/')
				name = arr[-1]
				name = name.replace('%20', '-')

				c = self.db.conn.cursor()
				c.execute("SELECT title FROM reports WHERE title = %s AND source = %s", [name, source])

				# Check if report already exists
				if not c.fetchone():
					# Download file
					results = d.single_butlertownship_com(link, name)
					if results != "":
						dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
						c = self.db.conn.cursor()
						c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [name, results, source, location, dateTimePostedUnix])
						reports.append(results)

		if len(reports) > 0:
			return reports
		else:
			return ""

	def check_cityofbellbrook_org(self, source, location, target):
		"""Searches http://www.cityofbellbrook.org/government/departments/police/accident_reports.html"""

		reports = []
		names = []
		d = download.Download()

		self.driver.get('http://www.cityofbellbrook.org/government/departments/police/accident_reports.html')

		print "Getting soup data"
		soup = BeautifulSoup(unicode(self.driver.page_source))

		for a in soup.findAll('a'):
			link = str(a['href'])
			link = link.replace(' ', '%20')

			try:
				if link.index('.pdf'):
					isPdf = True
			except:
				isPdf = False

			if isPdf is True:
				# link looks like 'documents/nameofpdf.pdf'
				link = "http://www.cityofbellbrook.org/government/departments/police/" + link
				arr = link.split('/')
				name = arr[-1]
				name = name.replace('%20', '-')

				c = self.db.conn.cursor()
				c.execute("SELECT title FROM reports WHERE title = %s AND source = %s", [name, source])

				# Check if report already exists
				if not c.fetchone():
					# Download file
					results = d.single_cityofbellbrook_org(link, name)
					if results != "":
						dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
						c = self.db.conn.cursor()
						c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [name, results, source, location, dateTimePostedUnix])
						reports.append(results)

		if len(reports) > 0:
			return reports
		else:
			return ""

	def check_police_reports_us(self, source, county, target):
		"""Searches http://policereports.us"""

		# Load target website
		try:
			print "Loading target ", target
			print self.driver.get(target)
			sys.exit()
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
						if data.index("Last Report Upload"):
							wwwSoup = BeautifulSoup(data)
							wwwLastUpdate = wwwSoup.find(text=True)
							wwwLastUpdate = wwwLastUpdate.replace("Last Report Upload", "")
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
				wwwLastUpdate = wwwLastUpdate.replace("Last Report Upload", "")

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
			updateResults = self.scan_police_reports_us(source, county, target)
			c.execute("UPDATE site_list SET last_update = %s WHERE link = %s", [wwwLastUpdate, target])
			return updateResults
		else:
			print "This is legitimately up-to-date"
			return ""

    # Offline
	def scan_police_reports_us(self, source, county, target):
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
		c.execute("SELECT title, local_link FROM reports WHERE source = %s ORDER BY title ASC", source)
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
			self.driver.execute_script("jQuery('input#mDate').val('" + date + "')")
			self.driver.execute_script("jQuery('#searchform').submit()")

			try:
				# Wait for the search results to appear
				#WebDriverWait(self.driver.page_source, 10).until(lambda x: x.re.search("Your search returned [1-9]* results").group(0))
				WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.PARTIAL_LINK_TEXT, "<< Go Back"))

			except:
				print "Browser Timed Out!"
				#print sys.exc_info()

			#print "Grabbing SID"
			# Grab sid for links
			s = self.driver.page_source
			sid = re.search( "sid=[a-z0-9]*", s)
			sid = sid.group(0) # Grabs the first instance

			#DisplayReportS = viewreport.html > "View Online"
			#DisplayReportP = viewreportpdfv.html > "View Online PDF"
			#DisplayReportP2 = viewreportpdfrawv.html > "View Online PDF"
			#DisplayReportP2d = viewreportpdfraw.html > "View Online PDF"

			# First 4 are functions
			# Every entry uses two DisplayReportXXX links
			s = self.driver.page_source
			pattern = "DisplayReportP[a-zA-Z0-9]{0,2}"
			i=0
			onOff = 1 #on
			pList = []
			for pFunction in re.findall(pattern, s):
				if i >= 4:
					if onOff == 1:
						pList.append(pFunction)
						onOff = 0
					else:
						onOff = 1
				i = i + 1
			
			#print "Parsing all search results"
			# Check for new reports
			soup = BeautifulSoup(unicode(self.driver.page_source))
			rid = 0

			#links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "View Online PDF")

			i = 0
			for row in soup.find_all("tr", { "class" : "searchresult"}):
				col = row.find_all("td")
				columnString = unicode(col[0])

				if len(col) == 4:
					pFunction = pList[rid]

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
						link = d.single_police_reports_us(target, reportNumber, sid, rid, date, pFunction)
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
				dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
				link = newReports[key]
				c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [key, link, source, county, dateTimePostedUnix])
				diffList.append(link)

			return diffList
		else:
			print "Returning nothing"
			return ""

    # Offline
	def check_franklinohio_org(self, source, location, target):
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
					isPdf = True
			except:
				isPdf = False

			if isPdf is True:
				link = "http://franklinohio.org" + link
				arr = link.split('/')
				name = arr[-1]

				c = self.db.conn.cursor()
				c.execute("SELECT title FROM reports WHERE title = %s AND source = %s", [name, source])

				# Check if report already exists
				if not c.fetchone():
					# Download file
					results = d.single_franklinohio_org(link, name)
					if results != "":
						dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
						c = self.db.conn.cursor()
						c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [name, results, source, location, dateTimePostedUnix])
						reports.append(results)

		if len(reports) > 0:
			return reports
		else:
			return ""

    # Offline
	def check_mason_ftp(self, source, location, link):
		"""Searches ftp.masonoh.org"""

		links = []

		d = download.Download()

		# Connect and enter crash reports directory
		host = ftputil.FTPHost(link, 'anonymous', '')
		try:
			host.chdir('public download/mpd traffic crash reports/')
		except:
			print "The file structure has changed"

		try:
			# Iterate through folders
			folders = host.listdir(host.curdir)
			for folder in folders:
				statarr = host.stat(folder)
				# statarr[8] = date modified unix timestamp
				dmod = str(datetime.datetime.fromtimestamp(int(statarr[8])).strftime('%Y-%m-%d %H:%M:%S'))

				# Query date modified
				c = self.db.conn.cursor()
				c.execute("SELECT last_update FROM ftp_masonoh_org WHERE folder = %s", folder)
				lastUpdate = c.fetchone()
				if lastUpdate != None:
					for data in lastUpdate:
						storedDate = data
				else:
					storedDate = None

				# Folder is new
				if not storedDate:
					c = self.db.conn.cursor()
					c.execute("INSERT INTO ftp_masonoh_org (folder) VALUES (%s)", folder)
					storedDate = ""

				# Folder has new files
				if not storedDate == dmod:
					# Update datemodified
					c = self.db.conn.cursor()
					c.execute("UPDATE ftp_masonoh_org SET last_update = %s WHERE folder = %s", [dmod, folder])

					# Enter folder
					print "Entering %s" % folder
					host.chdir(folder)
					files = host.listdir(host.curdir)
					
					# Iterate through files
					for file in files:
						if host.path.isfile(file):

							c = self.db.conn.cursor()
							c.execute("SELECT title FROM reports WHERE title = %s AND source = %s", [file, source])

							# Check if report already exists
							if not c.fetchone():
								# Download file
								results = d.single_mason_ftp(host, file, folder)
								if results != "":
									dateTimePostedUnix = int(time.mktime(datetime.datetime.now().timetuple()))
									links.append(results)
									c = self.db.conn.cursor()
									c.execute("INSERT INTO reports (title, local_link, source, location, datetime_posted) VALUES (%s, %s, %s, %s, %s)", [file, results, source, location, dateTimePostedUnix])
								else:
									print "There was a problem downloading a file from FTP"

						else:
							print "There was a folder when a file was expected"

					print "Exiting %s" % folder
					host.chdir("../")
		except:
			# Prevents timeouts from not relaying new content
			print "Exception raised, probably an FTP timeout"

		if len(links) > 0:
			return links
		else:
			return ""
