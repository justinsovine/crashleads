#!/usr/bin/env python

import sys
import MySQLdb

class Pages(object):
	"""Returns the list of pages that should be searched"""

	def __init__(self, db):
		"""Initialization"""
		self.db = db

	def get_pages(self):

		# Get pages
		try:
			#print "Creating db cursor: pages"
			pages = self.db.conn.cursor()
			#print "Searching database for pages"
			pages.execute("SELECT source, title, link FROM site_list WHERE active = 1")

			#print "Compiling links"
			links = []
			for title, link in pages.fetchall():
				links.append(link)
			return links

		except:
			#sys.exit("An error occurred while attempting to search the database for pages")
			sys.exit(sys.exc_info())