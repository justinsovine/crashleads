#!/usr/bin/env python

import sys
import MySQLdb

class Database(object):
	"""Initializes a database connection"""

	def __init__(self):
		"""Docstring"""
		try:
			#print "Initializing the database connection"
			self.conn = MySQLdb.connect(host = "localhost",
										user = "grabreports",
										passwd = "grabreports2015!",
										db = "grabreports")
			#print "Database was successfully initialized"

		except:
			sys.exit("There was an error while initializing the database")
