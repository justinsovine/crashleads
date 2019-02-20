#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # # # # # # # # # #
# Intellect37, LLC  #
# # # # # # # # # # #

import re
from bs4 import BeautifulSoup
import getpass
import logging
import time
from datetime import datetime, timedelta
import os
import sys
import argparse
import pprint
import signal 

# Multiprocessing
from itertools import repeat
from multiprocessing import Pool, freeze_support

# This should be in a module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Import files in ./modules/
from modules.download import download_reports
from modules.ocr import run_tet, get_xml_info
from modules.model import store_report_data, store_unit_data, store_person_data, get_old_reports
from modules.notify import build_email, notify_via_email


# Wait for page to load by searching for presence of element
def verify_page_loaded_by_id(driver, element_id, time_to_wait=10):
    try:
        WebDriverWait(driver, time_to_wait).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        logging.debug("Page loaded.")
        return True
    except:
        logging.warning('Page timed out!')
        return False


def verify_page_loaded_by_partial_link_text(driver, partial_text, time_to_wait=10):
    try:
        WebDriverWait(driver, time_to_wait).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, partial_text))
        )
        logging.debug("Page loaded.")
        return True
    except:
        logging.warning('Page timed out!')
        return False

def start_driver():
    driver = webdriver.PhantomJS(port=4444)
    driver.set_window_size(1366, 768)
    logging.info('Started WebDriver.')
    return driver


