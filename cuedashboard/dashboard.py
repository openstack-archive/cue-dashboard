from django.utils.translation import ugettext as _
from cuedashboard.queues.panel import CuePanel
import horizon


class CueDashboard(horizon.Dashboard):
    name = _("Cue")
    slug = "cue"
    panel = (CuePanel,)
    default_panel = 'queues'

CueDashboard.register(CuePanel)
horizon.register(CueDashboard)
