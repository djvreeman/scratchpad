#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    
import json
import subprocess
import re
import datetime
import csv
import pysftp
import sys
import urllib
import codecs
import gzip
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# Setup some variables
currentDT = datetime.datetime.now()
locationID = "4497290"
apikey = '{your API key}'
unitsUS = "imperial"
urlData = "api.openweathermap.org/data/2.5/weather?id={id}}&appid={appid}}&units=imperial"

serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"
url = serviceUrl + urllib.parse.urlencode({'id': locationID, 'APPID': apikey, 'units': unitsUS})

# Lets get the current temps from openweathermap
r = urllib.request.urlopen(url)
dataJSON = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

temp_f = float(dataJSON['main']['temp'])

# Now get tortoise temp from the USB temp device
output = subprocess.check_output('/usr/local/bin/temper-poll', stderr=subprocess.STDOUT).decode('utf-8')
pattern = "([+-]?\d+(\.\d+)*)\s?°([Ff])"
tort_temp = re.search('([+-]?\d+(\.\d+)*)\s?°([Ff])', output)
temps =  str(temp_f) + ',' + tort_temp.group(1) + ',' + str(currentDT)
outsideTemp = str(temp_f)
tortTemp = tort_temp.group(1)
currentDateTime = str(currentDT)
tempsRow = [outsideTemp,tortTemp,currentDateTime]
print(temps)

# write out the data to a local csv   
tempWriter = open('/home/pi/temperature/tort_temps-2021.csv', 'a')
tempWriter.write("%s,%s,%s\n" % (outsideTemp,tortTemp,currentDateTime))
tempWriter.close()

#sFTP transfer of CSV file
remote_file = "/home/pi/temperature/tort_temps-2021.csv"
cnopts = pysftp.CnOpts(knownhosts='/home/pi/temperature/known_hosts')
cnopts.hostkeys = None

with pysftp.Connection(host="{yourhost}", username="{username}", password="{passwd}}",cnopts=cnopts) as sftp:
    with sftp.cd('/var/www/main'):
#    with sftp.cd('/home/dvreeman/tmp'):
	    sftp.put(remote_file)
	# Closes the connection
    sftp.close()
sys.exit()
