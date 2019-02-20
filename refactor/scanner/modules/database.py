#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# Intellect37, LLC 2017 #
# # # # # # # # # # # # #

import os
import sys
import time
import pprint
import logging

import MySQLdb
import MySQLdb.cursors

class DatabaseModel:
    def __init__(self):
        # connect to database
        self.db = MySQLdb.connect(  host="localhost",  # your host, usually localhost
                                    user="crashleadsprod",  # your username
                                    passwd="crashleads2017!",  # your password
                                    db="crashleads_prod",
                                    cursorclass=MySQLdb.cursors.DictCursor )  # cursor type
        self.db.set_character_set('utf8')

        # initialize database cursor
        self.c = self.db.cursor()
        self.c.execute('SET NAMES utf8;')
        self.c.execute('SET CHARACTER SET utf8;')
        self.c.execute('SET character_set_connection=utf8;')

    def select_all_report_ids(self):
        """Returns report ID's"""

        self.c.execute('SELECT crash_id FROM crashleads_reports_test ORDER BY id DESC LIMIT 5000')
        report_ids = [item['crash_id'] for item in self.c.fetchall()]
        return report_ids

    def insert_report_data(self, report_data):
        """Stores report data"""

        print('Inserting data into database')
        try:
            self.c.execute("""
                INSERT INTO crashleads_reports_test 
                (
                    unix_timestamp, local_report_id, crash_date, p, location, law_enforcement, jurisdiction, crash_severity,
                    doc_no, crash_county_number, crash_fips, entered_by, crash_id, digital_external_link, scanned_external_link
                )
                VALUES 
                (
                    %(unix_timestamp)s, %(local_report_num)s, %(crash_date)s, %(p)s, %(location)s, %(law_enforcement)s, 
                    %(jurisdiction)s, %(severity)s, %(document_number)s, %(county_code)s, %(fips_code)s, 
                    %(entered_by)s, %(crash_id)s, %(digital_external_link)s, %(scanned_external_link)s
                )""", report_data)

            self.db.commit() # Success & commit
        except Exception as ex:
            print(ex)
            print('wtf')
            return False

        return True