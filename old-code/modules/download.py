#!/usr/bin/env python

import os
import sys
import string
import urllib2
from urllib2 import quote
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# Replace urllib2? This works for HTTP Errors
#import requests
#from requests.exceptions import HTTPError

class Download(object):
	"""Downloads new reports from target sources"""

	def __init__(self):
		"""Initialization"""
		#self.server = "http://grabreports.com/"
		self.server = "http://grabreports.com/"
		self.reportdir = "/srv/service/grabreports/reports/"

	def single_ext_dps_state_oh_us(self, reportId, date, systemV):
		dateArr = string.split(date, "/")        
		month = dateArr[0]
		day = dateArr[1]
		year = dateArr[2]

		# pdfLink  = "https://ext.dps.state.oh.us/CrashRetrieval/ViewCrashReport.aspx?DocNumber=" + reportId + "&RequestFrom=ViewEfilePDF"
		pdfLink  = "https://services.dps.ohio.gov/CrashRetrieval/ViewCrashReport.aspx?CrashId=" + reportId + "&RequestFrom=ViewEfilePDF"
		fileName = "report_" + str(reportId) + ".pdf"
		filePath = "reports/ext.dps.state.oh.us/" + year + "/" + month + "/" + day + "/"

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				print "Path doesn't exist. Creating path"
				# Create path
				os.makedirs(filePath) 
		except:
			print "Failed to check/create path info"

		try:
			# Check if file exists. If not, download it.
			# This will need to be more accurate in the future
			if not os.path.exists(filePath + fileName):
				print "Downloading %s from %s" % (fileName, systemV)
				#print "Location: " + pdfLink
				thePdf = urllib2.urlopen(pdfLink)
				output = open(filePath + fileName,"wb")
				output.write(thePdf.read())
				output.close

				return self.server + filePath + fileName # Link to downloaded file
			else:
				return self.server + filePath + fileName # No file downloading, using old file
		except:
			print "Failed to download file or something"
			return ""


	def single_egovlink_com_vandalia(self, target, name):
		"""Downloads from http://www.egovlink.com/vandalia/docs/menu/home_ada.asp"""

		filePath = self.reportdir + "egovlink.com/vandalia/"

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				# Create path
				os.makedirs(filePath) 

			# Check if file exists. If not, download it.
			if not os.path.exists(filePath + name):
				print "Downloading " + name
				thePdf = urllib2.urlopen(target)
				output = open(filePath + name,"wb")
				output.write(thePdf.read())
				output.close
				return self.server + "egovlink.com/vandalia/" + name # File downloaded
			#else:
			#	print "File exists, returning link"
			#	return self.server + self.reportdir + "egovlink.com/vandalia/" + name # Returns local_link to fill in DB
				return self.server + self.reportdir + "egovlink.com/vandalia/" + name # File downloaded
			else:
				print "File exists, returning link"
				return self.server + self.reportdir + "egovlink.com/vandalia/" + name # Returns local_link to fill in DB

		except:
			print "Failure in download.py"
			return ""

	def single_butlertownship_com(self, target, name):
		"""Downloads from http://www.butlertownship.com/departments-services/police-department/reports-crash"""

		filePath = self.reportdir + "butlertownship.com/"

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				# Create path
				os.makedirs(filePath) 

			# Check if file exists. If not, download it.
			if not os.path.exists(filePath + name):
				print "Downloading " + name
				thePdf = urllib2.urlopen(target)
				output = open(filePath + name,"wb")
				output.write(thePdf.read())
				output.close
				return self.server + "reports/butlertownship.com/" + name # File downloaded
			else:
				print "File exists, returning link"
				return self.server + "reports/butlertownship.com/" + name # Returns local_link to fill in DB

		except:
			print "Failure in download.py"
			return ""

	def single_cityofbellbrook_org(self, target, name):
		"""Downloads from http://www.cityofbellbrook.org/government/departments/police/accident_reports.html"""

		filePath = self.reportdir + "cityofbellbrook.org/"

		# Use this to check for 404 error
		"""
		try:
			r = requests.get('http://httpbin.org/status/200')
			r.raise_for_status()
		except HTTPError:
			print 'Could not download page'
		else:
			print r.url, 'downloaded successfully'
		"""

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				# Create path
				os.makedirs(filePath) 

			# Check if file exists. If not, download it.
			if not os.path.exists(filePath + name):
				print "Downloading " + name
				thePdf = urllib2.urlopen(target)
				output = open(filePath + name,"wb")
				output.write(thePdf.read())
				output.close
				return self.server + "reports/cityofbellbrook.org/" + name # File downloaded
			else:
				print "File exists, returning link"
				return self.server + "reports/cityofbellbrook.org/" + name # Returns local_link to fill in DB

		except:
			print "Failure in download.py"
			return ""

	def single_lebanonohio_gov(self, target, name):
		"""Searches lebanonohio.gov"""
		name = "%s.pdf" % name
		filePath = self.reportdir + "lebanonohio.gov/"

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				# Create path
				os.makedirs(filePath) 

			# Check if file exists. If not, download it.
			if not os.path.exists(filePath + name):
				print "Downloading " + target
				thePdf = urllib2.urlopen(target)
				output = open(filePath + name,"wb")
				output.write(thePdf.read())
				output.close
				return self.server + "reports/lebanonohio.gov/%s" % name # File downloaded
			else:
				print "File exists, returning link"
				return self.server + "reports/lebanonohio.gov/%s" % name # Returns local_link to fill in DB

		except:
			print "Failure in download.py"
			return ""

	def single_franklinohio_org(self, target, name):
		"""Searches franklinohio.org"""

		filePath = self.reportdir + "franklinohio.org/"

		try:
			# Check if path exists
			if not os.path.exists(filePath):
				# Create path
				os.makedirs(filePath) 

			# Check if file exists. If not, download it.
			if not os.path.exists(filePath + name):
				print "Downloading " + name
				thePdf = urllib2.urlopen(target)
				output = open(filePath + name,"wb")
				output.write(thePdf.read())
				output.close
				return self.server + "reports/franklinohio.org/" + name # File downloaded
			else:
				print "File exists, returning link"
				return self.server + "reports/franklinohio.org/" + name # Returns local_link to fill in DB

		except:
			print "Failure in download.py"
			return ""

	def single_mason_ftp(self, host, file, folder):
		"""Searches ftp.masonoh.org"""
		
		downloadDir = self.reportdir + "ftp.masonoh.org/%s" % folder 
		local = "%s/%s" % (downloadDir, file)

		if not os.path.exists(downloadDir):
			try:
				os.makedirs(downloadDir)
			except:
				print "Failed to create download directory"
				return ""

		if not os.path.exists(local):
			host.download(file, local, 'b', host.keep_alive())  # remote, local, binary mode, keep_alive callback
			print "Downloaded => %s" % file
			return self.server + "reports/ftp.masonoh.org/%s/%s" % (folder, file)
		else:
			return self.server + "reports/ftp.masonoh.org/%s/%s" % (folder, file)

	def single_police_reports_us(self, target, reportNum, sid, rid, date, pFunction):
		dateArr = string.split(date, "/")        
		month = dateArr[0]
		day = dateArr[1]
		year = dateArr[2]

		if target == "http://ketteringoh.policereports.us/":
			targetLink = "viewreportpdf.html"
			
		elif target == "http://springfieldoh.policereports.us/":
			targetLink = "viewreportpdfrawv.html"
			
		else:
			targetLink = "viewreportpdfraw.html"

		#DisplayReportS = viewreport.html > "View Online"
		#DisplayReportP = viewreportpdfv.html > "View Online PDF"
		#DisplayReportP2 = viewreportpdfrawv.html > "View Online PDF"
		#DisplayReportP2d = viewreportpdfraw.html > "View Online PDF"

		if pFunction == "DisplayReportP":
			#targetLink = "viewreportpdfv.html" # V = iframe = doesn't work
			targetLink = "viewreportpdf.html"

		if pFunction == "DisplayReportP2":
			#targetLink = "viewreportpdfrawv.html" # V = iframe = doesn't work
			targetLink = "viewreportpdfraw.html"

		if pFunction == "DisplayReportP2d":
			targetLink = "viewreportpdfraw.html"

		pdfLink  = target + targetLink + "?" + sid + "&rid=" + str(rid) + "&f=report.pdf"
		fileName = "report_" + str(reportNum) + ".pdf"
		filePath = "reports/" + target.replace("http://","") + year + "/" + month + "/" + day + "/"

		# Check if path exists
		if not os.path.exists(filePath):
			#print "Path doesn't exist. Creating path"
			# Create path
			os.makedirs(filePath) 

		# Check if file exists. If not, download it.
		# This will need to be more accurate in the future
		if not os.path.exists(filePath + fileName):
			print "Downloading " + fileName
			print "From " + pdfLink

			#thePdf = urllib2.urlopen(pdfLink)
			#output = open(filePath + fileName,"wb")
			#output.write(thePdf.read())
			#output.close

			thePdf = requests.get(pdfLink)
			with open(filePath + fileName, "wb") as stuff:
				stuff.write(thePdf.content)

			# print "Returning " + self.server + filePath + fileName
			return self.server + filePath + fileName # File downloaded
		else:
			#print "Returning nothing"
			return self.server + filePath + fileName # No file downloaded, using old file