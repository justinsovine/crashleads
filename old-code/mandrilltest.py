#!/usr/bin/env python

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart('alternative')

msg['Subject'] = "Hello from Mandrill, Python style!"
msg['From']    = "Justin Sovine <jsovine@smagno.com>" # Your from name and email address
msg['To']      = "justinsovine@gmail.com"

text = "Mandrill speaks plaintext"
part1 = MIMEText(text, 'plain')

html = "<em>Mandrill speaks <strong>HTML</strong></em>"
part2 = MIMEText(html, 'html')

username = os.environ['grabreports@smagno.com']
password = os.environ['W9qNf7N2JPjLjjcjJM7QMQ']

msg.attach(part1)
msg.attach(part2)

s = smtplib.SMTP('smtp.mandrillapp.com', 587)

s.login(username, password)
s.sendmail(msg['From'], msg['To'], msg.as_string())

s.quit()
