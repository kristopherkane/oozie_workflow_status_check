###Hortonworks Data Platform 2.1 Nagios Plugin - Oozie Workflow Status

This plugin will identify and alert the status of Oozie workflows.

![Ambari Oozie Nagios Screenshot](/images/ambari-oozie.png "Ambari Oozie Nagios Screenshot")
![Nagios Screenshot](/images/nagios-oozie.png "Nagios Oozie Screenshot")

###News
Updated for HDP 2.1 Nagios integration.
This plugin now only reports on a fixed number of jobs in the past that meet time range criteria specified by the admin.

###Dependencies
With the Kerberos integration, the Python source will need two new packages installed on the Nagios server.
python-kerberos (CentOS Base)
python-urllib2_kerberos (EPEL)
For Timezone handling:
pytz (CentOS Base)


###Tested
HDP 2.1

###Installation
All actions are conducted on the HDP2 Nagios server

**Read Carefully** -- The only files that should be added are check_oozie_workflows{.py,.sh}.  The other files are configurations that should be added to the existing HDP2 Ambari configuration.

1. Add [check_oozie_workflows.py](/src/check_oozie_workflows.py) and [check_oozie_workflows.sh](/src/check_oozie_workflows.sh)  to the Ambari agent Puppet module files directory at: /var/lib/ambari-agent/puppet/modules/hdp-nagios/files/
2. Add the additional configuration within the existing Oozie if conditional in file [hadoop-services.cfg.erb](/ambari/templates/hadoop-services.cfg.erb) to: /var/lib/ambari-agent/puppet/modules/hdp-nagios/templates/hadoop-services.cfg.erb

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
#Oozie workflow check
define service {
        hostgroup_name          oozie-server
        use                     hadoop-service
        service_description     OOZIE::Oozie Workflow status
        servicegroups           OOZIE
        {% if security_enabled %}
        check_command           check_oozie_workflows!{{ oozie_server_port }}!{{ java64_home }}!true!{{ nagios_keytab_path }}!{{ nagios_principal_name }}!{{ kinit_path_local }}
        {% else %}
        check_command           check_oozie_workflows!{{ oozie_server_port }}!{{ java64_home }}!false
        {% endif %}
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
1. ~~Filter workflows based on x minutes in the past~~
2. ~~Add option to pull x number of workflows.  Currently, it pulls the default of 50.~~
3. ~~Integrate with Kerberos~~
4. Filter workflows based on user
5. Filter workflows based on name matching
