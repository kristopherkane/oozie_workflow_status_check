#Add the following line below the current Oozie check to the config.pp
#Puppet will use these definitions to push the files to their destination
#This definition should go on the Nagios host at: /var/lib/ambari-agent/puppet/modules/hdp-nagios/manifests/server/config.pp
#Place this below the other oozie line
#DO NOT overwrite the entire file with this one.
hdp-nagios::server::check { 'check_oozie_workflows.sh': }
hdp-nagios::server::check { 'check_oozie_workflows.py': }
