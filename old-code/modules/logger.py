#!/usr/bin/env python

class Log(object):
	"""Logs to a file or the terminal"""

	def __init__(self):
		"""Initialization"""

	def simplelog(self, string):
		try:
			print string
			return 0
		except:
			print "Failed to log"
			return 1