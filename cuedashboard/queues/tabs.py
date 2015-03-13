from django.utils.translation import ugettext_lazy as _
from horizon import tabs


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "project/queues/_detail_overview.html"

    def get_context_data(self, request):
        return {"cluster": self.tab_group.kwargs['cluster']}


class ClusterDetailTabs(tabs.TabGroup):
    slug = "cluster_details"
    tabs = (OverviewTab,)
    sticky = True
