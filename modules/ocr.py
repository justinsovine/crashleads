#!/usr/bin/env python3

import os
import sys
from subprocess import call
import time
import xml.etree.ElementTree as ET
import logging
import re


def get_xml_info(xml_file_location):

    # Check if file exists
    if not os.path.exists(xml_file_location):
        # TET thinks this is too big or too many pages or errored for some reason
        # This is honestly a missed good lead. Use this as an opportunity to split the PDF
        logging.debug('TET didn\'t scan this PDF because it was too big, had too many pages, or had an unknown error...')
        return False

    try:
        # TET makes some dumb XML format that doesn't work right so removing their xmlns
        f = open(xml_file_location, "r+")
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i == '<TET xmlns="http://www.pdflib.com/XML/TET5/TET-5.0"\n':
                logging.info('Replacing TET\'s XMLNS')
                ii = i.replace('http://www.pdflib.com/XML/TET5/TET-5.0', '')
                f.write(ii)
            else:
                f.write(i)
        f.truncate()
        f.close()
    except:
        return False

    try:
        logging.debug('Scanning %s' % xml_file_location)
        tree = ET.parse(xml_file_location)
        root = tree.getroot()
    except:
        return False

    report_object = {}

    # Get crash id. This is super stupid
    filename = xml_file_location.split('/')
    filename = filename[-1]
    crash_id = int(re.search(r'\d+', filename).group())
    report_object['crash_id'] = crash_id
    report_object['unit_at_fault'] = ''

    report_object['unit'] = {}
    report_object['unit']['1'] = {}
    report_object['unit']['2'] = {}
    report_object['unit']['3'] = {}
    report_object['unit']['4'] = {}
    #report_object['unit']['5'] = {}
    #report_object['unit']['6'] = {}
    #report_object['unit']['7'] = {}
    #report_object['unit']['8'] = {}

    report_object['person'] = {}
    report_object['person']['1'] = {}
    report_object['person']['2'] = {}
    report_object['person']['3'] = {}
    report_object['person']['4'] = {}
    report_object['person']['5'] = {}
    report_object['person']['6'] = {}
    report_object['person']['7'] = {}
    report_object['person']['8'] = {}

    unit_i = 1;

    # Initialize Person #1
    report_object['unit']['1']['unit_number'] = ''
    report_object['unit']['1']['insurance'] = ''

    # Initialize Person #2
    report_object['unit']['2']['unit_number'] = ''
    report_object['unit']['2']['insurance'] = ''

    # Initialize Person #3
    report_object['unit']['3']['unit_number'] = ''
    report_object['unit']['3']['insurance'] = ''

    # Initialize Person #4
    report_object['unit']['4']['unit_number'] = ''
    report_object['unit']['4']['insurance'] = ''

    # Initialize Person #1
    report_object['person']['1']['unit_number'] = ''
    report_object['person']['1']['full_name'] = ''
    report_object['person']['1']['first_name'] = ''
    report_object['person']['1']['middle_name'] = ''
    report_object['person']['1']['last_name'] = ''
    report_object['person']['1']['dob'] = ''
    report_object['person']['1']['age'] = ''
    report_object['person']['1']['gender'] = ''
    report_object['person']['1']['address'] = ''
    report_object['person']['1']['zip'] = ''
    report_object['person']['1']['injuries'] = ''
    report_object['person']['1']['offense_charged'] = ''
    report_object['person']['1']['offense_description'] = ''
    report_object['person']['1']['citation_number'] = ''
    report_object['person']['1']['phone'] = ''
    report_object['person']['1']['air_bag'] = ''

    # Initialize Person #2
    report_object['person']['2']['unit_number'] = ''
    report_object['person']['2']['full_name'] = ''
    report_object['person']['2']['first_name'] = ''
    report_object['person']['2']['middle_name'] = ''
    report_object['person']['2']['last_name'] = ''
    report_object['person']['2']['dob'] = ''
    report_object['person']['2']['age'] = ''
    report_object['person']['2']['gender'] = ''
    report_object['person']['2']['address'] = ''
    report_object['person']['2']['zip'] = ''
    report_object['person']['2']['injuries'] = ''
    report_object['person']['2']['offense_charged'] = ''
    report_object['person']['2']['offense_description'] = ''
    report_object['person']['2']['citation_number'] = ''
    report_object['person']['2']['phone'] = ''
    report_object['person']['2']['air_bag'] = ''

    # Initialize Person #3
    report_object['person']['3']['unit_number'] = ''
    report_object['person']['3']['full_name'] = ''
    report_object['person']['3']['first_name'] = ''
    report_object['person']['3']['middle_name'] = ''
    report_object['person']['3']['last_name'] = ''
    report_object['person']['3']['dob'] = ''
    report_object['person']['3']['age'] = ''
    report_object['person']['3']['gender'] = ''
    report_object['person']['3']['address'] = ''
    report_object['person']['3']['zip'] = ''
    report_object['person']['3']['injuries'] = ''
    report_object['person']['3']['offense_charged'] = ''
    report_object['person']['3']['offense_description'] = ''
    report_object['person']['3']['citation_number'] = ''
    report_object['person']['3']['phone'] = ''
    report_object['person']['3']['air_bag'] = ''

    # Initialize Person #4
    report_object['person']['4']['unit_number'] = ''
    report_object['person']['4']['full_name'] = ''
    report_object['person']['4']['first_name'] = ''
    report_object['person']['4']['middle_name'] = ''
    report_object['person']['4']['last_name'] = ''
    report_object['person']['4']['dob'] = ''
    report_object['person']['4']['age'] = ''
    report_object['person']['4']['gender'] = ''
    report_object['person']['4']['address'] = ''
    report_object['person']['4']['zip'] = ''
    report_object['person']['4']['injuries'] = ''
    report_object['person']['4']['offense_charged'] = ''
    report_object['person']['4']['offense_description'] = ''
    report_object['person']['4']['citation_number'] = ''
    report_object['person']['4']['phone'] = ''
    report_object['person']['4']['air_bag'] = ''

    # Initialize Person #1_v2
    report_object['person']['5']['unit_number'] = ''
    report_object['person']['5']['full_name'] = ''
    report_object['person']['5']['first_name'] = ''
    report_object['person']['5']['middle_name'] = ''
    report_object['person']['5']['last_name'] = ''
    report_object['person']['5']['dob'] = ''
    report_object['person']['5']['age'] = ''
    report_object['person']['5']['gender'] = ''
    report_object['person']['5']['address'] = ''
    report_object['person']['5']['zip'] = ''
    report_object['person']['5']['injuries'] = ''
    report_object['person']['5']['offense_charged'] = ''
    report_object['person']['5']['offense_description'] = ''
    report_object['person']['5']['citation_number'] = ''
    report_object['person']['5']['phone'] = ''
    report_object['person']['5']['air_bag'] = ''

    # Initialize Person #2_v2
    report_object['person']['6']['unit_number'] = ''
    report_object['person']['6']['full_name'] = ''
    report_object['person']['6']['first_name'] = ''
    report_object['person']['6']['middle_name'] = ''
    report_object['person']['6']['last_name'] = ''
    report_object['person']['6']['dob'] = ''
    report_object['person']['6']['age'] = ''
    report_object['person']['6']['gender'] = ''
    report_object['person']['6']['address'] = ''
    report_object['person']['6']['zip'] = ''
    report_object['person']['6']['injuries'] = ''
    report_object['person']['6']['offense_charged'] = ''
    report_object['person']['6']['offense_description'] = ''
    report_object['person']['6']['citation_number'] = ''
    report_object['person']['6']['phone'] = ''
    report_object['person']['6']['air_bag'] = ''

    # Initialize Person #3_v2
    report_object['person']['7']['unit_number'] = ''
    report_object['person']['7']['full_name'] = ''
    report_object['person']['7']['first_name'] = ''
    report_object['person']['7']['middle_name'] = ''
    report_object['person']['7']['last_name'] = ''
    report_object['person']['7']['dob'] = ''
    report_object['person']['7']['age'] = ''
    report_object['person']['7']['gender'] = ''
    report_object['person']['7']['address'] = ''
    report_object['person']['7']['zip'] = ''
    report_object['person']['7']['injuries'] = ''
    report_object['person']['7']['offense_charged'] = ''
    report_object['person']['7']['offense_description'] = ''
    report_object['person']['7']['citation_number'] = ''
    report_object['person']['7']['phone'] = ''
    report_object['person']['7']['air_bag'] = ''

    # Initialize Person #4_v2
    report_object['person']['8']['unit_number'] = ''
    report_object['person']['8']['full_name'] = ''
    report_object['person']['8']['first_name'] = ''
    report_object['person']['8']['middle_name'] = ''
    report_object['person']['8']['last_name'] = ''
    report_object['person']['8']['dob'] = ''
    report_object['person']['8']['age'] = ''
    report_object['person']['8']['gender'] = ''
    report_object['person']['8']['address'] = ''
    report_object['person']['8']['zip'] = ''
    report_object['person']['8']['injuries'] = ''
    report_object['person']['8']['offense_charged'] = ''
    report_object['person']['8']['offense_description'] = ''
    report_object['person']['8']['citation_number'] = ''
    report_object['person']['8']['phone'] = ''
    report_object['person']['8']['air_bag'] = ''

    try:
        for box in root.iter('Box'):
            # Get <Line></Line>'s in <Box ...>
            # This is for the above methods
            #box_lines = box.iter('Line')

            # Get coordinates
            llx = box.get('llx')
            lly = box.get('lly')
            #urx = box.get('urx')
            #ury = box.get('ury')

            # Get Report Data
            # Unit at Fault
            if llx == "520.78" and lly == "694.66":
                for line in box.iter('Line'):
                    unit_at_fault = line.find('Text').text
                    report_object['unit_at_fault'] = unit_at_fault
                    logging.debug('Unit at Fault: %s' % unit_at_fault)

            # Unit #1 Insurance
            # llx="83.09" lly="608.33"
            if llx == "83.09" and lly == "608.33":
                for line in box.iter('Line'):
                    unit_1_insurance = line.find('Text').text
                    report_object['unit']['1']['insurance'] = unit_1_insurance
                    logging.debug('[U1] Insurance: %s' % unit_1_insurance)

            # Unit #2 Insurance
            # llx="83.09" lly="608.33"
            if llx == "83.09" and lly == "608.33":
                for line in box.iter('Line'):
                    if unit_i == 1:
                        report_object['unit']['1']['unit_number'] = unit_i
                        unit_1_insurance = line.find('Text').text
                        report_object['unit']['1']['insurance'] = unit_1_insurance
                        logging.info('[U1] Insurance: %s' % unit_1_insurance)
                        #testt = input('Press key. ')
                        unit_i = 2
                    elif unit_i == 2:
                        report_object['unit']['2']['unit_number'] = unit_i
                        unit_2_insurance = line.find('Text').text
                        report_object['unit']['2']['insurance'] = unit_2_insurance
                        logging.info('[U2] Insurance: %s' % unit_2_insurance)
                        #testt = input('Press key. ')
                        unit_i = 3
                    elif unit_i == 3:
                        report_object['unit']['3']['unit_number'] = unit_i
                        unit_3_insurance = line.find('Text').text
                        report_object['unit']['3']['insurance'] = unit_3_insurance
                        logging.info('[U3] Insurance: %s' % unit_3_insurance)
                        #testt = input('Press key. ')
                        unit_i = 4
                    elif unit_i == 4:
                        report_object['unit']['4']['unit_number'] = unit_i
                        unit_4_insurance = line.find('Text').text
                        report_object['unit']['4']['insurance'] = unit_4_insurance
                        logging.info('[U4] Insurance: %s' % unit_4_insurance)
                        #testt = input('Press key. ')
                        unit_i = 5


            # PERSON #1 - MOTORIST / NON-MOTORIST / OCCUPANT V1 (Scanned lower on 1st page)
            #
            # Unit Number  <Box llx="40.32"  lly="703.01" urx="44.77"  ury="711.01">
            # Name         <Box llx="34.27"  lly="664.49" urx="124.06" ury="672.49">
            # DOB          <Box llx="385.63" lly="664.56" urx="425.64" ury="672.56">
            # Age          <Box llx="485.42" lly="664.56" urx="494.32" ury="672.56">
            # Gender       <Box llx="518.26" lly="668.59" urx="524.36" ury="678.59">
            # Address      <Box llx="34.27"  lly="639.07" urx="173.98" ury="647.07">
            # Phone        <Box llx="423.43" lly="639.07" urx="473.23" ury="647.07">
            # Injuries/EMS ?
            # Injuries     <Box llx="39.82"  lly="615.02" urx="45.38"  ury="625.02">
            # Air Bag      <Box llx="486.14" lly="615.02" urx="491.70" ury="625.02">
            # Offense Crgd <Box llx="35.64"  lly="558.72" urx="60.09"  ury="566.72">
            # Offense Desc <Box llx="151.27" lly="559.58" urx="226.21" ury="567.58">
            # Citation Num <Box llx="357.05" lly="558.72" urx="392.63" ury="566.72">

            # Person #1 Unit Number & Name
            # Only like this on MNmO page
            if llx == "34.27" and lly == "664.49":
                logging.debug('\nPerson #1')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')
                    person_1_unit_number = blah[0][:1]
                    report_object['person']['1']['unit_number'] = person_1_unit_number
                    logging.debug('[P1] Unit Number: %s' % person_1_unit_number)

                    if len(blah) == 3:
                        person_1_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['1']['full_name'] = person_1_full_name
                        logging.debug('[P1] Full Name: %s' % person_1_full_name)
                        person_1_first_name = blah[1].strip()
                        report_object['person']['1']['first_name'] = person_1_first_name
                        logging.debug('[P1] First Name: %s' % person_1_first_name)
                        person_1_middle_name = blah[2].strip()
                        report_object['person']['1']['middle_name'] = person_1_middle_name
                        logging.debug('[P1] Middle Name: %s' % person_1_middle_name)
                        person_1_last_name = blah[0][2:]
                        report_object['person']['1']['last_name'] = person_1_last_name
                        logging.debug('[P1] Last Name: %s' % person_1_last_name)
                    elif len(blah) == 2:
                        person_1_full_name = blah[0][2:] + ',' + blah[1]
                        report_object['person']['1']['full_name'] = person_1_full_name
                        logging.debug('[P1] Full Name: %s' % person_1_full_name)
                        person_1_first_name = blah[1].strip()
                        report_object['person']['1']['first_name'] = person_1_first_name
                        logging.debug('[P1] First Name: %s' % person_1_first_name)
                        logging.debug('[P1] Middle Name: N/A')
                        person_1_last_name = blah[0][2:]
                        report_object['person']['1']['last_name'] = person_1_last_name
                        logging.debug('[P1] Last Name: %s' % person_1_last_name)
                    else:
                        person_1_full_name = blah[0][2:]
                        report_object['person']['1']['full_name'] = person_1_full_name
                        logging.debug('[P1] Full Name: %s' % person_1_full_name)

            # Person #1 DOB
            if llx == "385.63" and lly == "664.56":
                for line in box.iter('Line'):
                    person_1_dob = line.find('Text').text
                    report_object['person']['1']['dob'] = person_1_dob
                    logging.debug('[P1] DOB: %s' % person_1_dob)

            # Person #1 Age
            if llx == "485.42" and lly == "664.56":
                for line in box.iter('Line'):
                    person_1_age = line.find('Text').text
                    report_object['person']['1']['age'] = person_1_age
                    logging.debug('[P1] Age: %s' % person_1_age)

            # Person #1 Gender
            if llx == "518.26" and lly == "668.59":
                for line in box.iter('Line'):
                    person_1_gender = line.find('Text').text
                    report_object['person']['1']['gender'] = person_1_gender
                    logging.debug('[P1] Gender: %s' % person_1_gender)

            # Person #1 Address
            if llx == "34.27" and lly == "639.07":
                for line in box.iter('Line'):
                    person_1_address = line.find('Text').text
                    report_object['person']['1']['address'] = person_1_address
                    logging.debug('[P1] Address: %s' % person_1_address)

                    # Get zip code
                    person_1_zip = re.search(r'.*(\d{5}(-\d{4})?)$', person_1_address)
                    report_object['person']['1']['zip'] = str(person_1_zip.groups()[0])
                    logging.debug('[P1] Zip Code: %s' % str(person_1_zip.groups()[0]))

            # Person #1 Phone
            if llx == "423.43" and lly == "639.07":
                for line in box.iter('Line'):
                    person_1_phone = line.find('Text').text
                    report_object['person']['1']['phone'] = person_1_phone
                    logging.debug('[P1] Phone: %s' % report_object['person']['1']['phone'])

            # Person #1 Injuries
            if llx == "39.82" and lly == "615.02":
                for line in box.iter('Line'):
                    person_1_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['1']['injuries'] = person_1_injuries
                    logging.debug('[P1] Injuries: %s' % person_1_injuries)

            # Person #1 Air Bag
            if llx == "486.14" and lly == "615.02":
                for line in box.iter('Line'):
                    person_1_air_bag = line.find('Text').text
                    report_object['person']['1']['air_bag'] = person_1_air_bag
                    logging.debug('[P1] Air Bag: %s' % person_1_air_bag)

            # Person #1 Offense Charged
            if llx == "35.64" and lly == "558.72":
                for line in box.iter('Line'):
                    person_1_offense_charged = line.find('Text').text
                    report_object['person']['1']['offense_charged'] = person_1_offense_charged
                    logging.debug('[P1] Offense Charged: %s' % person_1_offense_charged)

            # Person #1 Offense Description
            if llx == "151.27" and lly == "559.58":
                for line in box.iter('Line'):
                    person_1_offense_description = line.find('Text').text
                    report_object['person']['1']['offense_description'] = person_1_offense_description
                    logging.debug('[P1] Offense Description: %s' % person_1_offense_description)

            # Person #1 Citation Number
            if llx == "357.05" and lly == "558.72":
                for line in box.iter('Line'):
                    person_1_citation_number = line.find('Text').text
                    report_object['person']['1']['citation_number'] = person_1_citation_number
                    logging.debug('[P1] Citation Number: %s' % person_1_citation_number)

            # PERSON #2 - MOTORIST / NON-MOTORIST / OCCUPANT V1 (Scanned lower on 1st page)
            #
            # Unit         <Box llx="34.27"  lly="532.94" urx="126.09" ury="540.94"> Sometimes Unit & Name
            # Name         <Box llx="72.29"  lly="532.94" urx="157.87" ury="540.94">
            # DOB          <Box llx="385.63" lly="533.09" urx="425.64" ury="541.09">
            # Age          <Box llx="485.42" lly="533.09" urx="494.32" ury="541.09">
            # Gender       <Box llx="517.10" lly="537.05" urx="525.43" ury="547.05">
            # Address      <Box llx="34.27"  lly="507.60" urx="176.89" ury="515.60">
            # Phone        <Box llx="423.43" lly="507.60" urx="473.23" ury="515.60">
            # Injuries/EMS ?
            # Injuries     <Box llx="39.82"  lly="483.55" urx="45.38"  ury="493.55">
            # Air Bag      <Box llx="486.14" lly="483.55" urx="491.70" ury="493.55">
            # Offense Crgd ? <Box llx="35.64"  lly="558.72" urx="60.09"  ury="566.72">
            # Offense Desc ? <Box llx="151.27" lly="559.58" urx="226.21" ury="567.58">
            # Citation Num ? <Box llx="357.05" lly="558.72" urx="392.63" ury="566.72">

            # Person #2 Unit Number or UN & Name
            if llx == "34.27" and lly == "532.94":
                logging.debug('\nPerson #2')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_2_unit_number = check_if_just_unit[0]
                        report_object['person']['2']['unit_number'] = person_2_unit_number
                        logging.debug('[P2] Unit Number Only: %s' % person_2_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_2_unit_number = blah[0][:1]
                        report_object['person']['2']['unit_number'] = person_2_unit_number
                        logging.debug('[P2] Unit Number: %s' % person_2_unit_number)

                        if len(blah) == 3:
                            person_2_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['2']['full_name'] = person_2_full_name
                            logging.debug('[P2] Full Name: %s' % person_2_full_name)
                            person_2_first_name = blah[1].strip()
                            report_object['person']['2']['first_name'] = person_2_first_name
                            logging.debug('[P2] First Name: %s' % person_2_first_name)
                            person_2_middle_name = blah[2].strip()
                            report_object['person']['2']['middle_name'] = person_2_middle_name
                            logging.debug('[P2] Middle Name: %s' % person_2_middle_name)
                            person_2_last_name = blah[0][2:]
                            report_object['person']['2']['last_name'] = person_2_last_name
                            logging.debug('[P2] Last Name: %s' % person_2_last_name)

                        elif len(blah) == 2:
                            person_2_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['2']['full_name'] = person_2_full_name
                            logging.debug('[P2] Full Name: %s' % person_2_full_name)
                            person_2_first_name = blah[1].strip()
                            report_object['person']['2']['first_name'] = person_2_first_name
                            logging.debug('[P2] First Name: %s' % person_2_first_name)
                            logging.debug('[P2] Middle Name: N/A')
                            person_2_last_name = blah[0][2:]
                            report_object['person']['2']['last_name'] = person_2_last_name
                            logging.debug('[P2] Last Name: %s' % person_2_last_name)

                        else:
                            person_2_unknown_name = blah[0][2:]
                            report_object['person']['2']['last_name'] = person_2_unknown_name
                            logging.debug('[P2] Unknown Name Format: %s' % person_2_unknown_name)

            # Person #2 Name (if not included with unit number above)
            if llx == "72.29" and lly == "532.94":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')
                    if len(blah) == 3:
                        person_2_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['2']['full_name'] = person_2_full_name
                        logging.debug('[P2] Full Name: %s' % person_2_full_name)
                        person_2_first_name = blah[1].strip()
                        report_object['person']['2']['first_name'] = person_2_first_name
                        logging.debug('[P2] First Name: %s' % person_2_first_name)
                        person_2_middle_name = blah[2].strip()
                        report_object['person']['2']['middle_name'] = person_2_middle_name
                        logging.debug('[P2] Middle Name: %s' % person_2_middle_name)
                        person_2_last_name = blah[0]
                        report_object['person']['2']['last_name'] = person_2_last_name
                        logging.debug('[P2] Last Name: %s' % person_2_last_name)

                    elif len(blah) == 2:
                        person_2_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['2']['full_name'] = person_2_full_name
                        logging.debug('[P2] Full Name: %s' % person_2_full_name)
                        person_2_first_name = blah[1].strip()
                        report_object['person']['2']['first_name'] = person_2_first_name
                        logging.debug('[P2] First Name: %s' % person_2_first_name)
                        logging.debug('[P2] Middle Name: N/A')
                        person_2_last_name = blah[0]
                        report_object['person']['2']['last_name'] = person_2_last_name
                        logging.debug('[P2] Last Name: %s' % person_2_last_name)

                    else:
                        person_2_unknown_name = blah[0]
                        report_object['person']['2']['last_name'] = person_2_unknown_name
                        logging.debug('[P2] Unknown Name Format: %s' % person_2_unknown_name)

            # Person #2 DOB
            if llx == "385.63" and lly == "533.09":
                for line in box.iter('Line'):
                    person_2_dob = line.find('Text').text
                    report_object['person']['2']['dob'] = person_2_dob
                    logging.debug('[P2] DOB: %s' % person_2_dob)

            # Person #2 Age
            if llx == "485.42" and lly == "533.09":
                for line in box.iter('Line'):
                    person_2_age = line.find('Text').text
                    report_object['person']['2']['age'] = person_2_age
                    logging.debug('[P2] Age: %s' % person_2_age)

            # Person #2 Gender
            if llx == "517.10" and lly == "537.05":
                for line in box.iter('Line'):
                    person_2_gender = line.find('Text').text
                    report_object['person']['2']['gender'] = person_2_gender
                    logging.debug('[P2] Gender: %s' % person_2_gender)

            # Person #2 Address
            if llx == "34.27" and lly == "507.60":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_2_address = line.find('Text').text
                        report_object['person']['2']['address'] = person_2_address
                        logging.debug('[P2] Address: %s' % person_2_address)

                        # Get zip code
                        person_2_zip = re.search(r'.*(\d{5}(\-\d{4})?)$', person_2_address)
                        report_object['person']['2']['zip'] = str(person_2_zip.groups()[0])
                        logging.debug('[P2] Zip Code: %s' % str(person_2_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_2_phone = line.find('Text').text
                        report_object['person']['2']['phone'] = person_2_phone
                        logging.debug('[P2] Phone: %s' % person_2_phone)

                    i = i + 1

            # Person #2 Phone
            if llx == "423.43" and lly == "507.60":
                for line in box.iter('Line'):
                    person_2_phone = line.find('Text').text
                    report_object['person']['2']['phone'] = person_2_phone
                    logging.debug('[P2] Phone: %s' % person_2_phone)

            # Person #2 Injuries
            if llx == "39.82" and lly == "483.55":
                for line in box.iter('Line'):
                    person_2_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['2']['injuries'] = person_2_injuries
                    logging.debug('[P2] Injuries: %s' % person_2_injuries)

            # Person #2 Air Bag
            if llx == "486.14" and lly == "483.55":
                for line in box.iter('Line'):
                    person_2_air_bag = line.find('Text').text
                    report_object['person']['2']['air_bag'] = person_2_air_bag
                    logging.debug('[P2] Air Bag: %s' % person_2_air_bag)

            # Person #2 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_offense_charged = line.find('Text').text
                    report_object['person']['2']['offense_charged'] = person_2_offense_charged
                    logging.debug('[P2] Offense Charged: %s' % person_2_offense_charged)

            # Person #2 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_offense_description = line.find('Text').text
                    report_object['person']['2']['offense_description'] = person_2_offense_description
                    logging.debug('[P2] Offense Description: %s' % person_2_offense_description)

            # Person #2 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_citation_number = line.find('Text').text
                    report_object['person']['2']['citation_number'] = person_2_citation_number
                    logging.debug('[P2] Citation Number: %s' % person_2_citation_number)

            # PERSON #3 - MOTORIST / NON-MOTORIST / OCCUPANT V1 (Scanned lower on 1st page)
            #
            # Unit         <Box llx == "34.56" and lly == "174.31" and urx == "39.01" and  ury == "182.31"> Sometimes Unit & Name
            # Name         <Box llx == "70.70" and lly == "174.53" and urx == "120.79" and ury == "182.53">
            # DOB          <Box llx == "383.11" and lly == "174.67" and urx == "423.12" and ury == "182.67">
            # Age          <Box llx == "483.70" and lly == "174.60" and urx == "492.59" and ury == "182.60">
            # Gender       <Box llx == "518.04" and lly == "178.34" and urx == "526.37" and ury == "188.34">
            # Address      <Box llx == "35.35" and lly == "147.02" and urx == "182.80" and ury == "155.02">
            # Phone        <Box llx == "420.84" and lly == "147.46" and urx == "470.64" and ury == "155.46">
            # Injuries/EMS ?
            # Injuries     <Box llx == "40.32" and lly == "124.85" and urx == "45.88" and  ury == "134.85">
            # Air Bag      <Box llx == "483.05" and lly == "139.18" and urx == "518.41" and ury == "143.18">
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # Person #3 Unit Number or UN & Name
            if llx == "34.56" and lly == "174.31":
                logging.debug('\nPerson #3')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_3_unit_number = check_if_just_unit[0]
                        report_object['person']['3']['unit_number'] = person_3_unit_number
                        logging.debug('[P3] Unit Number Only: %s' % person_3_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_3_unit_number = blah[0][:1]
                        report_object['person']['3']['unit_number'] = person_3_unit_number
                        logging.debug('[P3] Unit Number: %s' % person_3_unit_number)

                        if len(blah) == 3:
                            person_3_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['3']['full_name'] = person_3_full_name
                            logging.debug('[P3] Full Name: %s' % person_3_full_name)
                            person_3_first_name = blah[1].strip()
                            report_object['person']['3']['first_name'] = person_3_first_name
                            logging.debug('[P3] First Name: %s' % person_3_first_name)
                            person_3_middle_name = blah[2].strip()
                            report_object['person']['3']['middle_name'] = person_3_middle_name
                            logging.debug('[P3] Middle Name: %s' % person_3_middle_name)
                            person_3_last_name = blah[0][2:]
                            report_object['person']['3']['last_name'] = person_3_last_name
                            logging.debug('[P3] Last Name: %s' % person_3_last_name)

                        elif len(blah) == 2:
                            person_3_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['3']['full_name'] = person_3_full_name
                            logging.debug('[P3] Full Name: %s' % person_3_full_name)
                            person_3_first_name = blah[1].strip()
                            report_object['person']['3']['first_name'] = person_3_first_name
                            logging.debug('[P3] First Name: %s' % person_3_first_name)
                            logging.debug('[P3] Middle Name: N/A')
                            person_3_last_name = blah[0][2:]
                            report_object['person']['3']['last_name'] = person_3_last_name
                            logging.debug('[P3] Last Name: %s' % person_3_last_name)

                        else:
                            person_3_unknown_name = blah[0][2:]
                            report_object['person']['3']['last_name'] = person_3_unknown_name
                            logging.debug('[P3] Unknown Name Format: %s' % person_3_unknown_name)

            # Person #3 Name (if not included with unit number above)
            if llx == "70.70" and lly == "174.53":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_3_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['3']['full_name'] = person_3_full_name
                        logging.debug('[P3] Full Name: %s' % person_3_full_name)
                        person_3_first_name = blah[1].strip()
                        report_object['person']['3']['first_name'] = person_3_first_name
                        logging.debug('[P3] First Name: %s' % person_3_first_name)
                        person_3_middle_name = blah[2].strip()
                        report_object['person']['3']['middle_name'] = person_3_middle_name
                        logging.debug('[P3] Middle Name: %s' % person_3_middle_name)
                        person_3_last_name = blah[0]
                        report_object['person']['3']['last_name'] = person_3_last_name
                        logging.debug('[P3] Last Name: %s' % person_3_last_name)

                    elif len(blah) == 2:
                        person_3_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['3']['full_name'] = person_3_full_name
                        logging.debug('[P3] Full Name: %s' % person_3_full_name)
                        person_3_first_name = blah[1].strip()
                        report_object['person']['3']['first_name'] = person_3_first_name
                        logging.debug('[P3] First Name: %s' % person_3_first_name)
                        logging.debug('[P3] Middle Name: N/A')
                        person_3_last_name = blah[0]
                        report_object['person']['3']['last_name'] = person_3_last_name
                        logging.debug('[P3] Last Name: %s' % person_3_last_name)

                    else:
                        person_3_unknown_name = blah[0]
                        report_object['person']['3']['last_name'] = person_3_unknown_name
                        logging.debug('[P3] Unknown Name Format: %s' % person_3_unknown_name)

            # Person #3 DOB
            if llx == "383.11" and lly == "174.67":
                for line in box.iter('Line'):
                    person_3_dob = line.find('Text').text
                    report_object['person']['3']['dob'] = person_3_dob
                    logging.debug('[P3] DOB: %s' % person_3_dob)

            # Person #3 Age
            if llx == "483.70" and lly == "174.60":
                for line in box.iter('Line'):
                    person_3_age = line.find('Text').text
                    report_object['person']['3']['age'] = person_3_age
                    logging.debug('[P3] Age: %s' % person_3_age)

            # Person #3 Gender
            if llx == "518.04" and lly == "178.34":
                for line in box.iter('Line'):
                    person_3_gender = line.find('Text').text
                    report_object['person']['3']['gender'] = person_3_gender
                    logging.debug('[P3] Gender: %s' % person_3_gender)

            # Person #3 Address
            if llx == "35.35" and lly == "147.02":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_3_address = line.find('Text').text
                        report_object['person']['3']['address'] = person_3_address
                        logging.debug('[P3] Address: %s' % person_3_address)

                        # Get zip code
                        person_3_zip = re.search(r'.*(\d{5}(\-\d{4})?)$', person_3_address)
                        report_object['person']['3']['zip'] = str(person_3_zip.groups()[0])
                        logging.debug( '[P3] Zip Code: %s' % str(person_3_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_3_phone = line.find('Text').text
                        report_object['person']['3']['phone'] = person_3_phone
                        logging.debug('[P3] Phone: %s' % person_3_phone)

                    i = i + 1

            # Person #3 Phone
            if llx == "420.84" and lly == "147.46":
                for line in box.iter('Line'):
                    person_3_phone = line.find('Text').text
                    report_object['person']['3']['phone'] = person_3_phone
                    logging.debug('[P3] Phone: %s' % person_3_phone)

            # Person #3 Injuries
            if llx == "40.32" and lly == "124.85":
                for line in box.iter('Line'):
                    person_3_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['3']['injuries'] = person_3_injuries
                    logging.debug('[P3] Injuries: %s' % person_3_injuries)

            # Person #3 Air Bag
            # THIS IS WRONG
            if llx == "483.05" and lly == "139.18":
                for line in box.iter('Line'):
                    person_3_air_bag = line.find('Text').text
                    report_object['person']['3']['air_bag'] = person_3_air_bag
                    logging.debug('[P3] Air Bag: %s' % person_3_air_bag)

            # Person #3 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_offense_charged = line.find('Text').text
                    report_object['person']['3']['offense_charged'] = person_3_offense_charged
                    logging.debug('[P3] Offense Charged: %s' % person_3_offense_charged)

            # Person #3 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_offense_description = line.find('Text').text
                    report_object['person']['3']['offense_description'] = person_3_offense_description
                    logging.debug('[P3] Offense Description: %s' % person_3_offense_description)

            # Person #3 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_citation_number = line.find('Text').text
                    report_object['person']['3']['citation_number'] = person_3_citation_number
                    logging.debug('[P3] Citation Number: %s' % person_3_citation_number)

            # PERSON #4 - MOTORIST / NON-MOTORIST / OCCUPANT V1 (Scanned lower on 1st page)
            #
            # Unit         <Box llx="34.56" lly="91.37" ulx="34.56" uly="99.37" urx="155.76" ury="99.51" lrx="155.76" lry="91.51"> Sometimes Unit & Name
            # Name         <Box llx="70.70" lly="91.51" urx="142.89" ury="99.51">
            # DOB          <Box llx="383.11" lly="91.73" urx="423.12" ury="99.73">
            # Age          <Box llx="483.70" lly="91.58" urx="492.59" ury="99.58">
            # Gender       <Box llx="515.23" lly="107.28" urx="533.90" ury="111.28">
            # Address      <Box llx="35.35" lly="64.01" urx="183.69" ury="72.01">
            # Phone        <Box llx="420.84" lly="64.51" urx="470.64" ury="72.51">
            # Injuries/EMS <Box llx="40.32" lly="41.90" urx="73.24" ury="51.90">
            # Air Bag      <Box llx="486.58" lly="41.90" urx="492.14" ury="51.90">
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # Person #4 Unit Number or UN & Name
            if llx == "34.56" and lly == "91.37":
                logging.debug('\nPerson #4')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_4_unit_number = check_if_just_unit[0]
                        report_object['person']['4']['unit_number'] = person_4_unit_number
                        logging.debug('[P4] Unit Number Only: %s' % person_4_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_4_unit_number = blah[0][:1]
                        report_object['person']['4']['unit_number'] = person_4_unit_number
                        logging.debug('[P4] Unit Number: %s' % person_4_unit_number)

                        if len(blah) == 3:
                            person_4_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['4']['full_name'] = person_4_full_name
                            logging.debug('[P4] Full Name: %s' % person_4_full_name)
                            person_4_first_name = blah[1].strip()
                            report_object['person']['4']['first_name'] = person_4_first_name
                            logging.debug('[P4] First Name: %s' % person_4_first_name)
                            person_4_middle_name = blah[2].strip()
                            report_object['person']['4']['middle_name'] = person_4_middle_name
                            logging.debug('[P4] Middle Name: %s' % person_4_middle_name)
                            person_4_last_name = blah[0][2:]
                            report_object['person']['4']['last_name'] = person_4_last_name
                            logging.debug('[P4] Last Name: %s' % person_4_last_name)

                        elif len(blah) == 2:
                            person_4_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['4']['full_name'] = person_4_full_name
                            logging.debug('[P4] Full Name: %s' % person_4_full_name)
                            person_4_first_name = blah[1].strip()
                            report_object['person']['4']['first_name'] = person_4_first_name
                            logging.debug('[P4] First Name: %s' % person_4_first_name)
                            logging.debug('[P4] Middle Name: N/A')
                            person_4_last_name = blah[0][2:]
                            report_object['person']['4']['last_name'] = person_4_last_name
                            logging.debug('[P4] Last Name: %s' % person_4_last_name)

                        else:
                            person_4_unknown_name = blah[0][2:]
                            report_object['person']['4']['last_name'] = person_4_unknown_name
                            logging.debug('[P4] Unknown Name Format: %s' % person_4_unknown_name)

            # Person #4 Name (if not included with unit number above)
            if llx == "70.70" and lly == "91.51":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_4_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['4']['full_name'] = person_4_full_name
                        logging.debug('[P4] Full Name: %s' % person_4_full_name)
                        person_4_first_name = blah[1].strip()
                        report_object['person']['4']['first_name'] = person_4_first_name
                        logging.debug('[P4] First Name: %s' % person_4_first_name)
                        person_4_middle_name = blah[2].strip()
                        report_object['person']['4']['middle_name'] = person_4_middle_name
                        logging.debug('[P4] Middle Name: %s' % person_4_middle_name)
                        person_4_last_name = blah[0]
                        report_object['person']['4']['last_name'] = person_4_last_name
                        logging.debug('[P4] Last Name: %s' % person_4_last_name)

                    elif len(blah) == 2:
                        person_4_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['4']['full_name'] = person_4_full_name
                        logging.debug('[P4] Full Name: %s' % person_4_full_name)
                        person_4_first_name = blah[1].strip()
                        report_object['person']['4']['first_name'] = person_4_first_name
                        logging.debug('[P4] First Name: %s' % person_4_first_name)
                        logging.debug('[P4] Middle Name: N/A')
                        person_4_last_name = blah[0]
                        report_object['person']['4']['last_name'] = person_4_last_name
                        logging.debug('[P4] Last Name: %s' % person_4_last_name)

                    else:
                        person_4_unknown_name = blah[0]
                        report_object['person']['4']['last_name'] = person_4_unknown_name
                        logging.debug('[P4] Unknown Name Format: %s' % person_4_unknown_name)

            # Person #4 DOB
            if llx == "383.11" and lly == "91.73":
                for line in box.iter('Line'):
                    person_4_dob = line.find('Text').text
                    report_object['person']['4']['dob'] = person_4_dob
                    logging.debug('[P4] DOB: %s' % person_4_dob)

            # Person #4 Age
            if llx == "483.70" and lly == "91.58":
                for line in box.iter('Line'):
                    person_4_age = line.find('Text').text
                    report_object['person']['4']['age'] = person_4_age
                    logging.debug('[P4] Age: %s' % person_4_age)

            # Person #4 Gender
            if llx == "515.23" and lly == "107.28":
                for line in box.iter('Line'):
                    person_4_gender = line.find('Text').text
                    report_object['person']['4']['gender'] = person_4_gender
                    logging.debug('[P4] Gender: %s' % person_4_gender)

            # Person #4 Address
            if llx == "35.35" and lly == "64.01":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_4_address = line.find('Text').text
                        report_object['person']['4']['address'] = person_4_address
                        logging.debug('[P4] Address: %s' % person_4_address)

                        # Get zip code
                        person_4_zip = re.search(r'.*(\d{5}(\-\d{4})?)$', person_4_address)
                        report_object['person']['4']['zip'] = str(person_4_zip.groups()[0])
                        logging.debug('[P4] Zip Code: %s' % str(person_4_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_4_phone = line.find('Text').text
                        report_object['person']['4']['phone'] = person_4_phone
                        logging.debug('[P4] Phone: %s' % person_4_phone)

                    i = i + 1


            # Person #4 Phone
            if llx == "420.84" and lly == "64.51":
                for line in box.iter('Line'):
                    person_4_phone = line.find('Text').text
                    report_object['person']['4']['phone'] = person_4_phone
                    logging.debug('[P4] Phone: %s' % person_4_phone)

            # Person #4 Injuries
            # !!!!!!!!!
            if llx == "40.32" and lly == "41.90":
                for line in box.iter('Line'):
                    person_4_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['4']['injuries'] = person_4_injuries
                    logging.debug('[P4] Injuries: %s' % person_4_injuries)

            # Person #4 Air Bag
            if llx == "486.58" and lly == "41.90":
                for line in box.iter('Line'):
                    person_4_air_bag = line.find('Text').text
                    report_object['person']['4']['air_bag'] = person_4_air_bag
                    logging.debug('[P4] Air Bag: %s' % person_4_air_bag)

            # Person #4 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_offense_charged = line.find('Text').text
                    report_object['person']['4']['offense_charged'] = person_4_offense_charged
                    logging.debug('[P4] Offense Charged: %s' % person_4_offense_charged)

            # Person #4 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_offense_description = line.find('Text').text
                    report_object['person']['4']['offense_description'] = person_4_offense_description
                    logging.debug('[P4] Offense Description: %s' % person_4_offense_description)

            # Person #4 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_citation_number = line.find('Text').text
                    report_object['person']['4']['citation_number'] = person_4_citation_number
                    logging.debug('[P4] Citation Number: %s' % person_4_citation_number)

            # PERSON #1v2 - MOTORIST / NON-MOTORIST / OCCUPANT V2 (Scanned higher on subsequent pages)
            #
            # Unit         <Box llx == "34.27" and lly == "699.55" and urx == "181.76" and ury == "707.55"> Sometimes Unit & Name
            # Name         ?
            # DOB          <Box llx == "385.63" and lly == "699.62" and urx == "425.64" and ury == "707.62">
            # Age          <Box llx == "485.42" and lly == "699.62" and urx == "494.32" and ury == "707.62">
            # Gender       <Box llx == "518.26" and lly == "703.66" and urx == "524.36" and ury == "713.65">
            # Address      <Box llx == "34.27" and lly == "674.14" and urx == "191.99" and ury == "682.13">
            # Phone        <Box llx == "423.43" and lly == "674.14" and urx == "473.23" and ury == "682.13">
            # Injuries     <Box llx == "39.82" and lly == "650.09" and urx == "45.38" and ury == "660.09">
            # EMS          <Box llx == "67.25" and lly == "650.09" and urx == "72.81" and ury == "660.09">
            # Air Bag      <Box llx == "486.14" and lly == "650.09" and urx == "491.70" and ury == "660.09">
            # Offense Crgd ?
            # Offense Desc ?
            # Citation Num ?

            # Person #1v2 Unit Number or UN & Name
            if llx == "34.27" and lly == "699.55":
                logging.debug('\nPerson #1v2')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_1_v2_unit_number = check_if_just_unit[0]
                        report_object['person']['5']['unit_number'] = person_1_v2_unit_number
                        logging.debug('[P1v2] Unit Number Only: %s' % person_1_v2_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_1_v2_unit_number = blah[0][:1]
                        report_object['person']['5']['unit_number'] = person_1_v2_unit_number
                        logging.debug('[P1v2] Unit Number: %s' % person_1_v2_unit_number)

                        if len(blah) == 3:
                            person_1_v2_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['5']['full_name'] = person_1_v2_full_name
                            logging.debug('[P1v2] Full Name: %s' % person_1_v2_full_name)
                            person_1_v2_first_name = blah[1].strip()
                            report_object['person']['5']['first_name'] = person_1_v2_first_name
                            logging.debug('[P1v2] First Name: %s' % person_1_v2_first_name)
                            person_1_v2_middle_name = blah[2].strip()
                            report_object['person']['5']['middle_name'] = person_1_v2_middle_name
                            logging.debug('[P1v2] Middle Name: %s' % person_1_v2_middle_name)
                            person_1_v2_last_name = blah[0][2:]
                            report_object['person']['5']['last_name'] = person_1_v2_last_name
                            logging.debug('[P1v2] Last Name: %s' % person_1_v2_last_name)

                        elif len(blah) == 2:
                            person_1_v2_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['5']['full_name'] = person_1_v2_full_name
                            logging.debug('[P1v2] Full Name: %s' % person_1_v2_full_name)
                            person_1_v2_first_name = blah[1].strip()
                            report_object['person']['5']['first_name'] = person_1_v2_first_name
                            logging.debug('[P1v2] First Name: %s' % person_1_v2_first_name)
                            logging.debug('[P1v2] Middle Name: N/A')
                            person_1_v2_last_name = blah[0][2:]
                            report_object['person']['5']['last_name'] = person_1_v2_last_name
                            logging.debug('[P1v2] Last Name: %s' % person_1_v2_last_name)

                        else:
                            person_1_v2_unknown_name = blah[0][2:]
                            report_object['person']['5']['last_name'] = person_1_v2_unknown_name
                            logging.debug('[P1v2] Unknown Name Format: %s' % person_1_v2_unknown_name)

            # Person #1v2 Name (if not included with unit number above)
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_1_v2_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['5']['full_name'] = person_1_v2_full_name
                        logging.debug('[P1v2] Full Name: %s' % person_1_v2_full_name)
                        person_1_v2_first_name = blah[1].strip()
                        report_object['person']['5']['first_name'] = person_1_v2_first_name
                        logging.debug('[P1v2] First Name: %s' % person_1_v2_first_name)
                        person_1_v2_middle_name = blah[2].strip()
                        report_object['person']['5']['middle_name'] = person_1_v2_middle_name
                        logging.debug('[P1v2] Middle Name: %s' % person_1_v2_middle_name)
                        person_1_v2_last_name = blah[0]
                        report_object['person']['5']['last_name'] = person_1_v2_last_name
                        logging.debug('[P1v2] Last Name: %s' % person_1_v2_last_name)

                    elif len(blah) == 2:
                        person_1_v2_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['5']['full_name'] = person_1_v2_full_name
                        logging.debug('[P1v2] Full Name: %s' % person_1_v2_full_name)
                        person_1_v2_first_name = blah[1].strip()
                        report_object['person']['5']['first_name'] = person_1_v2_first_name
                        logging.debug('[P1v2] First Name: %s' % person_1_v2_first_name)
                        logging.debug('[P1v2] Middle Name: N/A')
                        person_1_v2_last_name = blah[0]
                        report_object['person']['5']['last_name'] = person_1_v2_last_name
                        logging.debug('[P1v2] Last Name: %s' % person_1_v2_last_name)

                    else:
                        person_1_v2_unknown_name = blah[0]
                        report_object['person']['5']['last_name'] = person_1_v2_unknown_name
                        logging.debug('[P1v2] Unknown Name Format: %s' % person_1_v2_unknown_name)

            # Person #1v2 DOB
            if llx == "385.63" and lly == "699.62":
                for line in box.iter('Line'):
                    person_1_v2_dob = line.find('Text').text
                    report_object['person']['5']['dob'] = person_1_v2_dob
                    logging.debug('[P1v2] DOB: %s' % person_1_v2_dob)

            # Person #1v2 Age
            if llx == "485.42" and lly == "699.62":
                for line in box.iter('Line'):
                    person_1_v2_age = line.find('Text').text
                    report_object['person']['5']['age'] = person_1_v2_age
                    logging.debug('[P1v2] Age: %s' % person_1_v2_age)

            # Person #1v2 Gender
            if llx == "518.26" and lly == "703.66":
                for line in box.iter('Line'):
                    person_1_v2_gender = line.find('Text').text
                    report_object['person']['5']['gender'] = person_1_v2_gender
                    logging.debug('[P1v2] Gender: %s' % person_1_v2_gender)

            # Person #1v2 Address
            if llx == "34.27" and lly == "674.14":
                i = 0
                for line in box.iter('Line'):
                    if i == 1:
                        person_1_v2_address = line.find('Text').text
                        report_object['person']['5']['address'] = person_1_v2_address
                        logging.debug('[P1v2] Address: %s' % person_1_v2_address)

                        # Get zip code
                        person_1_v2_zip = re.search(r'.*(\d{5}(-\d{4})?)$', person_1_v2_address)
                        report_object['person']['5']['zip'] = str(person_1_v2_zip.groups()[0])
                        logging.debug('[P1v2] Zip Code: %s' % str(person_1_v2_zip.groups()[0]))
                    elif i == 0:
                        # Phone number?
                        person_1_v2_phone = line.find('Text').text
                        report_object['person']['5']['phone'] = person_1_v2_phone
                        logging.debug('[P1v2] Phone: %s' % person_1_v2_phone)

                    i = i + 1


            # Person #1v2 Phone
            if llx == "423.43" and lly == "674.14":
                for line in box.iter('Line'):
                    person_1_v2_phone = line.find('Text').text
                    report_object['person']['5']['phone'] = person_1_v2_phone
                    logging.debug('[P1v2] Phone: %s' % person_1_v2_phone)

            # Person #1v2 Injuries
            if llx == "39.82" and lly == "650.09":
                for line in box.iter('Line'):
                    person_1_v2_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['5']['injuries'] = person_1_v2_injuries
                    logging.debug('[P1v2] Injuries: %s' % person_1_v2_injuries)

            # Person #1v2 Air Bag
            if llx == "486.14" and lly == "650.09":
                for line in box.iter('Line'):
                    person_1_v2_air_bag = line.find('Text').text
                    report_object['person']['5']['air_bag'] = person_1_v2_air_bag
                    logging.debug('[P1v2] Air Bag: %s' % person_1_v2_air_bag)

            # Person #1v2 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_1_v2_offense_charged = line.find('Text').text
                    report_object['person']['5']['offense_charged'] = person_1_v2_offense_charged
                    logging.debug('[P1v2] Offense Charged: %s' % person_1_v2_offense_charged)

            # Person #1v2 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_1_v2_offense_description = line.find('Text').text
                    report_object['person']['5']['offense_description'] = person_1_v2_offense_description
                    logging.debug('[P1v2] Offense Description: %s' % person_1_v2_offense_description)

            # Person #1v2 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_1_v2_citation_number = line.find('Text').text
                    report_object['person']['5']['citation_number'] = person_1_v2_citation_number
                    logging.debug('[P1v2] Citation Number: %s' % person_1_v2_citation_number)

            # PERSON #2 - MOTORIST / NON-MOTORIST / OCCUPANT V2 (Scanned higher on subsequent pages)
            #
            # Unit & Name  <Box llx == "34.27" and lly == "568.01" and urx == "128.57" and ury == "576.01"> Sometimes Unit & Name
            # Name         ?
            # DOB          <Box llx == "385.63" and lly == "568.15" and urx == "425.64" and ury == "576.15">
            # Age          <Box llx == "485.42" and lly == "568.15" and urx == "494.32" and ury == "576.15">
            # Gender       <Box llx == "517.10" and lly == "572.11" and urx == "525.43" and ury == "582.11">
            # Address      <Box llx == "34.27" and lly == "542.66" and urx == "161.34" and ury == "550.66">
            # Phone        <Box llx == "423.43" and lly == "542.66" and urx == "473.23" and ury == "550.66">
            # Injuries     <Box llx == "39.82" and lly == "518.62" and urx == "45.38" and ury == "528.62">
            # EMS          ?
            # Air Bag      <Box llx == "486.14" and lly == "518.62" and urx == "491.70" and ury == "528.62">
            # Offense Crgd ?
            # Offense Desc ?
            # Citation Num ?

            # Person #2v2 Unit Number or UN & Name
            if llx == "34.27" and lly == "568.01":
                logging.debug('\nPerson #2v2')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_2_v2_unit_number = check_if_just_unit[0]
                        report_object['person']['6']['unit_number'] = person_2_v2_unit_number
                        logging.debug('[P2v2] Unit Number Only: %s' % person_2_v2_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_2_v2_unit_number = blah[0][:1]
                        report_object['person']['6']['unit_number'] = person_2_v2_unit_number
                        logging.debug('[P2v2] Unit Number: %s' % person_2_v2_unit_number)

                        if len(blah) == 3:
                            person_2_v2_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['6']['full_name'] = person_2_v2_full_name
                            logging.debug('[P2v2] Full Name: %s' % person_2_v2_full_name)
                            person_2_v2_first_name = blah[1].strip()
                            report_object['person']['6']['first_name'] = person_2_v2_first_name
                            logging.debug('[P2v2] First Name: %s' % person_2_v2_first_name)
                            person_2_v2_middle_name = blah[2].strip()
                            report_object['person']['6']['middle_name'] = person_2_v2_middle_name
                            logging.debug('[P2v2] Middle Name: %s' % person_2_v2_middle_name)
                            person_2_v2_last_name = blah[0][2:]
                            report_object['person']['6']['last_name'] = person_2_v2_last_name
                            logging.debug('[P2v2] Last Name: %s' % person_2_v2_last_name)

                        elif len(blah) == 2:
                            person_2_v2_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['6']['full_name'] = person_2_v2_full_name
                            logging.debug('[P2v2] Full Name: %s' % person_2_v2_full_name)
                            person_2_v2_first_name = blah[1].strip()
                            report_object['person']['6']['first_name'] = person_2_v2_first_name
                            logging.debug('[P2v2] First Name: %s' % person_2_v2_first_name)
                            logging.debug('[P2v2] Middle Name: N/A')
                            person_2_v2_last_name = blah[0][2:]
                            report_object['person']['6']['last_name'] = person_2_v2_last_name
                            logging.debug('[P2v2] Last Name: %s' % person_2_v2_last_name)

                        else:
                            person_2_v2_unknown_name = blah[0][2:]
                            report_object['person']['6']['last_name'] = person_2_v2_unknown_name
                            logging.debug('[P2v2] Unknown Name Format: %s' % person_2_v2_unknown_name)

            # Person #2v2 Name (if not included with unit number above)
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_2_v2_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['6']['full_name'] = person_2_v2_full_name
                        logging.debug('[P2v2] Full Name: %s' % person_2_v2_full_name)
                        person_2_v2_first_name = blah[1].strip()
                        report_object['person']['6']['first_name'] = person_2_v2_first_name
                        logging.debug('[P2v2] First Name: %s' % person_2_v2_first_name)
                        person_2_v2_middle_name = blah[2].strip()
                        report_object['person']['6']['middle_name'] = person_2_v2_middle_name
                        logging.debug('[P2v2] Middle Name: %s' % person_2_v2_middle_name)
                        person_2_v2_last_name = blah[0]
                        report_object['person']['6']['last_name'] = person_2_v2_last_name
                        logging.debug('[P2v2] Last Name: %s' % person_2_v2_last_name)

                    elif len(blah) == 2:
                        person_2_v2_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['6']['full_name'] = person_2_v2_full_name
                        logging.debug('[P2v2] Full Name: %s' % person_2_v2_full_name)
                        person_2_v2_first_name = blah[1].strip()
                        report_object['person']['6']['first_name'] = person_2_v2_first_name
                        logging.debug('[P2v2] First Name: %s' % person_2_v2_first_name)
                        logging.debug('[P2v2] Middle Name: N/A')
                        person_2_v2_last_name = blah[0]
                        report_object['person']['6']['last_name'] = person_2_v2_last_name
                        logging.debug('[P2v2] Last Name: %s' % person_2_v2_last_name)

                    else:
                        person_2_v2_unknown_name = blah[0]
                        report_object['person']['6']['last_name'] = person_2_v2_unknown_name
                        logging.debug('[P2v2] Unknown Name Format: %s' % person_2_v2_unknown_name)

            # Person #2v2 DOB
            if llx == "385.63" and lly == "568.15":
                for line in box.iter('Line'):
                    person_2_v2_dob = line.find('Text').text
                    report_object['person']['6']['dob'] = person_2_v2_dob
                    logging.debug('[P2v2] DOB: %s' % person_2_v2_dob)

            # Person #2v2 Age
            if llx == "485.42" and lly == "568.15":
                for line in box.iter('Line'):
                    person_2_v2_age = line.find('Text').text
                    report_object['person']['6']['age'] = person_2_v2_age
                    logging.debug('[P2v2] Age: %s' % person_2_v2_age)

            # Person #2v2 Gender
            if llx == "517.10" and lly == "572.11":
                for line in box.iter('Line'):
                    person_2_v2_gender = line.find('Text').text
                    report_object['person']['6']['gender'] = person_2_v2_gender
                    logging.debug('[P2v2] Gender: %s' % person_2_v2_gender)

            # Person #2v2 Address
            if llx == "34.27" and lly == "542.66":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_2_v2_address = line.find('Text').text
                        report_object['person']['6']['address'] = person_2_v2_address
                        logging.debug('[P2v2] Address: %s' % person_2_v2_address)

                        # Get zip code
                        person_2_v2_zip = re.search(r'.*(\d{5}(-\d{4})?)$', person_2_v2_address)
                        report_object['person']['6']['zip'] = str(person_2_v2_zip.groups()[0])
                        logging.debug('[P2v2] Zip Code: %s' % str(person_2_v2_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_2_v2_phone = line.find('Text').text
                        report_object['person']['6']['phone'] = person_2_v2_phone
                        logging.debug('[P2v2] Phone: %s' % person_2_v2_phone)

                    i = i + 1

            # Person #2v2 Phone
            if llx == "423.43" and lly == "542.66":
                for line in box.iter('Line'):
                    person_2_v2_phone = line.find('Text').text
                    report_object['person']['6']['phone'] = person_2_v2_phone
                    logging.debug('[P2v2] Phone: %s' % person_2_v2_phone)

            # Person #2v2 Injuries
            if llx == "39.82" and lly == "518.62":
                for line in box.iter('Line'):
                    person_2_v2_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['6']['injuries'] = person_2_v2_injuries
                    logging.debug('[P2v2] Injuries: %s' % person_2_v2_injuries)

            # Person #2v2 Air Bag
            if llx == "486.14" and lly == "518.62":
                for line in box.iter('Line'):
                    person_2_v2_air_bag = line.find('Text').text
                    report_object['person']['6']['air_bag'] = person_2_v2_air_bag
                    logging.debug('[P2v2] Air Bag: %s' % person_2_v2_air_bag)

            # Person #2v2 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_v2_offense_charged = line.find('Text').text
                    report_object['person']['6']['offense_charged'] = person_2_v2_offense_charged
                    logging.debug('[P2v2] Offense Charged: %s' % person_2_v2_offense_charged)

            # Person #2v2 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_v2_offense_description = line.find('Text').text
                    report_object['person']['6']['offense_description'] = person_2_v2_offense_description
                    logging.debug('[P2v2] Offense Description: %s' % person_2_v2_offense_description)

            # Person #2v2 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_2_v2_citation_number = line.find('Text').text
                    report_object['person']['6']['citation_number'] = person_2_v2_citation_number
                    logging.debug('[P2v2] Citation Number: %s' % person_2_v2_citation_number)

            # PERSON #3 - MOTORIST / NON-MOTORIST / OCCUPANT V2 (Scanned higher on subsequent pages)
            #
            # Unit         <Box llx == "34.56" and lly == "209.38" and urx == "39.01" and ury == "217.38"> Sometimes Unit & Name
            # Name         <Box llx == "70.70" and lly == "209.59" and urx == "122.24" and ury == "217.59">
            # DOB          <Box llx == "383.11" and lly == "209.74" and urx == "423.12" and ury == "217.73">
            # Age          <Box llx == "483.70" and lly == "225.58" and urx == "493.50" and ury == "229.58">
            # Gender       <Box llx == "518.04" and lly == "213.48" and urx == "526.37" and ury == "223.48">
            # Address      <Box llx == "35.35" and lly == "182.09" and urx == "161.13" and ury == "190.09">
            # Phone        <Box llx == "420.84" and lly == "182.52" and urx == "470.64" and ury == "190.52">
            # Injuries     <Box llx == "40.32" and lly == "159.91" and urx == "45.88" and ury == "169.91">
            # EMS          ?
            # Air Bag      <Box llx == "486.58" and lly == "159.91" and urx == "492.14" and ury == "169.91">
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # Person #3v2 Unit Number or UN & Name
            if llx == "34.56" and lly == "209.38":
                logging.debug('\nPerson #3v2')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_3_v2_unit_number = check_if_just_unit[0]
                        report_object['person']['7']['unit_number'] = person_3_v2_unit_number
                        logging.debug('[P3v2] Unit Number Only: %s' % person_3_v2_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_3_v2_unit_number = blah[0][:1]
                        report_object['person']['7']['unit_number'] = person_3_v2_unit_number
                        logging.debug('[P3v2] Unit Number: %s' % person_3_v2_unit_number)

                        if len(blah) == 3:
                            person_3_v2_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['7']['full_name'] = person_3_v2_full_name
                            logging.debug('[P3v2] Full Name: %s' % person_3_v2_full_name)
                            person_3_v2_first_name = blah[1].strip()
                            report_object['person']['7']['first_name'] = person_3_v2_first_name
                            logging.debug('[P3v2] First Name: %s' % person_3_v2_first_name)
                            person_3_v2_middle_name = blah[2].strip()
                            report_object['person']['7']['middle_name'] = person_3_v2_middle_name
                            logging.debug('[P3v2] Middle Name: %s' % person_3_v2_middle_name)
                            person_3_v2_last_name = blah[0][2:]
                            report_object['person']['7']['last_name'] = person_3_v2_last_name
                            logging.debug('[P3v2] Last Name: %s' % person_3_v2_last_name)

                        elif len(blah) == 2:
                            person_3_v2_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['7']['full_name'] = person_3_v2_full_name
                            logging.debug('[P3v2] Full Name: %s' % person_3_v2_full_name)
                            person_3_v2_first_name = blah[1].strip()
                            report_object['person']['7']['first_name'] = person_3_v2_first_name
                            logging.debug('[P3v2] First Name: %s' % person_3_v2_first_name)
                            logging.debug('[P3v2] Middle Name: N/A')
                            person_3_v2_last_name = blah[0][2:]
                            report_object['person']['7']['last_name'] = person_3_v2_last_name
                            logging.debug('[P3v2] Last Name: %s' % person_3_v2_last_name)

                        else:
                            person_3_v2_unknown_name = blah[0][2:]
                            report_object['person']['7']['last_name'] = person_3_v2_unknown_name
                            logging.debug('[P3v2] Unknown Name Format: %s' % person_3_v2_unknown_name)

            # Person #3v2 Name (if not included with unit number above)
            if llx == "70.70" and lly == "209.59":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_3_v2_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['7']['full_name'] = person_3_v2_full_name
                        logging.debug('[P3v2] Full Name: %s' % person_3_v2_full_name)
                        person_3_v2_first_name = blah[1].strip()
                        report_object['person']['7']['first_name'] = person_3_v2_first_name
                        logging.debug('[P3v2] First Name: %s' % person_3_v2_first_name)
                        person_3_v2_middle_name = blah[2].strip()
                        report_object['person']['7']['middle_name'] = person_3_v2_middle_name
                        logging.debug('[P3v2] Middle Name: %s' % person_3_v2_middle_name)
                        person_3_v2_last_name = blah[0]
                        report_object['person']['7']['last_name'] = person_3_v2_last_name
                        logging.debug('[P3v2] Last Name: %s' % person_3_v2_last_name)

                    elif len(blah) == 2:
                        person_3_v2_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['7']['full_name'] = person_3_v2_full_name
                        logging.debug('[P3v2] Full Name: %s' % person_3_v2_full_name)
                        person_3_v2_first_name = blah[1].strip()
                        report_object['person']['7']['first_name'] = person_3_v2_first_name
                        logging.debug('[P3v2] First Name: %s' % person_3_v2_first_name)
                        logging.debug('[P3v2] Middle Name: N/A')
                        person_3_v2_last_name = blah[0]
                        report_object['person']['7']['last_name'] = person_3_v2_last_name
                        logging.debug('[P3v2] Last Name: %s' % person_3_v2_last_name)

                    else:
                        person_3_v2_unknown_name = blah[0]
                        report_object['person']['7']['last_name'] = person_3_v2_unknown_name
                        logging.debug('[P3v2] Unknown Name Format: %s' % person_3_v2_unknown_name)

            # Person #3v2 DOB
            if llx == "383.11" and lly == "209.74":
                for line in box.iter('Line'):
                    person_3_v2_dob = line.find('Text').text
                    report_object['person']['7']['dob'] = person_3_v2_dob
                    logging.debug('[P3v2] DOB: %s' % person_3_v2_dob)

            # Person #3v2 Age
            if llx == "483.70" and lly == "225.58":
                for line in box.iter('Line'):
                    person_3_v2_age = line.find('Text').text
                    report_object['person']['7']['age'] = person_3_v2_age
                    logging.debug('[P3v2] Age: %s' % person_3_v2_age)

            # Person #3v2 Gender
            if llx == "518.04" and lly == "213.48":
                for line in box.iter('Line'):
                    person_3_v2_gender = line.find('Text').text
                    report_object['person']['7']['gender'] = person_3_v2_gender
                    logging.debug('[P3v2] Gender: %s' % person_3_v2_gender)

            # Person #3v2 Address
            if llx == "35.35" and lly == "182.09":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_3_v2_address = line.find('Text').text
                        report_object['person']['7']['address'] = person_3_v2_address
                        logging.debug('[P3v2] Address: %s' % person_3_v2_address)

                        # Get zip code
                        person_3_v2_zip = re.search(r'.*(\d{5}(-\d{4})?)$', person_3_v2_address)
                        report_object['person']['7']['zip'] = str(person_3_v2_zip.groups()[0])
                        logging.debug('[P3v2] Zip Code: %s' % str(person_3_v2_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_3_v2_phone = line.find('Text').text
                        report_object['person']['7']['phone'] = person_3_v2_phone
                        logging.debug('[P3v2] Phone: %s' % person_3_v2_phone)

                    i = i + 1

            # Person #3v2 Phone
            if llx == "420.84" and lly == "182.52":
                for line in box.iter('Line'):
                    person_3_v2_phone = line.find('Text').text
                    report_object['person']['7']['phone'] = person_3_v2_phone
                    logging.debug('[P3v2] Phone: %s' % person_3_v2_phone)

            # Person #3v2 Injuries
            if llx == "40.32" and lly == "159.91":
                for line in box.iter('Line'):
                    person_3_v2_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['7']['injuries'] = person_3_v2_injuries
                    logging.debug('[P3v2] Injuries: %s' % person_3_v2_injuries)

            # Person #3v2 Air Bag
            if llx == "486.58" and lly == "159.91":
                for line in box.iter('Line'):
                    person_3_v2_air_bag = line.find('Text').text
                    report_object['person']['7']['air_bag'] = person_3_v2_air_bag
                    logging.debug('[P3v2] Air Bag: %s' % person_3_v2_air_bag)

            # Person #3v2 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_v2_offense_charged = line.find('Text').text
                    report_object['person']['7']['offense_charged'] = person_3_v2_offense_charged
                    logging.debug('[P3v2] Offense Charged: %s' % person_3_v2_offense_charged)

            # Person #3v2 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_v2_offense_description = line.find('Text').text
                    report_object['person']['7']['offense_description'] = person_3_v2_offense_description
                    logging.debug('[P3v2] Offense Description: %s' % person_3_v2_offense_description)

            # Person #3v2 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_3_v2_citation_number = line.find('Text').text
                    report_object['person']['7']['citation_number'] = person_3_v2_citation_number
                    logging.debug('[P3v2] Citation Number: %s' % person_3_v2_citation_number)

            # PERSON #4 - MOTORIST / NON-MOTORIST / OCCUPANT V2 (Scanned higher on subsequent pages)
            #
            # Unit         <Box llx == "34.56" and lly == "126.43" urx="39.01" ury="134.43"> Sometimes Unit & Name
            # Name         <Box llx == "70.70" and lly == "126.58" and urx == "133.65" and ury == "134.57">
            # DOB          <Box llx == "384.05" and lly == "142.63" and urx == "418.79" and ury == "146.63">
            # Age          <Box llx == "483.70" and lly == "126.65" and urx == "492.59" and ury == "134.65">
            # Gender       <Box llx == "519.19" and lly == "130.46" and urx == "525.29" and ury == "140.46">
            # Address      <Box llx == "35.35" and lly == "99.07" and urx == "161.13" and ury == "107.07">
            # Phone        <Box llx == "420.84" and lly == "99.58" and urx == "470.64" and ury == "107.57">
            # Injuries     <Box llx == "40.32" and lly == "159.91" and urx == "45.88" and ury == "169.91">
            # EMS          ?
            # Air Bag      <Box llx == "486.58" and lly == "76.97" and urx == "492.14" and ury == "86.97">
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # Person #4v2 Unit Number or UN & Name
            if llx == "34.56" and lly == "126.43":
                logging.debug('\nPerson #4v2')
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    check_if_just_unit = blah.split(' ')
                    if len(check_if_just_unit) == 1:
                        # Only unit number
                        person_4_v2_unit_number = check_if_just_unit[0]
                        report_object['person']['8']['unit_number'] = person_4_v2_unit_number
                        logging.debug('[P4v2] Unit Number Only: %s' % person_4_v2_unit_number)

                    else:
                        # Both unit number & name
                        blah = blah.split(',')
                        person_4_v2_unit_number = blah[0][:1]
                        report_object['person']['8']['unit_number'] = person_4_v2_unit_number
                        logging.debug('[P4v2] Unit Number: %s' % person_4_v2_unit_number)

                        if len(blah) == 3:
                            person_4_v2_full_name = blah[0][2:] + ',' + blah[1] + ',' + blah[2]
                            report_object['person']['8']['full_name'] = person_4_v2_full_name
                            logging.debug('[P4v2] Full Name: %s' % person_4_v2_full_name)
                            person_4_v2_first_name = blah[1].strip()
                            report_object['person']['8']['first_name'] = person_4_v2_first_name
                            logging.debug('[P4v2] First Name: %s' % person_4_v2_first_name)
                            person_4_v2_middle_name = blah[2].strip()
                            report_object['person']['8']['middle_name'] = person_4_v2_middle_name
                            logging.debug('[P4v2] Middle Name: %s' % person_4_v2_middle_name)
                            person_4_v2_last_name = blah[0][2:]
                            report_object['person']['8']['last_name'] = person_4_v2_last_name
                            logging.debug('[P4v2] Last Name: %s' % person_4_v2_last_name)

                        elif len(blah) == 2:
                            person_4_v2_full_name = blah[0][2:] + ',' + blah[1]
                            report_object['person']['8']['full_name'] = person_4_v2_full_name
                            logging.debug('[P4v2] Full Name: %s' % person_4_v2_full_name)
                            person_4_v2_first_name = blah[1].strip()
                            report_object['person']['8']['first_name'] = person_4_v2_first_name
                            logging.debug('[P4v2] First Name: %s' % person_4_v2_first_name)
                            logging.debug('[P4v2] Middle Name: N/A')
                            person_4_v2_last_name = blah[0][2:]
                            report_object['person']['8']['last_name'] = person_4_v2_last_name
                            logging.debug('[P4v2] Last Name: %s' % person_4_v2_last_name)

                        else:
                            person_4_v2_unknown_name = blah[0][2:]
                            report_object['person']['8']['last_name'] = person_4_v2_unknown_name
                            logging.debug('[P4v2] Unknown Name Format: %s' % person_4_v2_unknown_name)

            # Person #4v2 Name (if not included with unit number above)
            if llx == "70.70" and lly == "126.58":
                for line in box.iter('Line'):
                    blah = line.find('Text').text
                    blah = blah.split(',')

                    if len(blah) == 3:
                        person_4_v2_full_name = blah[0] + ',' + blah[1] + ',' + blah[2]
                        report_object['person']['8']['full_name'] = person_4_v2_full_name
                        logging.debug('[P4v2] Full Name: %s' % person_4_v2_full_name)
                        person_4_v2_first_name = blah[1].strip()
                        report_object['person']['8']['first_name'] = person_4_v2_first_name
                        logging.debug('[P4v2] First Name: %s' % person_4_v2_first_name)
                        person_4_v2_middle_name = blah[2].strip()
                        report_object['person']['8']['middle_name'] = person_4_v2_middle_name
                        logging.debug('[P4v2] Middle Name: %s' % person_4_v2_middle_name)
                        person_4_v2_last_name = blah[0]
                        report_object['person']['8']['last_name'] = person_4_v2_last_name
                        logging.debug('[P4v2] Last Name: %s' % person_4_v2_last_name)

                    elif len(blah) == 2:
                        person_4_v2_full_name = blah[0] + ',' + blah[1]
                        report_object['person']['8']['full_name'] = person_4_v2_full_name
                        logging.debug('[P4v2] Full Name: %s' % person_4_v2_full_name)
                        person_4_v2_first_name = blah[1].strip()
                        report_object['person']['8']['first_name'] = person_4_v2_first_name
                        logging.debug('[P4v2] First Name: %s' % person_4_v2_first_name)
                        logging.debug('[P4v2] Middle Name: N/A')
                        person_4_v2_last_name = blah[0]
                        report_object['person']['8']['last_name'] = person_4_v2_last_name
                        logging.debug('[P4v2] Last Name: %s' % person_4_v2_last_name)

                    else:
                        person_4_v2_unknown_name = blah[0]
                        report_object['person']['8']['last_name'] = person_4_v2_unknown_name
                        logging.debug('[P4v2] Unknown Name Format: %s' % person_4_v2_unknown_name)

            # Person #4v2 DOB
            if llx == "384.05" and lly == "142.63":
                for line in box.iter('Line'):
                    person_4_v2_dob = line.find('Text').text
                    report_object['person']['8']['dob'] = person_4_v2_dob
                    logging.debug('[P4v2] DOB: %s' % person_4_v2_dob)

            # Person #4v2 Age
            if llx == "483.70" and lly == "126.65":
                for line in box.iter('Line'):
                    person_4_v2_age = line.find('Text').text
                    report_object['person']['8']['age'] = person_4_v2_age
                    logging.debug('[P4v2] Age: %s' % person_4_v2_age)

            # Person #4v2 Gender
            if llx == "519.19" and lly == "130.46":
                for line in box.iter('Line'):
                    person_4_v2_gender = line.find('Text').text
                    report_object['person']['8']['gender'] = person_4_v2_gender
                    logging.debug('[P4v2] Gender: %s' % person_4_v2_gender)

            # Person #4v2 Address
            if llx == "35.35" and lly == "99.07":
                i = 0
                for line in box.iter('Line'):
                    if i == 0:
                        person_4_v2_address = line.find('Text').text
                        report_object['person']['8']['address'] = person_4_v2_address
                        logging.debug('[P4v2] Address: %s' % person_4_v2_address)

                        # Get zip code
                        person_4_v2_zip = re.search(r'.*(\d{5}(-\d{4})?)$', person_4_v2_address)
                        report_object['person']['8']['zip'] = str(person_4_v2_zip.groups()[0])
                        logging.debug('[P4v2] Zip Code: %s' % str(person_4_v2_zip.groups()[0]))
                    elif i == 1:
                        # Phone number?
                        person_4_v2_phone = line.find('Text').text
                        report_object['person']['8']['phone'] = person_4_v2_phone
                        logging.debug('[P4v2] Phone: %s' % person_4_v2_phone)

                    i = i + 1

            # Person #4v2 Phone
            if llx == "420.84" and lly == "99.58":
                for line in box.iter('Line'):
                    person_4_v2_phone = line.find('Text').text
                    report_object['person']['8']['phone'] = person_4_v2_phone
                    logging.debug('[P4v2] Phone: %s' % person_4_v2_phone)

            # Person #4v2 Injuries
            if llx == "40.32" and lly == "159.91":
                for line in box.iter('Line'):
                    person_4_v2_injuries = line.find('Text').text[:1]  # This removes possible Injured Taken By
                    report_object['person']['8']['injuries'] = person_4_v2_injuries
                    logging.debug('[P4v2] Injuries: %s' % person_4_v2_injuries)

            # Person #4v2 Air Bag
            if llx == "486.58" and lly == "76.97":
                for line in box.iter('Line'):
                    person_4_v2_air_bag = line.find('Text').text
                    report_object['person']['8']['air_bag'] = person_4_v2_air_bag
                    logging.debug('[P4v2] Air Bag: %s' % person_4_v2_air_bag)

            # Person #4v2 Offense Charged
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_v2_offense_charged = line.find('Text').text
                    report_object['person']['8']['offense_charged'] = person_4_v2_offense_charged
                    logging.debug('[P4v2] Offense Charged: %s' % person_4_v2_offense_charged)

            # Person #4v2 Offense Description
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_v2_offense_description = line.find('Text').text
                    report_object['person']['8']['offense_description'] = person_4_v2_offense_description
                    logging.debug('[P4v2] Offense Description: %s' % person_4_v2_offense_description)

            # Person #4v2 Citation Number
            if llx == "NO_EXAMPLE" and lly == "NO_EXAMPLE":
                for line in box.iter('Line'):
                    person_4_v2_citation_number = line.find('Text').text
                    report_object['person']['8']['citation_number'] = person_4_v2_citation_number
                    logging.debug('[P4v2] Citation Number: %s' % person_4_v2_citation_number)

            # Person #1 - OCCUPANT / WITNESS ADDENDUM v1
            #
            # Unit         ... Sometimes Unit & Name
            # Name         ...
            # DOB          ...
            # Age          ...
            # Gender       ...
            # Address      ...
            # Phone        ...
            # Injuries     ...
            # EMS          ?
            # Air Bag      ...
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # ...

            # Person #2 - OCCUPANT / WITNESS ADDENDUM
            #
            # Unit         ... Sometimes Unit & Name
            # Name         ...
            # DOB          ...
            # Age          ...
            # Gender       ...
            # Address      ...
            # Phone        ?
            # Injuries     ...
            # EMS          ?
            # Air Bag      ...
            # Offense Crgd N/A
            # Offense Desc N/A
            # Citation Num N/A

            # ...
    except:
        return False

    logging.debug('Finished iterating over XML in %s\n\n' % xml_file_location)
    return report_object


def run_tet(pdf_file_path, file_path):
    if pdf_file_path != 'ERROR' and pdf_file_path != '':
        xml_file_path = '%s/digital_extracts' % file_path
        os.makedirs(xml_file_path, exist_ok=True)  # Create path if it doesn't exist
        xml_file_name = pdf_file_path.replace(file_path, '')
        xml_file_name = xml_file_name.replace('/', '')
        xml_file_name = xml_file_name.replace('pdf', 'xml')
        xml_file_location = '%s/%s' % (xml_file_path, xml_file_name)

        # Check if file exists
        if not os.path.exists(xml_file_location):
            # Extract PDF data into XML
            call(["tet", "--outfile", xml_file_name, "--targetdir", xml_file_path, "--tetml", "line", pdf_file_path], shell=False)
            logging.info('%s was OCR\'d' % xml_file_name)

        return [pdf_file_path, xml_file_location]
    else:
        return False

if __name__ == "__main__":
    # test ocr without running scanner/downloader
    get_xml_info('/srv/service/crashleads/worker/reports/2017/03/30/digital_extracts/digital_report_6280567.xml')
