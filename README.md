###Hortonworks Data Platform 2 Nagios Plugin - Oozie Workflow Status

This plugin will identify and alert the status of Oozie workflows.

(https://github.com/kristopherkane/images/ambari-oozie.png "Ambari Oozie Nagios Screenshot")

###Assumptions
Oozie has been configured with the same timezone as the host server.  This can be achieved with the oozie-site.xml parameter of: oozie.processing.timezone
Example for Eastern Standard Time:
>oozie.processing.timezone = GMT-0500

###Installation
All actions are conducted on the HDP2 Nagios server
1. Add [check_oozie_workflows.py](/src//com/kane/check_oozie_workflows.py) to the Ambari agent Puppet module files directory at: /var/lib/ambari-agent/puppet/modules/hdp-nagios/files/
2. Add the additional configuration in [hadoop-services.cfg.erb](/Ambari-Puppet-Configs/hadoop-services.cfg.erb) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/templates/hadoop-services.cfg.erb
3. Add the additional configuration in [hadoop-commands.cfg.erb](/Ambari-Puppet-Configs/hadoop-commands.cfg.erb) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/templates/hadoop-commands.cfg.erb
4. Add the additional configuratio in [config.pp](/Ambari-Puppet-Configs/config.pp) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/manifests/server/config.pp
5. Restart Nagios via Ambari


####Alert Translations

Oozie Status   |  Script Exit Code |  Nagios Level
FAILED              2                   CRITICAL
KILLED              1                   WARNING
SUSPENDED           1                   WARNING
SUCCEEDED           0                   OK
<all others>        0                   OK

###TODO
1. Filter workflows based on x minutes in the past
2. Add option to pull x number of workflows.  Currently, it pulls the default of 50.