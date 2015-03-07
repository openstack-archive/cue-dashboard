from django.utils.translation import ugettext_lazy as _

# The name of the panel group to be added to HORIZON_CONFIG. Required.
# Must match devplatforminstaller.utils.const.PANEL_GROUP
PANEL_GROUP = 'queues'

# The display name of the PANEL_GROUP. Required.
# Should match devplatforminstaller.utils.const.PANEL_GROUP_DASHBOARD
PANEL_GROUP_NAME = _('Message Queues')

# The name of the dashboard the PANEL_GROUP associated with. Required.
# Must match devplatforminstaller.utils.const.PANEL_GROUP_DASHBOARD
PANEL_GROUP_DASHBOARD = 'project'