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
                     user="REDACTED!",  # your username
                     passwd="REDACTED!",  # your password
                     db="REDACTED!",
                     cursorclass=MySQLdb.cursors.DictCursor)  # Cursor type
db.set_character_set('utf8')

c = db.cursor()
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')


def get_old_reports():
    c.execute('SELECT crash_id FROM crashleads_reports')
    report_list = [item['crash_id'] for item in c.fetchall()]
    return report_list


def store_report_data(report):
    # Insert REPORT data into database
    try:
        print(report)
        if 'unit_at_fault' not in report:
            report['unit_at_fault'] = 'Unknown'
        if 'digital_file_path' not in report:
            report['digital_file_path'] = ''
        if 'scanned_file_path' not in report:
            report['scanned_file_path'] = ''

        c.execute("""
            INSERT INTO crashleads_reports 
            (
                unix_timestamp, local_report_id, crash_date, p, location, law_enforcement, jurisdiction, crash_severity,
                doc_no, crash_county_number, crash_fips, entered_by, crash_id, digital_internal_link, scanned_internal_link, unit_at_fault
            )
            VALUES 
            (
                %(unix_timestamp)s, %(local_report_num)s, %(crash_date)s, %(p)s, %(location)s, %(law_enforcement)s, 
                %(jurisdiction)s, %(severity)s, %(document_number)s, %(county_code)s, %(fips_code)s, 
                %(entered_by)s, %(crash_id)s, %(digital_file_path)s, %(scanned_file_path)s, %(unit_at_fault)s
            )""", report)

        db.commit() # Success & commit
        logging.info('Report %s was successfully stored' % report['crash_id'])

        # Return ID
        c.execute('SELECT LAST_INSERT_ID()')
        row = c.fetchone()
        return int(row['LAST_INSERT_ID()'])

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        logging.error(e)
        # Rollback in case there is any error
        db.rollback() # Failure & rollback
        logging.error('Report %s failed to be stored' % report['crash_id'])
        # Record Rollback error
        return False

def store_unit_data(report, reports_id):
    # Insert REPORT data into database
    try:
        report_unit = report['unit']
    except:
        return False


    for unit_num, unit_data in report['unit'].items():

        print(report['unit'])
        regex = re.compile('[^a-zA-Z]')
        #First parameter is the replacement, second parameter is your input string
        unit_data['insurance'] = regex.sub('', unit_data['insurance'])
        print(unit_data)
        print(unit_num)

        #Out: 'abdE'

        unit_data['insurance'] = unit_data['insurance'].replace('\n', ' ').replace('\r', '')

        unit_data['reports_id'] = int(reports_id)
        try:
            c.execute("""
                INSERT INTO crashleads_units 
                (
                    reports_id, unit_number, insurance
                )
                VALUES 
                (
                    %(reports_id)s, %(unit_number)s, %(insurance)s
                )""", unit_data)

            db.commit() # Success & commit
            logging.info('Unit %s was successfully stored' % report['crash_id'])

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            logging.error(e)
            # Rollback in case there is any error
            db.rollback() # Failure & rollback
            logging.error('Unit failed to be stored')
            # Record Rollback error


def store_person_data(report, reports_id):
    pp = pprint.PrettyPrinter(indent=4)
    # Loop through individuals

    try:
        for person_num, person_data in report['person'].items():

            person_data['reports_id'] = int(reports_id)

            if person_data['unit_number'] != '':
                person_data['unit_number'] = int(person_data['unit_number'])
            else:
                person_data['age'] = 0

            if person_data['age'] != '' and person_data['age'] != 'AGE':
                person_data['age'] = int(person_data['age'])
            else:
                person_data['age'] = 0

            if person_data['injuries'] != '':
                person_data['injuries'] = int(person_data['injuries'])
            else:
                person_data['injuries'] = 0

            if person_data['air_bag'] != '' and person_data['air_bag'] != 'AIR BAG USAGE':
                person_data['air_bag'] = int(person_data['air_bag'])
            else:
                person_data['air_bag'] = 0

            if person_data['full_name'] != '' and person_data['address'] == '':
                if report['scanned_file_path'] != '':
                    person_data['address'] = 'Not Listed.Check scanned report'
                else:
                    person_data['address'] = 'Not Listed. There is no scanned report'

            if person_data['full_name'] != '' and person_data['phone'] == '':
                if report['scanned_file_path'] != '' and report['scanned_file_path'] != 'ERROR':
                    person_data['phone'] = 'Not Listed.Check scanned report'
                else:
                    person_data['phone'] = 'Not Listed. There is no scanned report'

            if person_data['full_name'] != '' and 'unknown' not in person_data['full_name'].lower():

                # Insert PERSON data into database
                try:
                    c.execute("""
                        INSERT INTO crashleads_individuals 
                        (
                            reports_id, units_id, full_name, first_name, middle_name, last_name, age, gender, full_address, 
                            zip, phone, injuries, air_bag_usage
                        )
                        VALUES 
                        (
                            %(reports_id)s, %(unit_number)s, %(full_name)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(age)s, 
                            %(gender)s, %(address)s, %(zip)s, %(phone)s, %(injuries)s, %(air_bag)s
                        )""", person_data)

                    db.commit() # Success & commit
                    logging.info('Person was successfully stored')

                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    logging.error(e)
                    # Rollback in case there is any error
                    db.rollback() # Failure & rollback
                    logging.error('Person failed to be stored')
                    # Record Rollback error
            else:
                logging.debug('Prob hit & run or blank field') # Not really an error in most cases
    except:
        logging.error(sys.exc_info())
        pp.pprint(report)

    return True
