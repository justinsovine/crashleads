#!/bin/bash

phantomjs --webdriver='127.0.0.1:4444' --load-images='false' --ignore-ssl-errors='true'

#nohup phantomjs --webdriver='127.0.0.1:4444' --load-images='false' --ignore-ssl-errors='true' &