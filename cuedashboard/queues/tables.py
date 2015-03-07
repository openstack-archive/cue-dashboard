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

import logging
from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext as _
from horizon import tables
from cuedashboard import api


LOG = logging.getLogger(__name__)


class CreateQueue(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Cluster")
    url = "horizon:project:queues:create"
    classes = ("ajax-modal", "btn-create")


class DeleteQueue(tables.BatchAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Terminate Instance",
            u"Terminate Instances",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Scheduled deletion of Queue",
            u"Scheduled deletion of Queues",
            count
        )

    name = "delete"
    classes = ("btn-danger", )
    icon = "off"

    def action(self, request, obj_id):
        api.trove.instance_delete(request, obj_id)


class QueuesTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link='horizon:project:queues:detail')
    size = tables.Column("size", verbose_name=_("Size"),)
    flavor = tables.Column("flavor", verbose_name=_("Flavor"),)
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, datum):
        LOG.info(type(datum))
        LOG.info(dir(datum))
        return None

    class Meta:
        name = "queues"
        verbose_name = _("Queues")
        table_actions = (CreateQueue, DeleteQueue,)
        row_actions = (DeleteQueue,)
