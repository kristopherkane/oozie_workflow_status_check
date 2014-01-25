#!/usr/bin/env python

################################################
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
################################################

"""
This requires python-kerberos (CentOS Base) and python-urllib2_kerberos (EPEL)
root@box>yum install python-kerberos python-urllib2_kerberos
"""

import sys
import urllib
import json
import time
import datetime
from time import gmtime, strftime
import urllib2_kerberos
import urllib2

#get current timezone - This assumes Oozie has been setup for the system timezone
tz = strftime("%Z", gmtime())
try:
    host = sys.argv[1]
    port = sys.argv[2]
    kinit_truth = sys.argv[3]
except:
    print "Arguments to check script are wrong"
    print "Expecting [1] host [2] port [3] kerberos ruth (true|false)"
    sys.exit(2)

uri = "http://" + host + ":" + port + "/oozie/v1/jobs?jobType=wf&timezone=%s" % (tz)

failed_count = 0
suspended_count = 0
killed_count = 0
succeeded_count = 0
prep_count = 0
running_count = 0
workflows = []

#If Kerberos, use urllib2/urllib2_kerberos, if not, use urllib

if kinit_truth == "true":
    try:
        opener = urllib2.build_opener()
        opener.add_handler(urllib2_kerberos.HTTPKerberosAuthHandler())
        resp = opener.open(uri)
        a = resp.read()

        #Create a JSON object
    except:
        print "Error connecting to the Oozie server with kerberos"
        sys.exit(2)
    #Create a JSON object
    try:
        json_object = json.loads(a)
    except:
        print "Error parsing the JSON from Oozie"
        sys.exit(2)
else:
    try:
        raw_json = urllib.urlopen(uri)
    except:
        print "Error connecting to the Oozie server"
        sys.exit(2)

    #Create a JSON object
    try:
        json_object = json.load(raw_json)
    except:
        print "Error parsing the JSON from Oozie"
        sys.exit(2)

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

    elif workflow[2] == "PREP":
        prep_count += 1

    elif workflow[2] == "RUNNING":
        running_count += 1

total = failed_count + suspended_count + killed_count + succeeded_count + prep_count + running_count

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