# Executive function
def main(logging):

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-pd', '--post-date', help="The date you want to scan as MM/DD/YYYY")  # Check formatting
    parser.add_argument('-pdr', '--post-date-range', help="Scan the last X days")  # Check formatting
    parser.add_argument('-c', '--county', help="The county you want to scan")
    parser.add_argument('-n', '--notifications', help="Notifications on or off (1 or 0)")
    args = parser.parse_args()

    if args.post_date:
        logging.info("Scanning for reports posted on %s" % args.post_date)
    if args.post_date_range:
        logging.info("Scanning for reports posted in the last %s days" % str(args.post_date_range))
    if args.county:
        logging.info("Scanning for reports in %s" % args.county)
    if args.notifications:
        notifications = int(args.notifications)
        if notifications == 1:
            logging.info("Notifications ENABLED")
        elif notifications == 0:
            logging.info("Notifications DISABLED")
        else:
            logging.info("Unknown notifications setting")
            time.sleep(3)
    else:
        notifications = 1
        #notifications = 0

    all_counties = {
        '01': 'Adams',
        '02': 'Allen',
        '03': 'Ashland',
        '04': 'Ashtabula',
        '05': 'Athens',
        '06': 'Auglaize',
        '07': 'Belmont',
        '08': 'Brown',
        '09': 'Butler',
        '10': 'Carroll',
        '11': 'Champaign',
        '12': 'Clark',
        '13': 'Clermont',
        '14': 'Clinton',
        '15': 'Columbiana',
        '16': 'Coshocton',
        '17': 'Crawford',
        '18': 'Cuyahoga',
        '19': 'Darke',
        '20': 'Defiance',
        '21': 'Delaware',
        '22': 'Erie',
        '23': 'Fairfield',
        '24': 'Fayette',
        '25': 'Franklin',
        '26': 'Fulton',
        '27': 'Gallia',
        '28': 'Geauga',
        '29': 'Greene',
        '30': 'Guernsey',
        '31': 'Hamilton',
        '32': 'Hancock',
        '33': 'Hardin',
        '34': 'Harrison',
        '35': 'Henry',
        '36': 'Highland',
        '37': 'Hocking',
        '38': 'Holmes',
        '39': 'Huron',
        '40': 'Jackson',
        '41': 'Jefferson',
        '42': 'Knox',
        '43': 'Lake',
        '44': 'Lawrence',
        '45': 'Licking',
        '46': 'Logan',
        '47': 'Lorain',
        '48': 'Lucas',
        '49': 'Madison',
        '50': 'Mahoning',
        '51': 'Marion',
        '52': 'Medina',
        '53': 'Meigs',
        '54': 'Mercer',
        '55': 'Miami',
        '56': 'Monroe',
        '57': 'Montgomery',
        '58': 'Morgan',
        '59': 'Morrow',
        '60': 'Muskingum',
        '61': 'Noble',
        '62': 'Ottawa',
        '63': 'Paulding',
        '64': 'Perry',
        '65': 'Pickaway',
        '66': 'Pike',
        '67': 'Portage',
        '68': 'Preble',
        '69': 'Putnam',
        '70': 'Richland',
        '71': 'Ross',
        '72': 'Sandusky',
        '73': 'Scioto',
        '74': 'Seneca',
        '75': 'Shelby',
        '76': 'Stark',
        '77': 'Summit',
        '78': 'Trumbull',
        '79': 'Tuscarawas',
        '80': 'Union',
        '81': 'Van Wert',
        '82': 'Vinton',
        '83': 'Warren',
        '84': 'Washington',
        '85': 'Wayne',
        '86': 'Williams',
        '87': 'Wood',
        '88': 'Wyandot'
    }

    # Counties of the largest cities in Ohio
    # Columbus, Cleveland, Cincinnati, Toledo, Akron, Dayton, Canton, Lorain, Hamilton, Youngstown
    largest_county_list = {
        '09': 'Butler',
        '13': 'Clermont',
        '18': 'Cuyahoga',
        '25': 'Franklin',
        '31': 'Hamilton',
        '47': 'Lorain',
        '48': 'Lucas',
        '50': 'Mahoning',
        '57': 'Montgomery',
        '76': 'Stark',
        '77': 'Summit',
        '78': 'Trumbull'
    }

    if args.county:
        print('*crickets*')

    for cid, county in all_counties.items():

        # Enter crash add date
        if args.post_date:
            date_range = [args.post_date]
        else:
            date_range = [datetime.now().strftime('%m/%d/%Y')]

        # Date range previous
        if args.post_date_range:
            num_days_previous = int(args.post_date_range)
            today = datetime.now()
            date_range = []
            for i in reversed(range(num_days_previous)):
                the_day = today - timedelta(days=i+1)
                date_range.append(the_day.strftime('%m/%d/%Y'))
            date_range.append(today.strftime('%m/%d/%Y'))

        for date in date_range:
            print('\n\n-------------------------------------------------------\n\n')
            
            # Clock into work
            start_time = time.time()
            logging.info('Worker node started working.')

            # Get main page
            logging.info('Getting target')
            target = 'https://services.dps.ohio.gov/CrashRetrieval/OHCrashRetrieval.aspx'

            try:
                driver
            except NameError:
                print('driver doesnt exist yet')
            else:
                print('quitting driver')
                os.system("killall -9 phantomjs");
                try:
                    driver.quit()
                except:
                    os.system("killall -9 phantomjs");

            # Start up browser
            driver = start_driver()

            while True:
                try:
                    driver.get(target)
                except:
                    print('Connection error! Restarting driver')
                    os.system("killall -9 phantomjs");
                    try:
                        driver.quit()
                    except:
                        os.system("killall -9 phantomjs");
                    driver = start_driver()
                else:
                    break

            if not verify_page_loaded_by_id(driver, 'main_cboCounty'):
                logging.error('Something screwy is happening')
                continue

            logging.info("Selecting %s (%s) from dropdown, waiting for __doPostBack().", county, cid)
            input_county = Select(driver.find_element_by_id("main_cboCounty"))
            input_county.select_by_value(str(cid))
            if not verify_page_loaded_by_id(driver, 'main_txtCrashAddDate'):
                logging.error('Something screwy is happening')
                continue


            logging.info("Entering crash add date %s.", date)
            input_date = driver.find_element_by_id("main_txtCrashAddDate")
            input_date.send_keys(date)
            if not verify_page_loaded_by_id(driver, 'main_txtSpoofText'):
                logging.error('Something screwy is happening')
                continue

            loop = 1
            while loop == 1:

                # Solve CAPTCHA
                logging.info("Solving CAPTCHA.")
                spoof_image = driver.find_element_by_id('main_SpoofImage')
                spoof_image_src = spoof_image.get_attribute("src")
                print(spoof_image_src)
                spoof_value = re.search("rndval=[A-Z0-9]{5}", spoof_image_src)
                spoof_value = spoof_value.group(0)
                spoof_value = spoof_value.replace("rndval=", "")
                logging.info("Solved: %s", spoof_value)
                input_spoof = driver.find_element_by_id("main_txtSpoofText")
                input_spoof.send_keys(spoof_value)

                # Submit form
                logging.info("Submitting form.")
                driver.find_element_by_id("main_btnGetData").click()
                if not verify_page_loaded_by_id(driver, 'main_lblErrorMsg'):
                    logging.error('Something screwy is happening')
                    continue

                if len(driver.find_element_by_id("main_lblErrorMsg").text) > 0:
                    if driver.find_element_by_id("main_lblErrorMsg").text == "Invalid Image Text, Please ReEnter the Image Text.":
                        continue
                    else:
                        logging.error(driver.find_element_by_id("main_lblErrorMsg").text)
                        loop = 0
                        break
                else:
                    break

            if loop == 0:
                continue

            # Get number of reports
            try:
                report_num = driver.find_element_by_id("main_lblTotalCount").text
                logging.info("Reports: %s", str(report_num))
            except Exception as e:
                logging.error('Failed to find reports total. Probably indicates day change @ midnight.')
                logging.error(e)
                continue  # Return to top of loop

            # Get number of pages
            page_num = driver.find_element_by_id("main_lblPageCount").text
            page_count_arr = page_num.split(' ')
            current_page = int(page_count_arr[1])
            num_of_pages = int(page_count_arr[4])
            logging.info("Pages: %s", str(page_num))

            # Iterate through pages
            while current_page <= num_of_pages:
                # Retrieve reports table HTML
                table_html = driver.execute_script('return window.document.getElementById("main_gvCrashInfo").innerHTML')
                soup = BeautifulSoup(table_html, 'html.parser')

                # Parse column names
                table_html_column_names = soup.find_all('th')
                logging.info("Found %d column headings, %d hidden", len(table_html_column_names), 1)

                # Parse all reports
                reports_found = {}
                reports_found_crash_ids = []
                x = soup.find_all('tr')
                logging.info("Found %d reports", len(x))
                # Do this with threads?

                for report in x:
                    if len(report.find_all('th')) == 13:
                        # This is the header row
                        logging.debug('Header row detected.')

                    elif len(report.find_all('td')) == 13:
                        # This is a report
                        logging.debug('Gathering data for report #%d on page %d.', len(reports_found)+1, 1)

                        # Store report data in a dictionary row
                        # This can probably be replaced with something like report_td[0]
                        report_column_num = 0
                        for report_column in report.find_all('td'):

                            # Select Report Link
                            if report_column_num == 0:
                                for a in report_column.find_all('a', href=True):
                                    temp_local_select_report = a['href']
                                    #print(temp_local_select_report)

                                logging.debug('Local report #%s', temp_local_select_report)

                            # Local report number
                            if report_column_num == 1:
                                temp_local_report_num = str(report_column.string)
                                logging.debug('Local report #%s', temp_local_report_num)

                            # Crash Date
                            if report_column_num == 2:
                                temp_crash_date = str(report_column.string)
                                temp_crash_date = str(datetime.strptime(temp_crash_date, "%m/%d/%Y"))
                                temp_crash_date = temp_crash_date.split(' ')[0]  # MySQL format
                                logging.debug('Crash date #%s', temp_crash_date)

                            # "P"
                            if report_column_num == 3:
                                temp_p = str(report_column.string)

                            # Location
                            if report_column_num == 4:
                                temp_location = str(report_column.string)

                            # Law Enforcement
                            if report_column_num == 5:
                                temp_law_enforcement = str(report_column.string)

                            # Jurisdiction
                            if report_column_num == 6:
                                temp_jurisdiction = str(report_column.string)

                            # Severity
                            if report_column_num == 7:
                                temp_severity = str(report_column.string)

                            # Document Number
                            if report_column_num == 8:
                                temp_document_number = str(report_column.string)
                                temp_document_number = temp_document_number.strip()

                            # County Code
                            if report_column_num == 9:
                                temp_county_code = str(report_column.string)

                            # FIPS Code
                            if report_column_num == 10:
                                temp_fips_code = str(report_column.string)

                            # Entered By
                            if report_column_num == 11:
                                temp_entered_by = str(report_column.string)

                            # Crash ID (Hidden)
                            # Store data
                            if report_column_num == 12:
                                temp_crash_id = str(report_column.string)
                                logging.debug('Crash ID #%s', temp_crash_id)

                                logging.debug('Storing data')
                                reports_found_crash_ids.append(temp_crash_id)  # Add report crash id to list
                                reports_found[temp_crash_id] = {
                                    'select_report_link': str(temp_local_select_report),
                                    'unix_timestamp': str(int(time.time())),
                                    'local_report_num': temp_local_report_num,
                                    'crash_date': temp_crash_date,
                                    'p': temp_p,
                                    'location': temp_location,
                                    'law_enforcement': temp_law_enforcement,
                                    'jurisdiction': temp_jurisdiction,
                                    'severity': temp_severity,
                                    'document_number': temp_document_number,
                                    'county_code': temp_county_code,
                                    'fips_code': temp_fips_code,
                                    'entered_by': temp_entered_by,
                                    'crash_id': temp_crash_id
                                }

                            report_column_num = report_column_num + 1

                    elif '<table' in report:
                        # This is the <Prev Next> row
                        logging.info('<Prev Next> row detected.')

                    else:
                        # Unknown
                        logging.warning('Unknown case detected.')

                logging.info('Finished parsing reports.')
                logging.debug(reports_found_crash_ids)

                # Compare old and new reports
                old_reports = get_old_reports()  # queries db. rewrite this so it only queries ish from the last 24/48hrs
                logging.info('Comparing existing reports with reports found.')
                
                new_reports_crash_ids = []
                for report in reports_found_crash_ids:
                    if report not in old_reports:
                        new_reports_crash_ids.append(report)

                logging.info('%d out of %d reports are new.', len(new_reports_crash_ids), len(reports_found_crash_ids))

                if len(new_reports_crash_ids) != 0:
                    # Segregate new report data
                    new_reports_list = []
                    new_reports_dict = {}
                    for crash_id, report_data in reports_found.items():
                        if crash_id in new_reports_crash_ids:
                            new_reports_dict[crash_id] = report_data
                            new_reports_list.append(report_data)

                    # Schedule new reports to be downloaded and insert available data
                    logging.info('Scheduling %d new report(s) to be downloaded.', len(new_reports_crash_ids))
                    date_arr = date.split("/")
                    month = date_arr[0]
                    day = date_arr[1]
                    year = date_arr[2]

                    # Set file path
                    file_path = "reports/%s/%s/%s" % (year, month, day)
                    os.makedirs(file_path, exist_ok=True) # Create path if it doesn't exist

                    # Determine threads
                    if len(new_reports_list) >= 10:
                        num_threads = 10
                    else:
                        num_threads = len(new_reports_list)

                    # Download reports using multiprocessing
                    # Note: Website changed so we can no longer do it fast like this :(
                    #with Pool(processes=num_threads) as pool:
                    #    logging.info('Downloading %s files' % len(new_reports_list))
                    #    reports_processed = pool.starmap(download_reports, zip(new_reports_list, repeat(file_path)))  # Returns a list [crash_id, digital_file_path, scanned_file_path]
                    #    logging.info('Reports processed length = %d' % len(reports_processed))

                    reports_processed = []

                    # Enter into pages and download reports one by one
                    for report in new_reports_list:
                        try:
                            driver.find_element_by_xpath('//a[@href="' + report['select_report_link'] + '"]').click()
                        except:
                            print('Cant find %s' % report['select_report_link'])
                            continue

                        if verify_page_loaded_by_id(driver, 'Footer'):
                            if not verify_page_loaded_by_id(driver, 'main_frame1'):
                                if not verify_page_loaded_by_id(driver, 'main_Frame1'):
                                    logging.error('main_frame1 isnt behaving itself')
                                    while True:
                                        try:
                                            driver.get(target)
                                        except:
                                            print('Connection error! Restarting driver')
                                            driver = start_driver()
                                        else:
                                            break
                                    continue

                            iframe = driver.find_element_by_id('main_frame1')
                            iframe_src = iframe.get_attribute("src")
                            pdf_src = iframe_src.replace('Wait.aspx?redirectPage=ViewCrashReport.aspx&', 'ViewCrashReport.aspx?')

                            if 'DocNumber' in pdf_src:
                                report_type = 'scanned'

                            if 'CrashId' in pdf_src:
                                report_type = 'digital'

                            if not report_type:
                                report_type = 'unknown'

                            report_processed = download_reports(report, file_path, pdf_src, report_type)
                            reports_processed.append(report_processed)

                            driver.find_element_by_id('main_btnReturnHome').click()
                            if not verify_page_loaded_by_id(driver, 'Footer'):
                                print('Couldnt return to home!')
                            else:
                                print('Returned to home')



                    # Add file locations to new reports dictionary
                    for report in reports_processed:
                        crash_id = report[0]
                        digital_file_path = report[1]
                        scanned_file_path = report[2]
                        new_reports_dict[crash_id]['digital_file_path'] = digital_file_path
                        new_reports_dict[crash_id]['scanned_file_path'] = scanned_file_path


                    # Prob do OCR here igggg
                    with Pool(processes=num_threads) as pool:
                        logging.info('OCR\'ing %s files' % len(new_reports_list))
                        digital_reports = [item[1] for item in reports_processed]
                        digital_reports = [x for x in digital_reports if x != False]
                        reports_ocrd = pool.starmap(run_tet, zip(digital_reports, repeat(file_path)))  # Returns a list [pdf_file_path, xml_file_path]
                        logging.info('%d Reports processed' % len(reports_ocrd))

                    # Get structured information from XML
                    structured_report_data = []
                    for report in reports_ocrd:
                        if report != False:
                            xml_file_location = report[1]
                            results = get_xml_info(xml_file_location)
                            if results != False:
                                #Add results to data object
                                structured_report_data.append(results)

                    # Attach structured data to existing new_reports_dict
                    for report in structured_report_data:
                        crash_id = str(report['crash_id'])
                        unit_at_fault = str(report['unit_at_fault'])
                        if crash_id in new_reports_dict:
                            
                            # Iterate through units
                            new_reports_dict[crash_id]['unit'] = {}
                            for unit_num, field_name in report['unit'].items():
                                # Iterate through fieldsl
                                new_reports_dict[crash_id]['unit'][unit_num] = {}
                                for field_name, field_value in report['unit'][unit_num].items():
                                    new_reports_dict[crash_id]['unit'][unit_num][field_name] = field_value
                            
                            # Iterate through people
                            new_reports_dict[crash_id]['person'] = {}
                            new_reports_dict[crash_id]['unit_at_fault'] = unit_at_fault
                            for person_num, field_name in report['person'].items():
                                # Iterate through fieldsl
                                new_reports_dict[crash_id]['person'][person_num] = {}
                                for field_name, field_value in report['person'][person_num].items():
                                    new_reports_dict[crash_id]['person'][person_num][field_name] = field_value


                    # Record, parse, notify
                    for crash_id, crash_data in new_reports_dict.items():
                        #if crash_data['scanned_file_path'] != '' and crash_data['scanned_file_path'] != 'ERROR':
                        # Store data
                        row_id = store_report_data(crash_data)
                        store_unit_data(crash_data, row_id)
                        store_person_data(crash_data, row_id)

                        if notifications == 1:
                            # Parse report data
                            email_html = build_email(row_id)

                            # Notify users
                            notify_via_email(email_html, crash_id, row_id, crash_data['crash_date'], crash_data['scanned_file_path'], cid)
                        else:
                            logging.info('Skipping notification step')


                # Zero reports out
                reports_found.clear()
                reports_found_crash_ids.clear()

                # Determine if there's another page
                if current_page < num_of_pages:
                    if verify_page_loaded_by_partial_link_text(driver, "Next") == False:
                        break
                    # There is another page. Click "Next>"
                    logging.info("Clicking to next page")
                    driver.find_element_by_partial_link_text("Next").click()
                    verify_page_loaded_by_partial_link_text(driver, "Prev")
                    current_page = current_page + 1
                else:
                    # There are no other pages
                    logging.info("Done scanning all pages.")
                    break

            # Clock out of work
            end_time = time.time()
            logging.info('Worker node stopped working.')

            logging.info('Scanned county in %s seconds\n', end_time - start_time)

            # Only allow worker to run once every `run_every` seconds
            time_diff = int(end_time - start_time)
            run_every = 5  # seconds
            if time_diff <= run_every:
                time_diff = int(time.time() - start_time)  # time elapsed since time started
                time_to_sleep = run_every - time_diff  # time to sleep
                logging.info('Sleeping for %s seconds...', time_to_sleep)
                time.sleep(time_to_sleep)  # sleep

    # Shutting down worker
    # Put this outside of main?
    logging.info('Shutting down WebDriver')
    try:
        driver.service.process.send_signal(signal.SIGTERM)
        os.system("killall -9 phantomjs");
        try:
            driver.quit()
        except:
            os.system("killall -9 phantomjs");
        logging.info('WebDriver shut down normally.')
    except:
        logging.warning('WebDriver failed to shut down normally!')


# Run main() indefinitely if executed directly by cl-slave
if __name__ == "__main__":
    print('')

    # Configure logging
    # level = DEBUG; INFO; WARNING
    # format = "[2017-03-25 07:54:36 PM] is when this event was logged"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='[%Y/%m/%d %I:%M:%S %p]')

    # Executive function
    main(logging)

