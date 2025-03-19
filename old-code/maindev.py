#!/usr/bin/env python

import os
import sys
import urllib2
import string
import MySQLdb
import datetime
#from multiprocessing import Pool

import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import selenium.webdriver.chrome.service as service

# Files in ./modules/
from modules import database, download, notify, pages, search

def main():
	"""Executive Function"""

	# Add app directory to PATH
	sys.path.append(os.path.dirname(os.path.abspath(__file__)))

	# Change to app directory
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	
	starttime = datetime.datetime.now()

	# Main exception handler, prevents browser from being left open
	try:
		scriptStart = datetime.datetime.today()

		print "\nCreating virtual display"
		display = Display(backend='xvfb', visible=0, size=(800, 600))
		display.start()

		# Start chromedriver
		#print "Starting chromedriver"
		#serviceA = service.Service('/usr/bin/chromedriver')
		#serviceA.start()
		#print "chromedriver started"

        # Start chromium
		#print "Starting chromium"
		#capabilities = {'chrome.binary': '/usr/bin/chromium'}
		#driver = webdriver.Remote(serviceA.service_url, capabilities)
		#driver = webdriver.Chrome('/usr/bin/chromedriver')  # Optional argument, if not specified will search path.
		#print "chromium started"

		#print "Starting Firefox"
		driver = webdriver.Firefox()

		# Server url
		# Do this with a simple config file
		server = "http://grabreports.com/"

		# Create database connection
		db = database.Database()

		# Get all report source data
		print "Getting report sources\n"
		try:
			c = db.conn.cursor()
			c.execute("SELECT source, title, link FROM site_list WHERE active = 1")
			sources = c.fetchall()
		except:
			print "Failed to get report sources"
			print sys.exc_info()
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
			if source == "DEV_egovlink.com/vandalia":
				location = "eGovLink Vandalia"
				print "Searching for %s" % source
				searchResults = s.check_egovlink_com_vandalia(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# cityofbellbrook.org
			if source == "DEV_butlertownship.com":
				location = "Butler Township"
				print "Searching for %s" % source
				searchResults = s.check_butlertownship_com(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# cityofbellbrook.org
			if source == "DEV_cityofbellbrook.org":
				location = "City of Bellbrook"
				print "Searching for %s" % source
				searchResults = s.check_cityofbellbrook_org(source, location, link)
				if len(searchResults) > 0:
					print "There were %s new reports for %s\n" % (str(len(searchResults)), source)
					newReportDict[location] = searchResults # Stores lists
				else:
					print "There were no new reports for %s\n" % source

			# ext.dps.state.oh.us
			
			if source == "DEV_ext.dps.state.oh.us":
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
		display.stop()
		driver.quit()
		#serviceA.stop()

if __name__ == "__main__":
	main()
