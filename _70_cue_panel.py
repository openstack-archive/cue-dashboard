###############################################################################
# (c) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#     This software is the confidential and proprietary information of Hewlett
#     Packard Company. ("Confidential Information").  You shall not
#     disclose such Confidential Information and shall use it only in
#     accordance with the terms of the license agreement you entered into
#     with Hewlett-Packard.
###############################################################################

# The name of the panel to be added to HORIZON_CONFIG. Required.
# Should match devplatforminstaller.utils.const.PANEL
PANEL = 'queues'

# The name of the panel group the PANEL is associated with. Required.
# Must match devplatforminstaller.utils.const.PANEL_GROUP
PANEL_GROUP = 'queues'

# The name of the dashboard the PANEL associated with. Required.
# Must match devplatforminstaller.utils.const.PANEL_GROUP_DASHBOARD
PANEL_DASHBOARD = 'project'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'cuedashboard.queues.panel.CuePanel'

# Whether or not the panel is disabled.
# DISABLED = False

# Add the devplatforminstaller app into the list of applications to run.
ADD_INSTALLED_APPS = [
    'cuedashboard',
]
