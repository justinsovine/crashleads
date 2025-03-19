# CrashLeads
*Lead generation service for chiropractors and lawyers*

Scrapes public records from Ohio Department of Public Safety website as 
PDF's in real-time 24/7, then scrapes the data into an XML file using TET, 
from which the information is found using positional XY coords and stored in 
a database where the information can be correlated and used via a portal, or 
by push/sms/email notifications. It makes use of PhantomJS as the browser 
using Selenium as the website makes heavy use of javascript and ASPX 
callbacks, or I would simply request pages using simple HTTP 1.1 GET 
requests.

This service netted me around $1000 a month for several years and is 
currently defunct..

Please view the sample-report.pdf for a sample of a crash report, and the 
sample-extract.xml to see what TET does to make the data accessible. The 
ohio-dps-website.aspx is a sample of what the front page of the website 
looked like code-wise.

### Sample Video of the Program Running

[![Watch the video](https://img.youtube.com/vi/gEcPmh-3lDY/0.jpg)](https://www.youtube.com/watch?v=gEcPmh-3lDY)


