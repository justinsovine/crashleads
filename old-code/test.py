#!/usr/bin/env python

import os
import sys
import urllib2
import requests
import string

pdfLink = "http://hamiltonoh.policereports.us/viewreportpdfraw.html?sid=khoualj3j0tg5rk3sfjpf75d85&rid=0&f=report.pdf"

print "Downloading " + pdfLink
#thePdf = urllib2.urlopen(pdfLink)
thePdf = requests.get(pdfLink)

with open("test-report.pdf", "wb") as code:
    code.write(thePdf.content)

#output = open("test-report.pdf","wb")
#output.write(thePdf.read())
#output.close

