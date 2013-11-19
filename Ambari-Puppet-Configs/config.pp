#Add the following line below the current Oozie check to the config.pp
hdp-nagios::server::check { 'check_oozie_workflows.py': }
