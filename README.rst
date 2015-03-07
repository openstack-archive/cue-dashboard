cue-dashboard
===============

Horizon plugin for Project Cue

Cue-dashboard Install
--------------------------------------------

Enter these commands in your terminal
::

 sudo pip install -e {cue-dashboard}
 cd /opt/stack/horizon/openstack_dashboard/local/enabled
 ln -s {cue-dashboard}/_70_0_cue_panel_group.py _70_0_cue_panel_group.py
 ln -s {cue-dashboard}/_70_cue_panel.py _70_cue_panel.py
 sudo service apache2 restart