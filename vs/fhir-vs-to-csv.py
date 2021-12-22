#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Overview:
#
# This simple script calls a FHIR Terminology Services API to $expand a ValueSet and converts the expansion to a CSV file saved on the file system.
# Currently this only supports open FHIR servers and those using basic authentication.
# Default server is NLM's VSAC
#
# Example usage:
# python3 fhir-vs-to-csv.py -u "apikey" -vs "2.16.840.1.113762.1.4.1247.1"


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

# Get Command Line Arguments

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u', '--username', help='Specify username',
    default=getpass.getuser())
parser.add_argument("-vs", help="enter \"id\" of the Valueset", required=True)
parser.add_argument("-s", help="enter service base URL of the Valueset", default="https://cts.nlm.nih.gov/fhir/")
args = parser.parse_args()
password = getpass.getpass("Remote Password (or skip for no auth): ")

if args.vs:
    vsName = args.vs
fhirServer = args.s

# Setup some variables
resource = "ValueSet"
vsOutput = vsName + ".csv"
vsOperation = "$expand"
vsFormat = "_format=json"
fhirHeader = {}
fhirHeader['Content-Type'] = "application/fhir+json;charset=utf-8"
# VSAC doesn't like the _format parameter
# fhirUrl = fhirServer + resource + '/' + vsName + '/' + vsOperation + '?' + vsFormat

fhirUrl = fhirServer + resource + '/' + vsName + '/' + vsOperation
print(fhirUrl)

# Lets get the Valueset (expecting JSON from the server)

# create an authorization handler if needed

if password:
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, fhirServer, args.username, password)

    auth_handler = urllib.request.HTTPBasicAuthHandler(p)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url=fhirUrl, headers=fhirHeader, method='GET')
    r = opener.open(req)
else:
    req = urllib.request.Request(url=fhirUrl, headers=fhirHeader, method='GET')
    r = urllib.request.urlopen(req)

dataJSON = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

# it's nice to see some summary on the commandline
try: 
    vsName = 'Name: ' + dataJSON['name']
except:
    vsName = 'Name: '
else:
    print (vsName)
try:
    vsDate = 'Date: ' + dataJSON['date']
except:
    vsName = 'Date: '
else:
    print (vsDate)
try:
    expansionTotal = 'Total: ' + str(dataJSON['expansion']['total'])
except:
    vsName = 'Total: '
else:
    print (expansionTotal)

# ok, now write out to the CSV file
    
with open(vsOutput, mode='w') as csv_file:
    csvWriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for concept in dataJSON['expansion']['contains']:
        try: 
            version = concept["version"]
            csvWriter.writerow([concept["code"],concept["display"],concept["system"],concept["version"]])
        except:
            csvWriter.writerow([concept["code"],concept["display"],concept["system"]])
