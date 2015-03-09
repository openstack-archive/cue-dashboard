# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Authors: Steve Leon <kokhang@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copyright [2014] Hewlett-Packard Development Company, L.P.
# limitations under the License.

from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext as _
from horizon import tables
from cuedashboard import api


class CreateCluster(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Cluster")
    url = "horizon:project:queues:create"
    classes = ("ajax-modal", "btn-create")


class DeleteCluster(tables.BatchAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate Cluster",
            u"Terminate Clusters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Cluster",
            u"Scheduled deletion of Clusters",
            count
        )

    name = "delete"
    classes = ("btn-danger", )
    icon = "off"

    def action(self, request, obj_id):
        api.delete_cluster(request, obj_id)


class ClusterTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link='horizon:project:queues:detail')
    size = tables.Column("size", verbose_name=_("Size"),)
    flavor = tables.Column("flavor", verbose_name=_("Flavor"),)
    status = tables.Column("status", verbose_name=_("Status"))

    class Meta:
        name = "clusters"
        verbose_name = _("Clusters")
        table_actions = (CreateCluster, DeleteCluster,)
        row_actions = (DeleteCluster,)
