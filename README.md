###Hortonworks Data Platform 2 Nagios Plugin - Oozie Workflow Status

This plugin will identify and alert the status of Oozie workflows.

![Ambari Oozie Nagios Screenshot](/images/ambari-oozie.png "Ambari Oozie Nagios Screenshot")
![Nagios Screenshot](/images/nagios-oozie.png "Nagios Oozie Screenshot")

###News
This HDP plugin now works with Kerberos enabled security!  It inherits much of the same properties as the built-in Oozie status check and so needs no new Ambari modifications.

###Dependencies
With the Kerberos integration, the Python source will need two new packages installed on the Nagios server.
python-kerberos (CentOS Base)
python-urllib2_kerberos (EPEL)

###Assumptions
Oozie has been configured with the same timezone as the host server.  This can be achieved with the oozie-site.xml parameter of: oozie.processing.timezone
Example for Eastern Standard Time:
>oozie.processing.timezone = GMT-0500

###Tested
HDP 1.3 (Kerberos)
HDP 2.0



###Installation
All actions are conducted on the HDP2 Nagios server

**Read Carefully** -- The only file that should be added is the check_oozie_workflows.py.  The other files are configurations that should be added to the existing HDP2 Puppet files.

1. Add [check_oozie_workflows.py](/src/com/kane/check_oozie_workflows.py) to the Ambari agent Puppet module files directory at: /var/lib/ambari-agent/puppet/modules/hdp-nagios/files/
2. Add the additional configuration within the existing Oozie if conditional in file [hadoop-services.cfg.erb](/Ambari-Puppet-Configs/hadoop-services.cfg.erb) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/templates/hadoop-services.cfg.erb

Example for hadoop-services.cfg.erb
```bash
<%if scope.function_hdp_nagios_members_exist('oozie-server')-%>
# Oozie check
define service {
        hostgroup_name          oozie-server
        use                     hadoop-service
        service_description     OOZIE::Oozie Server status
        servicegroups           OOZIE
        <%if scope.function_hdp_template_var("::hdp::params::security_enabled")-%>
        check_command           check_oozie_status!<%=scope.function_hdp_template_var("::hdp::oozie_server_port")%>!<%=scope.function_hdp_template_var("java64_home")%>!true!<%=scope.function_hdp_templat
e_var("nagios_keytab_path")%>!<%=scope.function_hdp_template_var("nagios_principal_name")%>!<%=scope.function_hdp_template_var("kinit_path_local")%>
        <%else-%>
        check_command           check_oozie_status!<%=scope.function_hdp_template_var("::hdp::oozie_server_port")%>!<%=scope.function_hdp_template_var("java64_home")%>!false
        <%end-%>
        normal_check_interval   1
        retry_check_interval    1
        max_check_attempts      3
}
# Oozie workflow check
define service {
        hostgroup_name          oozie-server
        use                     hadoop-service
        service_description     OOZIE::Oozie Workflow status
        servicegroups           OOZIE
        <%if scope.function_hdp_template_var("::hdp::params::security_enabled")-%>
        check_command           check_oozie_workflows!<%=scope.function_hdp_template_var("::hdp::oozie_server_port")%>!<%=scope.function_hdp_template_var("java64_home")%>!true!<%=scope.function_hdp_template_var("nagios_keytab_path")%>!<
%=scope.function_hdp_template_var("nagios_principal_name")%>!<%=scope.function_hdp_template_var("kinit_path_local")%>
        <%else-%>
        check_command           check_oozie_workflows!<%=scope.function_hdp_template_var("::hdp::oozie_server_port")%>!<%=scope.function_hdp_template_var("java64_home")%>!false
        <%end-%>
        normal_check_interval   1
        retry_check_interval    1
        max_check_attempts      3
}
<%end-%>
```

3. Add the additional configuration in [hadoop-commands.cfg.erb](/Ambari-Puppet-Configs/hadoop-commands.cfg.erb) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/templates/hadoop-commands.cfg.erb
4. Add the additional configuration in [config.pp](/Ambari-Puppet-Configs/config.pp) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/manifests/server/config.pp
5. Restart Nagios via Ambari


####Alert Translations

|Oozie Status   |  Script Exit Code |  Nagios Level |
| ------------- |:-----------------:|--------------:|
|FAILED         |     2             |    CRITICAL   |
|KILLED         |     1             |    WARNING    |
|SUSPENDED      |     1             |    WARNING    |
|SUCCEEDED      |     0             |    OK         |
|all others     |     0             |    OK         |

###TODO
1. Filter workflows based on x minutes in the past
2. Add option to pull x number of workflows.  Currently, it pulls the default of 50.
3. ~~Integrate with Kerberos~~
