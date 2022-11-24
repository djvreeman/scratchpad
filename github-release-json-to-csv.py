#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Overview:
#
# This script reads in a Git JSON export of a repo's release history, and 
# and exports a CSV with the release tag, published date, and author

# Usage:
# cd '/Users/dvreeman/odrive/Encryptor/B2/Documents/Work/HL7/Stats and Data Tracking'
# python3 github-release-json-to-csv.py -i SoftwareReleases/publisher-releases.json -o SoftwareReleases/publisher-releases.csv


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import getopt
import re    
import json
import csv
import sys
import urllib
import argparse
import getpass
from datetime import datetime

#Get Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="file name of input JSON file", required=True)
parser.add_argument("-o", help="file name of output CSV file", required=True)
#parser.add_argument("-r", help="name of GitHub repo e.g. fhir-ig-publisher", required=True)

args = parser.parse_args()

# Setup file names 
JsonInputFileName = args.i
csvOutputFileName = args.o
#repo = args.r

# Setup some variables
#params = "?_fields=title,date&per_page=100&order=asc&page="
dataOutput = csvOutputFileName
#fhirHeader = {}
#fhirHeader['Content-Type'] = "application/fhir+json;charset=utf-8"
#serverUrl = server + '/' + params + page 
#print(serverUrl)

# Lets get the Github JSON File

with open(JsonInputFileName) as user_file:
  file_contents = user_file.read()
  
#print(file_contents)

dataJSON = json.loads(file_contents)
#dataJSON = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

with open(dataOutput, mode='w') as csv_file:
    csvWriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for release in dataJSON:
        try: 
            releaseDate = release["published_at"]
            releaseName = release["name"]
            # "published_at": "2022-11-22T15:04:31Z",
            datetimeobj=datetime.strptime(releaseDate, "%Y-%m-%dT%H:%M:%SZ")
            simpleDate = datetimeobj.date()
            #simpleDateMonth = simpleDate.strftime('%Y %m')
            #print (simpleDate)
            releaseTag = release["tag_name"]
            releaseBranch = release["target_commitish"]
            csvWriter.writerow([releaseDate,simpleDate,releaseName,releaseTag,releaseBranch])
        except:
            releaseDate = release["published_at"]
            releaseName = release["name"]
            csvWriter.writerow([releaseDate,releaseName])