# Copyright 2013 Rackspace Hosting
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon.utils import memoized
from horizon import workflows
from openstack_dashboard import api
from cuedashboard.api import cluster_create

from openstack_dashboard.dashboards.project.instances \
    import utils as instance_utils


LOG = logging.getLogger(__name__)


class SetInstanceDetailsAction(workflows.Action):
    name = forms.CharField(max_length=80, label=_("Cluster Name"))
    flavor = forms.ChoiceField(label=_("Flavor"),
                               help_text=_("Size of image to launch."))
    size = forms.IntegerField(label=_("Size"),
                              min_value=0,
                              initial=1,
                              help_text=_("Size of cluster."))
    volume = forms.IntegerField(label=_("Volume Size"),
                                min_value=0,
                                initial=1,
                                help_text=_("Size of the volume in GB."))

    class Meta(object):
        name = _("Details")
        help_text_template = "queues/_launch_details_help.html"

    @memoized.memoized_method
    def flavors(self, request):
        try:
            return api.nova.flavor_list(request)
        except Exception:
            LOG.exception("Exception while obtaining flavors list")
            redirect = reverse("horizon:project:queues:index")
            exceptions.handle(request,
                              _('Unable to obtain flavors.'),
                              redirect=redirect)

    def populate_flavor_choices(self, request, context):
        flavors = self.flavors(request)
        if flavors:
            return instance_utils.sort_flavor_list(request, flavors)
        return []


class SetClusterDetails(workflows.Step):
    action_class = SetInstanceDetailsAction
    contributes = ("name", "volume", "flavor", "size")


class SetNetworkAction(workflows.Action):
    network = forms.MultipleChoiceField(label=_("Networks"),
                                        widget=forms.CheckboxSelectMultiple(),
                                        error_messages={
                                            'required': _(
                                                "At least one network must"
                                                " be specified.")},
                                        help_text=_("Create cluster with"
                                                    " these networks"))

    def __init__(self, request, *args, **kwargs):
        super(SetNetworkAction, self).__init__(request, *args, **kwargs)
        network_list = self.fields["network"].choices
        if len(network_list) == 1:
            self.fields['network'].initial = [network_list[0][0]]

    class Meta(object):
        name = _("Networking")
        permissions = ('openstack.services.network',)
        help_text = _("Select networks for your cluster.")

    def populate_network_choices(self, request, context):
        try:
            tenant_id = self.request.user.tenant_id
            networks = api.neutron.network_list_for_tenant(request, tenant_id)
            network_list = [(network.id, network.name_or_id)
                            for network in networks]
        except Exception:
            network_list = []
            exceptions.handle(request,
                              _('Unable to retrieve networks.'))
        return network_list


class SetNetwork(workflows.Step):
    action_class = SetNetworkAction
    template_name = "queues/_launch_networks.html"
    contributes = ("network_id",)

    def contribute(self, data, context):
        if data:
            networks = self.workflow.request.POST.getlist("network")
            # If no networks are explicitly specified, network list
            # contains an empty string, so remove it.
            networks = [n for n in networks if n != '']
            if networks:
                # TODO
                # Choosing the first networks until Cue
                # supports more than one networks.
                context['network_id'] = networks[0]

        return context


class CreateCluster(workflows.Workflow):
    slug = "create_cluster"
    name = _("Create Cluster")
    finalize_button_name = _("Create")
    success_message = _('Created cluster named "%(name)s".')
    failure_message = _('Unable to create cluster named "%(name)s".')
    success_url = "horizon:project:queues:index"
    default_steps = (SetClusterDetails,
                     SetNetwork)

    def __init__(self, request=None, context_seed=None, entry_point=None,
                 *args, **kwargs):
        super(CreateCluster, self).__init__(request, context_seed,
                                            entry_point, *args, **kwargs)
        self.attrs['autocomplete'] = (
            settings.HORIZON_CONFIG.get('password_autocomplete'))

    def format_status_message(self, message):
        name = self.context.get('name', 'unknown cluster')
        return message % {"name": name}

    def handle(self, request, context):
        try:
            LOG.info("Launching message queue cluster with parameters "
                     "{name=%s, volume=%s, flavor=%s, size=%s, nics=%s}",
                     context['name'], context['volume'], context['flavor'],
                     context['size'], context['network_id'])

            cluster_create(request, context['name'], context['network_id'],
                           context['flavor'], context['size'],
                           context['volume'])
            return True
        except Exception:
            exceptions.handle(request)
            return False
