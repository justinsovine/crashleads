#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# Intellect37, LLC 2017 #
# # # # # # # # # # # # #

import re
from bs4 import BeautifulSoup
import getpass
#import logging
import time  # Resolve this? Convert time -> datetime
from datetime import datetime, timedelta
import os
import sys
import argparse
import pprint
import signal

# browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# custom modules
from modules.database import DatabaseModel

# Wait for page to load by searching for presence of element
def verify_page_loaded_by_id(driver, element_id, time_to_wait=10):
    try:
        WebDriverWait(driver, time_to_wait).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        #print("Page loaded.")
        return True
    except:
        print('Page timed out!')
        return False


def verify_page_loaded_by_partial_link_text(driver, partial_text, time_to_wait=10):
    try:
        WebDriverWait(driver, time_to_wait).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, partial_text))
        )
        #print("Page loaded.")
        return True
    except:
        print('Page timed out!')
        return False

def start_browser():
    driver = webdriver.PhantomJS()
    driver.set_window_size(1366, 768)
    print("\n\nStarted WebDriver => PhantomJS")
    return driver

def main():

    counties = {
        '13': 'Clermont',
        '25': 'Franklin',
        '31': 'Hamilton'
    }

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

    print("Initializing database model")
    dbmodel = DatabaseModel()

    print('Getting list of old report ids')
    old_reports_ids = dbmodel.select_all_report_ids()

    todays_date = [datetime.now().strftime('%m/%d/%Y')]
    for cid, county_name in largest_county_list.items():
        
        # Ensures the program will keep trying to scan the same county until done correctly
        while True:
            target = 'https://services.dps.ohio.gov/CrashRetrieval/OHCrashRetrieval.aspx'
            try:
                driver = start_browser()
                driver.get(target)
            except Exception as ex:
                print(ex)
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("[%s] %s" % (cid, county_name))
            print("Selecting county from dropdown, waiting for __doPostBack().")
            try:
                input_county = Select(driver.find_element_by_id("main_cboCounty"))
                input_county.select_by_value(str(cid))
            except Exception as ex:
                print(ex)
                print('Error selecting a county from the dropdown! Restarting...')
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Verifying page loaded correctly after selecting the county dropdown")
            if not verify_page_loaded_by_id(driver, 'main_txtCrashAddDate'):
                print('Page was not loaded correctly! Restarting...')
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
            
            print("Entering crash add date %s." % todays_date)
            try:
                input_date = driver.find_element_by_id("main_txtCrashAddDate")
            except Exception as ex:
                print(ex)
                print("Error selecting the crash add date field! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            try:
                input_date.send_keys(todays_date)
            except Exception as ex:
                print(ex)
                print("Error typing in the crash add date field! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Verifying the spoof image field is there")
            if not verify_page_loaded_by_id(driver, 'main_txtSpoofText'):
                print("Could not find the spoof image field! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Selecting spoof image...")
            try:
                spoof_image = driver.find_element_by_id('main_SpoofImage')
                spoof_image_src = spoof_image.get_attribute("src")
            except Exception as ex:
                print(ex)
                print("Error selecting the spoof image field! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print('Scraping spoof text from spoof image: %s' % spoof_image_src)
            try:
                spoof_value = re.search("rndval=[A-Z0-9]{5}", spoof_image_src)
            except Exception as ex:
                print(ex)
                print("Could not solve spoof image! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
            else:
                spoof_value = spoof_value.group(0)
                spoof_value = spoof_value.replace("rndval=", "")
                print("Solved spoof image: %s" % spoof_value)

            print("Selecting spoof field")
            try:
                input_spoof = driver.find_element_by_id("main_txtSpoofText")
            except Exception as ex:
                print(ex)
                print("There was a problem selecting the spoof field! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Entering solution into spoof field")
            try:
                input_spoof.send_keys(spoof_value)
            except Exception as ex:
                print(ex)
                print("There was a problem when entering the solution! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Submitting form")
            try:
                driver.find_element_by_id("main_btnGetData").click()
            except Exception as ex:
                print(ex)
                print("There was a problem when submitting the form! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over


            print("Looking for main_lblErrorMsg")
            if not verify_page_loaded_by_id(driver, 'main_lblErrorMsg'):
                print("Could not find main_lblErrorMsg! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over

            print("Checking main_lblErrorMsg")
            if len(driver.find_element_by_id("main_lblErrorMsg").text) > 0:
                if driver.find_element_by_id("main_lblErrorMsg").text == "Invalid Image Text, Please ReEnter the Image Text.":
                    print("Invalid spoof image solution! Restarting...")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        continue
                    time.sleep(1)
                    continue  # back to the top of the loop to start over
                else:
                    print(driver.find_element_by_id("main_lblErrorMsg").text)
                    print("Unknown error message! Restarting...")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over

            # Get number of reports
            try:
                report_num = driver.find_element_by_id("main_lblTotalCount").text
            except Exception as ex:
                print(ex)
                print("Failed to find reports total. Probably indicates day change @ midnight! Restarting...")
                print("Restarting and continuing to next county...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                break  # NEXT COUNTY
            else:
                print("Total Reports: %s" % str(report_num))

            # Get number of pages
            try:
                page_num = driver.find_element_by_id("main_lblPageCount").text
            except Exception as ex:
                print(ex)
                print("Couldn't find page count! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
            else:
                page_count_arr = page_num.split(' ')
                current_page = int(page_count_arr[1])
                num_of_pages = int(page_count_arr[4])
                print("Number of Pages: %s" % str(page_num))

            # Iterate through pages
            #while current_page <= num_of_pages:

            # Retrieve reports table HTML
            print('Retrieving reports table HTML')
            try:
                table_html = driver.execute_script('return window.document.getElementById("main_gvCrashInfo").innerHTML')
            except Exception as ex:
                print(ex)
                print("Couldn't retrieve reports table HTML! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
                ##########################################################################################
                ######################### will be a problem with multi page###############################
                ##########################################################################################
            else:
                soup = BeautifulSoup(table_html, 'html.parser')

            # Parse column names
            print('Parsing column names')
            try:
                table_html_column_names = soup.find_all('th')
            except Exception as ex:
                print(ex)
                print("Couldn't parse column names! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
                ##########################################################################################
                ######################### will be a problem with multi page###############################
                ##########################################################################################
            else:
                print("Found %d column headings, %d hidden" % (len(table_html_column_names), 1))

            # Parse all reports
            print('Parsing reports')
            try:
                x = soup.find_all('tr')
            except Exception as ex:
                print(ex)
                print("Couldn't parse reports! Restarting...")
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
                    continue
                time.sleep(1)
                continue  # back to the top of the loop to start over
                ##########################################################################################
                ######################### will be a problem with multi page###############################
                ##########################################################################################
            else:
                num_reports_found = str(len(x)-1)
                print("Found %s reports" % num_reports_found)

            scanned_reports = {}
            scanned_reports_ids = []
            for report in x:
                if len(report.find_all('th')) == 13:
                    # This is the header row
                    print('Header row detected.')

                elif len(report.find_all('td')) == 13:
                    # This is a report
                    #print('Gathering data for report #%d on page %d.' % ( len(scanned_reports_ids)+1, 1))

                    # Store report data in a dictionary row
                    # This can probably be replaced with something like report_td[0]
                    report_column_num = 0
                    for report_column in report.find_all('td'):

                        # Select Report Link
                        if report_column_num == 0:
                            for a in report_column.find_all('a', href=True):
                                temp_local_select_report = a['href']
                                #print(temp_local_select_report)

                            #print('Local report #%s' % temp_local_select_report)

                        # Local report number
                        if report_column_num == 1:
                            temp_local_report_num = str(report_column.string)
                            #print('Local report #%s' % temp_local_report_num)

                        # Crash Date
                        if report_column_num == 2:
                            temp_crash_date = str(report_column.string)
                            temp_crash_date = str(datetime.strptime(temp_crash_date, "%m/%d/%Y"))
                            temp_crash_date = temp_crash_date.split(' ')[0]  # MySQL format
                            #print('Crash date #%s' % temp_crash_date)

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
                            #print('Crash ID #%s' % temp_crash_id)

                            #print('Storing data')
                            scanned_reports_ids.append(temp_crash_id)  # Add report crash id to list
                            scanned_reports[temp_crash_id] = {
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
                                'crash_id': temp_crash_id,
                                'digital_external_link': '',
                                'scanned_external_link': ''
                            }

                        report_column_num = report_column_num + 1

                elif '<table' in report:
                    # This is the <Prev Next> row
                    print('<Prev Next> row detected.')

                else:
                    # Unknown
                    print('Unknown case detected.')
                    #print(report)

            print('Finished parsing %d reports' % len(scanned_reports_ids))

            print("Comparing old reports with scanned reports")
            new_reports = {}
            new_reports_ids = []
            for report_id in scanned_reports_ids:
                if report_id not in old_reports_ids:
                    new_reports_ids.append(report_id)
                    new_reports[report_id] = scanned_reports[report_id]

            print("Found a total of %d new reports!" % len(new_reports_ids))

            # Enter into pages and download reports one by one
            for report in new_reports.items():
                report_list = list(report)
                crash_id = report_list[0];
                report_data = dict(report_list[1])

                print('\nClicking show report link for #%s' % crash_id)
                try:
                    driver.find_element_by_xpath('//a[@href="' + report_data['select_report_link'] + '"]').click()
                except Exception as ex:
                    print(ex)
                    print("Couldn't click show report link! Restarting...")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over

                print("Verifying page loaded correctly")
                if verify_page_loaded_by_id(driver, 'Footer'):
                    if not verify_page_loaded_by_id(driver, 'main_frame1'):
                        if not verify_page_loaded_by_id(driver, 'main_Frame1'):
                            print('main_frame1 isnt behaving itself! Restarting...')
                            driver.service.process.send_signal(signal.SIGTERM)
                            try:
                                driver.quit()
                            except OSError as ex:
                                print(ex)
                                print('BAD FILE DESCRIPTOR! Restarting...')
                                break
                            time.sleep(1)
                            break  # back to the top of the loop to start over
                else:
                    print('main_frame1 isnt behaving itself! Restarting...')
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over


                print("Selecting main_frame1")
                try:
                    iframe = driver.find_element_by_id('main_frame1')
                except Exception as ex:
                    print(ex)
                    print("Couldn't select main_frame1! Restarting...")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over

                iframe_src = iframe.get_attribute("src")
                pdf_src = iframe_src.replace('Wait.aspx?redirectPage=ViewCrashReport.aspx&', 'ViewCrashReport.aspx?')

                if 'DocNumber' in pdf_src:
                    report_type = 'scanned'
                    new_reports[report_data['crash_id']]['scanned_external_link'] = pdf_src

                if 'CrashId' in pdf_src:
                    report_type = 'digital'
                    new_reports[report_data['crash_id']]['digital_external_link'] = pdf_src

                if not report_type:
                    report_type = 'unknown'

                if not dbmodel.insert_report_data(new_reports[report_data['crash_id']]):
                    print("There was a problem inserting basic report data")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        sys.exit()
                    time.sleep(1)
                    sys.exit()

                print('Returning to home page')
                try:
                    driver.find_element_by_id('main_btnReturnHome').click()
                except Exception as ex:
                    print(ex)
                    print("Couldn't click to return home! Restarting...")
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over

                print("Verifying home page loaded correctly")
                if not verify_page_loaded_by_id(driver, 'Footer'):
                    print('Couldnt return to home! Restarting...')
                    driver.service.process.send_signal(signal.SIGTERM)
                    try:
                        driver.quit()
                    except OSError as ex:
                        print(ex)
                        print('BAD FILE DESCRIPTOR! Restarting...')
                        break
                    time.sleep(1)
                    break  # back to the top of the loop to start over
            
            # # # # # # # # # # # # # # # #
            # Browser shutdown. Next county
            # # # # # # # # # # # # # # # #
            print('Shutting down browser and starting next county...')
            try:
                driver
            except Exception as ex:
                print(ex)
                print('Driver doesnt exist! Restarting...')
                break
            else:
                driver.service.process.send_signal(signal.SIGTERM)
                try:
                    driver.quit()
                except OSError as ex:
                    print(ex)
                    print('BAD FILE DESCRIPTOR! Restarting...')
            finally:
                time.sleep(1)
                break  # NEXT COUNTY

if __name__ == "__main__":
    while True:
        main()