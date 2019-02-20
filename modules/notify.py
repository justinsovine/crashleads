#!/usr/bin/env python3

import os
import re
import sys
import pprint
import logging
import pprint
import time
import urllib.request, urllib.parse, urllib.error
import mandrill
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import MySQLdb
import MySQLdb.cursors

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="crashleadsprod",  # your username
                     passwd="crashleads2017!",  # your password
                     db="crashleads_prod",
                     cursorclass=MySQLdb.cursors.DictCursor)  # Cursor type
db.set_character_set('utf8')

c = db.cursor()
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')

def build_email(reports_id):
    c.execute('SELECT * FROM crashleads_reports WHERE id = %s', (reports_id,))
    row = c.fetchone()

    email_build = '<p>'
    email_build = email_build + '<strong>County:</strong> %s<br>' % row['crash_county_number']
    email_build = email_build + '<strong>Local Report ID #%s</strong><br>' % row['local_report_id']
    email_build = email_build + '<strong>Crash Date: </strong> %s<br>' % row['crash_date']
    #email_build = email_build + '<strong>Hit/Skip? </strong> Coming Momentarily<br>'

    if row['digital_internal_link'] != '' and row['scanned_internal_link'] != 'ERROR':
        email_build = email_build + '<strong>Digital Report:</strong> <a href="http://cl-slave-01.crashleads.com/%s">Direct Link</a><br>' % (row['digital_internal_link'])
    else:
        email_build = email_build + '<strong>Digital Report:</strong> N/A<br>'

    if row['scanned_internal_link'] != '' and row['scanned_internal_link'] != 'ERROR':
        email_build = email_build + '<strong>Scanned Report:</strong> <a href="http://cl-slave-01.crashleads.com/%s">Direct Link</a><br>' % (row['scanned_internal_link'])
    else:
        email_build = email_build + '<strong>Scanned Report:</strong> N/A<br>'

    email_build = email_build + '</p>'

    unit_at_fault = row['unit_at_fault']


    c.execute('SELECT * FROM crashleads_individuals WHERE reports_id = %s ORDER BY units_id, address ASC', (reports_id,))

    i = 1
    for row in c.fetchall():
        if str(row['units_id']) == str(unit_at_fault):
            at_fault = "Yes"
        else:
            at_fault = "No"

        email_build = email_build + '<p>'
        email_build = email_build + '<strong>Person %i</strong><br>' % i

        if row['units_id'] != '':
            email_build = email_build + '<strong>Unit #:</strong> %s<br>' % row['units_id']

        if row['full_name'] != '':
            email_build = email_build + '<strong>Full Name:</strong> %s<br>' % row['full_name']

        if row['full_address'] != '':
            email_build = email_build + '<strong>Address:</strong> %s<br>' % row['full_address']

        if row['phone'] != '':
            phone_link = row['phone'].replace('-', '')
            phone_link = 'tel:+1' + phone_link
            email_build = email_build + '<strong>Phone:</strong> <a href="%s">%s</a><br>' % (phone_link, row['phone'])

        injury_level = [
            'There was a problem scraping this data. Submit to support@crashleads.com',
            'No Injury / None Reported',
            'Possible Injury',
            'Non-Incapacitating',
            'Incapacitating',
            'Fatal'
        ]

        if row['injuries'] != '':
            email_build = email_build + '<strong>Injuries:</strong> %s<br>' % injury_level[int(row['injuries'])]

        if row['air_bag_usage'] != '':
            if row['air_bag_usage'] == '0' or row['air_bag_usage'] == '1' or row['air_bag_usage'] == 1 or row['air_bag_usage'] == 0:
                air_bag_usage = 'No'
            else:
                air_bag_usage = 'Yes'
            email_build = email_build + '<strong>Air Bag Deployed:</strong> %s<br>' % air_bag_usage

        email_build = email_build + '<strong>Unit at Fault?</strong> %s<br>' % at_fault
        email_build = email_build + '<strong>Insurance:</strong> Coming soon<br>'
        email_build = email_build + '<strong>On DNC List?</strong> Coming soon<br>'

        email_build = email_build + '</p>'
        i = i + 1

    return email_build


def notify_via_email(email_html, crash_id, reports_id, crash_date, scanned_file_path, current_cid):

    if len(scanned_file_path) > 0 and scanned_file_path != 'ERROR':
        premium = True
        subject = '[Scanned] Report #%s - Crash Date: %s - CID: %s' % (crash_id, crash_date, current_cid)
    else:
        premium = False
        subject = '[Digital] Report #%s - Crash Date: %s - CID: %s' % (crash_id, crash_date, current_cid)

    # The client who gets these emails only wants to receive items from these counties
    # This should be in a table in the db but we don't really support email notifications anymore
    # because we're using the web portal and mobile push notifications now.
    client_list = {
            "83": "Warren",
            "09": "Butler",
            "31": "Hamilton",
            '68': 'Preble',
            "57": "Montgomery",
            "13": "Clermont",
            '14': 'Clinton'
    }

    if str(current_cid) in client_list:
        contact_list = ['client@crashleads.com', 'us@crashleads.com']
    else:
        contact_list = ['us@crashleads.com']

    
    contact_list = list(set(contact_list))

    if contact_list:
        try:
            mandrill_client = mandrill.Mandrill('REDACTED!')
            message = {
                'from_email': 'noreply@crashleads.com',
                'from_name': 'CrashLeads',
                'headers': {'Reply-To': 'noreply@crashleads.com'},
                'text': email_html,
                'html': email_html,
                'to': [{"email": contact} for contact in contact_list],
                'subject': subject,
                'track_clicks': True,
                'track_opens': True,
                'url_strip_qs': None
            }
            result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
            logging.info(result)

        except (mandrill.Error) as e:
            # Mandrill errors are thrown as exceptions
            logging.error('A mandrill error occurred: %s - %s') % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
            #return e

        return result
    else:
        return False

