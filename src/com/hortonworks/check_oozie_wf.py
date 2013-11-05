#!/usr/bin/env python

import sys
import urllib
import json
import time
import datetime

host = sys.argv[1]
port = sys.argv[2]
uri = "http://" + host + ":" + port + "/oozie/v1/jobs"
try:
    raw_json = urllib.urlopen(uri)
except:
    print "Error connecting to the Oozie server"
    sys.exit(1)

json_object = json.load(raw_json)


for job in json_object[u'workflows']:
    row = [job[u'id'], job[u'appName'], job[u'status'], job[u'endTime']]
    print row


    '''
    print job[u'status'], job[u'endTime']
    dtg = job[u'endTime'].replace(",", "")
    name = job[u'appName']
    mytime = time.strptime(dtg, "%a %d %b %Y %X %Z")
    newtime = time.strftime("%B", mytime)
    print newtime
    print name
    print job[u'id']
    '''