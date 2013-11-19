#!/usr/bin/env python

import sys
import urllib
import json
import time
import datetime
from time import gmtime, strftime

#get current timezone - This assumes Oozie has been setup for the system timezone
tz = strftime("%Z", gmtime())

host = sys.argv[1]
port = sys.argv[2]

uri = "http://" + host + ":" + port + "/oozie/v1/jobs?jobType=wf&timezone=%s" % (tz)

bad_status = ["FAILED", "SUSPENDED", "KILLED"]
good_status = ["SUCCEEDED"]

failed_count = 0
suspended_count = 0
killed_count = 0
succeeded_count = 0

workflows = []

try:
    raw_json = urllib.urlopen(uri)
except:
    print "Error connecting to the Oozie server"
    sys.exit(2)

#Create a JSON object
json_object = json.load(raw_json)

#iterate through the json and pull out the workflows
for job in json_object[u'workflows']:
    row = [job[u'id'], job[u'appName'], job[u'status'], job[u'endTime']]
    workflows.append(row)

#iterate through the workflows and find failed jobs
for workflow in workflows:
    if workflow[2] == "FAILED":
        failed_count += 1

    elif workflow[2] == "SUSPENDED":
        suspended_count += 1

    elif workflow[2] == "KILLED":
        killed_count += 1

    elif workflow[2] == "SUCCEEDED":
        succeeded_count += 1

#Return exit codes based on counts - order by most severe descending
if failed_count > 0:
    print "FAILED: %d Oozie workflow(s)" % (failed_count)
    sys.exit(2)

elif killed_count > 0:
    print "KILLED: %d Oozie workflow(s)" % (killed_count)
    sys.exit(1)

elif suspended_count > 0:
    print "SUSPENDED: %d Oozie workflow(s)" % (suspended_count)
    sys.exit(1)

elif succeeded_count > 0:
    print "OK: %d Oozie workflows succeeded" % (succeeded_count)
    sys.exit(0)

else:
    print "OK: No workflows identified"
    sys.exit(0)

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