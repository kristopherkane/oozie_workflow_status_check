#Add the following to the bottom of "def nagios_server_config()"
nagios_server_check( 'check_oozie_workflows.sh' )
nagios_server_check( 'check_oozie_workflows.py' )