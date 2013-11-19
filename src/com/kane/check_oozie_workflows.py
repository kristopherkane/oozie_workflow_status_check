#!/usr/bin/env python

import sys
import urllib
import json
import time
import datetime
from time import gmtime, strftime

#get current timezone - This assumes Oozie has been setup for the system timezone
tz = strftime("%Z", gmtime())
try:
    host = sys.argv[1]
    port = sys.argv[2]
except:
    print "Arguments to check script are wrong"
    sys.exit(2)

uri = "http://" + host + ":" + port + "/oozie/v1/jobs?jobType=wf&timezone=%s" % (tz)

failed_count = 0
suspended_count = 0
killed_count = 0
succeeded_count = 0
prep_count = 0
running_count = 0
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

#iterate through the workflows and get status
for workflow in workflows:
    if workflow[2] == "FAILED":
        failed_count += 1

    elif workflow[2] == "SUSPENDED":
        suspended_count += 1

    elif workflow[2] == "KILLED":
        killed_count += 1

    elif workflow[2] == "SUCCEEDED":
        succeeded_count += 1

    elif wofklow[2] == "PREP":
        prep_count += 1

    elif workflow[2] == "RUNNING":
        running_count += 1

total = failed_count + suspended_count + killed_count + succeeded_count

#Return exit codes based on counts - order by most severe descending
print "FAILED: %d KILLED: %d SUSPENDED: %d SUCCEEDED: %d RUNNING: %d PREP: %d Total: %d" % (
                                                                       failed_count,
                                                                       killed_count,
                                                                       suspended_count,
                                                                       succeeded_count,
                                                                       running_count,
                                                                       prep_count,
                                                                       total)
#Generate Nagios CRITICAL
if failed_count > 0:
    sys.exit(2)

#Generate Nagios WARNING
elif killed_count > 0 or suspended_count > 0:
    sys.exit(1)

#Generate Nagios OK
else:
    sys.exit(0)
