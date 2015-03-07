# Copyright 2013 Rackspace Hosting.
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
from cueclient.v1 import client
from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v2

from openstack_dashboard.api import base

from horizon.utils.memoized import memoized  # noqa

LOG = logging.getLogger(__name__)


@memoized
def cueclient(request):
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    auth_url = base.url_for(request, 'identity')
    auth = v2.Token(auth_url, request.user.token.id,
                    tenant_id=request.user.tenant_id,
                    tenant_name=request.user.tenant_name)
    session = ksc_session.Session(auth=auth, verify=cacert)
    return client.Client(session=session)


def queue_list(request, marker=None):
    return cueclient(request).clusters.list()
