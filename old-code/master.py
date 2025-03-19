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

import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

reload(sys)  
sys.setdefaultencoding('utf8')

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

			# ext.dps.state.oh.us
			if source == "ext.dps.state.oh.us":
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
