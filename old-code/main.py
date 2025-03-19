#!/usr/bin/env python

import os
import sys
import urllib2
import string
import MySQLdb
import datetime
#from multiprocessing import Pool

import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service

# Files in ./modules/
from modules import database, download, notify, pages, search

def main():
	"""Executive Function"""

	# Add app directory to PATH
	sys.path.append(os.path.dirname(os.path.abspath(__file__)))

	# Change to app directory
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	for arg in sys.argv:
		if arg == "--user=Cron":
			user = "Cron"
		else:
			user = "Manual"

	starttime = datetime.datetime.now()

	output = open("run.log","a")
	output.write("User: %s\n" % user)
	output.write("Started: %s\n" % starttime)
	output.close()

	# Start logger
	#l = logger.Log()

	# Main exception handler, prevents browser from being left open
	try:
		scriptStart = datetime.datetime.today()
		#l.simplelog("###Started @ " + str(scriptStart) + "###\n")

		# Start virtual display and browser
		print "Starting chromedriver"
		# Start chromedriver
                service = service.Service('/usr/bin/chromedriver')
                service.start()
		print "chromedriver started"

                # Start chromium
		print "Starting chromium"
                capabilities = {'chrome.binary': '/usr/bin/chromium'}
                driver = webdriver.Remote(service.service_url, capabilities)
		print "chromium started"

		#b = browser.Browser()
		#display = b.display()
		#driver = b.browser()

		# Server url
		# Do this with a simple config file
		#server = "http://grabreports.com/"
		server = "http://198.58.116.175/"

		# Create database connection
		db = database.Database()

		# Get all report source data
		print "Getting report sources\n"
		try:
			c = db.conn.cursor()
			c.execute("SELECT source, title, link FROM site_list WHERE active = 1")
			sources = c.fetchall()
		except:
			#l.simplelog("Failed to get report sources")
			#l.simplelog(sys.exc_info())
			sys.exit()

		# Loop through report sources
		newReportList = []
		newReportDict = {}
		for source, title, link in sources:
			# Initialize search
			s = search.Search(driver, db)

			# PoliceReports.us
			if source == "policereports.us":
				searchResults = s.check_police_reports_us(source, title, link)
				if len(searchResults) == 0:
					print "There were no new reports for %s => %s\n" % (source, title)
				else:
					print "There were %s new reports for %s => %s\n" % (str(len(searchResults)), source, title)
					#newReportList.extend(searchResults)
					newReportDict[title] = searchResults # Stores lists

			# egovlink.com/vandalia
			if source == "@egovlink.com/vandalia":
				location = "eGovLink Vandalia"
				print "Searching for %s" % source
				searchResults = s.check_egovlink_com_vandalia(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# cityofbellbrook.org
			if source == "@butlertownship.com":
				location = "Butler Township"
				print "Searching for %s" % source
				searchResults = s.check_butlertownship_com(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# cityofbellbrook.org
			if source == "@cityofbellbrook.org":
				location = "City of Bellbrook"
				print "Searching for %s" % source
				searchResults = s.check_cityofbellbrook_org(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s\n" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# ext.dps.state.oh.us
			
			if source == "@ext.dps.state.oh.us":
				print "Searching for " + source
				countyDict = {
					"09": "Butler",
					"12": "Clark",
					"13": "Clermont",
					"29": "Greene",
					"31": "Hamilton",
					"55": "Miami",
					"57": "Montgomery",
					"83": "Warren"
				}

				for cid, county in countyDict.items():
					searchResults = s.ext_dps_state_oh_us(source, cid, county)
					if len(searchResults) == 0:
						print "There were no new reports for %s => %s\n" % (source, county)
					else:
						print "There were %s new reports for %s => %s\n" % (str(len(searchResults)), source, county)
						print "There were " + str(len(searchResults)) + " reports\n"
						#newReportList.extend(searchResults)
						newReportDict[county] = searchResults # Stores lists
			
			# ftp.masonoh.org
			#if source == "ftp.masonoh.org":
			if source == "WILL_NOT_RUN":
				location = "Mason PD"
				print "Searching for %s" % source
				searchResults = s.check_mason_ftp(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s\n" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# franklinohio.org
			if source == "WILL_NOT_RUN":
				location = "Franklin PD"
				print "Searching for %s" % source
				searchResults = s.check_franklinohio_org(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s\n" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# lebanonohio.gov
			#if source == "lebanonohio.gov":
			if source == "WILL_NOT_RUN":
				location = "Lebanon PD"
				print "Searching for %s" % source
				searchResults = s.check_lebanonohio_gov(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s\n" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

		# Notify everyone of the new reports
		if len(newReportDict) > 0:
			n = notify.Notify(db, server)
			n.execute(newReportDict, scriptStart)

			print "People were notified"
			numReports = len(newReportDict)

		else:
			print "No one was notified"
			numReports = 0

	finally:
		print "Closing browser"
		driver.quit()
		service.stop()
		#l.simplelog("Exiting virtual display\n")
		#display.stop()
		#l.simplelog("Unlinking pidfile")
		#os.unlink(pidfile)

		runTime = datetime.datetime.now() - scriptStart
		output = open("run.log","a")
		output.write("Ended: %s\n" % starttime)
		output.write("Runtime: %s\n" % runTime)
		try:
			if numReports > 0:
				output.write("Reports: %s\n\n" % str(numReports))
			else:
				output.write("Reports: None\n\n")
		except:
			output.write("Reports: Unknown\n\n")
		output.close()

if __name__ == "__main__":
	main()
