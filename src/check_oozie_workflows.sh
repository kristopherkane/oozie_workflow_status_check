#!/usr/bin/env bash
#
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
HOST=`echo $1 | tr '[:upper:]' '[:lower:]'`
PORT=$2
JAVA_HOME=$3
SEC_ENABLED=$4
if [[ "$SEC_ENABLED" == "true" ]]; then
  NAGIOS_KEYTAB=$5
  NAGIOS_USER=$6
  KINIT_PATH=$7
  TIME_RANGE=$8
  HISTORY_LENGTH=$9
  out1=`${KINIT_PATH} -kt ${NAGIOS_KEYTAB} ${NAGIOS_USER} 2>&1`
  if [[ "$?" -ne 0 ]]; then
    echo "CRITICAL: Error doing kinit for nagios [$out1]";
    exit 2;
  fi
else
  TIME_RANGE=$5
  HISTORY_LENGTH=$6
fi
out=`python $( dirname ${BASH_SOURCE[0]} )/check_oozie_workflows.py $HOST $PORT $SEC_ENABLED $TIME_RANGE $HISTORY_LENGTH 2>&1`;
rc=$?;
echo $out;
exit $rc;