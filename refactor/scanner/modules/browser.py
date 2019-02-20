#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# Intellect37, LLC 2017 #
# # # # # # # # # # # # #

import os
import sys
import logging
import time  # Resolve this? Convert time -> datetime

# Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class BrowserController:

    def __init__(self):
        self.target = 'https://services.dps.ohio.gov/CrashRetrieval/OHCrashRetrieval.aspx'
        self.start_browser()

    def start_browser(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1366, 768)
        print('Started WebDriver => PhantomJS')
        return self.driver

    def stop_browser(self):
        self.driver.service.process.send_signal(signal.SIGTERM)
        self.driver.quit()

