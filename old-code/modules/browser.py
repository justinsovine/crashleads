#!/usr/bin/env python

import time

import os, sys
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import selenium.webdriver.chrome.service as service

class Browser(object):
	"""Allows the script to control a real browser using a virtual display"""

	def __init__(self):
		"""Initialization"""

	def display(self):

		# Create virtual display
		try:
			print "\nCreating virtual display"
			display = Display(backend='xvfb', visible=0, size=(800, 600))
			display.start()
			#print "Virtual display was created"
			return display
		except:
			sys.exit("There was an error while creating the virtual display")

	def browser(self):
			
		# Launch web browser
		try:
			print "Launching browser\n"

			# Start chromedriver
			service = service.Service('/usr/bin/chromedriver')
			service.start()

			# Start chromium
			capabilities = {'chrome.binary': '/usr/bin/chromium'}
			driver = webdriver.Remote(service.service_url, capabilities)
			
			#profile = webdriver.FirefoxProfile()

			#profile.default_preferences["webdriver_assume_untrusted_issuer"] = "false"
			#profile.default_preferences["webdriver_accept_untrusted_certs"] = "true"

			#profile.set_preference("webdriver_assume_untrusted_issuer", False)
			#profile.set_preference("webdriver_accept_untrusted_certs", True)
			#profile.set_preference["webdriver_assume_untrusted_issuer"] = "false"
			#profile.set_preference["webdriver_accept_untrusted_certs"] = "true"
			#profile.update_preferences()

			#capabilities = webdriver.DesiredCapabilities().FIREFOX
			#capabilities['acceptSsslCerts'] = True
			#driver = webdriver.Firefox(capabilities=capabilities)

			## get the Firefox profile object
			#firefoxProfile = FirefoxProfile()
			
			#firefoxProfile.accept_untrusted_certs = True			

			## Disable CSS
			#firefoxProfile.set_preference('permissions.default.stylesheet', 2)

			## Disable images
			#firefoxProfile.set_preference('permissions.default.image', 2)

			## Disable Flash
			#firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

			## Set the modified profile while creating the browser object 
			#driver = webdriver.Firefox(firefox_profile=firefoxProfile)
			## get the Firefox profile object
			#firefoxProfile = FirefoxProfile()

			## Disable CSS
			#firefoxProfile.set_preference('permissions.default.stylesheet', 2)

			## Disable images
			#firefoxProfile.set_preference('permissions.default.image', 2)

			## Disable Flash
			#firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

			## Set the modified profile while creating the browser object 
			#driver = webdriver.Firefox(firefoxProfile)

			#driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT)

			print "Browser was launched"
			return driver
		except:
			sys.exit("There was an error while launching the web browser")
