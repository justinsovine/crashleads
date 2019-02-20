#!/usr/bin/env python3

import os
import logging
import time
import urllib.request, urllib.parse, urllib.error
import magic

def download_reports(report, file_path, pdf_src, report_type):
    try:
        if report_type == 'digital':
            # Digital external link
            digital_external_link = pdf_src
            logging.info('Downloading digital report')
            logging.debug(digital_external_link)
            digital_file_name = 'digital_report_%s.pdf' % report['crash_id']
            digital_file_path = '%s/%s' % (file_path, digital_file_name)
            scanned_external_link = ""
            scanned_file_path = ""

            # Check if file exists
            if not os.path.exists(digital_file_path):
                # Download file
                urllib.request.urlretrieve(digital_external_link, '%s' % digital_file_path)
            else:
                logging.info('File already exists at %s', digital_file_path)

            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(digital_file_path)
            if mimetype != 'application/pdf':
                digital_file_path = 'ERROR'

        if report_type == 'scanned':
            # Scanned external link
            scanned_external_link = pdf_src
            logging.info('Downloading scanned report')
            logging.debug(scanned_external_link)
            scanned_file_name = 'scanned_report_%s.pdf' % report['crash_id']
            scanned_file_path = '%s/%s' % (file_path, scanned_file_name)
            digital_external_link = ""
            digital_file_path = ""

            # Check if file exists
            if not os.path.exists(scanned_file_path):
                # Download file
                urllib.request.urlretrieve(scanned_external_link, '%s' % scanned_file_path)
            else:
                logging.info('File already exists at %s', scanned_file_path)

            mime = magic.Magic(mime=True)
            mimetype = mime.from_file(scanned_file_path)
            if mimetype != 'application/pdf':
                scanned_file_path = 'ERROR'

        if report_type == 'unknown':
            return False

        # Check if native digital (e.g. "CRASH_ECS", e.g. no scanned version)
        #if report['entered_by'] != 'CRASH_ECS':
        #    # Scanned version exists
        #    # Handle short FIPS codes
        #    if len(report['fips_code']) < 5:
        #        image_file_name = "%s0%s" % (report['county_code'], report['fips_code'])
        #    else:
        #        image_file_name = "%s%s" % (report['county_code'], report['fips_code'])
        #
        #    scanned_external_link = 'https://services.dps.ohio.gov/CrashRetrieval/ViewCrashReport.aspx?DocNumber=%s&ImageFileName=%s&RequestFrom=ViewPDF' % (
        #    report['document_number'], image_file_name)
        #    logging.info('Downloading scanned link: %s', scanned_external_link)
        #    scanned_file_name = 'scanned_report_%s_%s.pdf' % (report['entered_by'], report['crash_id'])
        #    scanned_file_path = '%s/%s' % (file_path, scanned_file_name)
        #
        #    # Check if file exists
        #    if not os.path.exists(scanned_file_path):
        #        # Download file
        #        urllib.request.urlretrieve(scanned_external_link, '%s' % scanned_file_path)
        #    else:
        #        # File exists
        #        logging.info('File already exists at %s', scanned_file_path)
        #else:
        #    scanned_external_link = ''
        #    scanned_file_path = ''
        #    logging.info('There was no scanned link. Report was natively digital.')

    except:
        return False

    return [report['crash_id'], digital_file_path, scanned_file_path]