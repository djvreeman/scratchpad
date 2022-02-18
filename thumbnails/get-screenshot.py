#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.error
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import base64
import sys
import os
import errno
import argparse
import re

#   The website's URL as an Input
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", help="enter site URL", default="http://hl7.org/fhir/")
args = parser.parse_args()
site = args.s
sitename = site.removeprefix('https://')
sitename = sitename.removeprefix('http://')
sitename = sitename.removesuffix('/')
sitename = sitename.replace('/','-')
print (site)
print (sitename)
#   The Google API.  Remove "&strategy=mobile" for a desktop screenshot
api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?&url=" + urllib.parse.quote(site)

#   Get the results from Google
print (api)

try:
    # site_data = json.load(urllib.request.urlopen(api))
    req = urllib.request.Request(url=api, method='GET')
    r = urllib.request.urlopen(req)
    dataJSON = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
except urllib.error.URLError:
    print ("Unable to retreive data")
    sys.exit()

# dl image
screen = dataJSON['lighthouseResult']['audits']['final-screenshot']['details']['data']
#response2 = request.urlopen(screen)
req2 = urllib.request.Request(url=screen, method='GET')
r2 = urllib.request.urlopen(req2)
with open(sitename + '-final-screenshot.jpg', 'wb') as f:
    f.write(r2.file.read())
    f.close()
