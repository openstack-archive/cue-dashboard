# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

from cueclient.v1 import client

from django.conf import settings
from horizon.utils.memoized import memoized  # noqa
from keystoneclient.auth.identity import v2
from keystoneclient.auth.identity import v3
from keystoneclient import session as ksc_session
from openstack_dashboard import api


@memoized
def cueclient(request):
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    auth_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    auth_version = getattr(settings,
                           'OPENSTACK_API_VERSIONS', {}).get('identity', 2.0)
    if auth_version == 3:
        auth = v3.Token(auth_url, request.user.token.id,
                        project_id=request.user.project_id,
                        project_name=request.user.project_name)
    elif auth_version == 2 or 2.0:
        auth = v2.Token(auth_url, request.user.token.id,
                        tenant_id=request.user.tenant_id,
                        tenant_name=request.user.tenant_name)

    session = ksc_session.Session(auth=auth, verify=cacert)
    return client.Client(session=session)


def clusters_list(request, marker=None):
    clusters = cueclient(request).clusters.list()
    return clusters


def cluster_get(request, cluster_id):
    cluster = cueclient(request).clusters.get(cluster_id)
    return cluster


def cluster_create(request, name, nic, flavor, size):
    return cueclient(request).clusters.create(name, nic,
                                              flavor, size, 0)


def delete_cluster(request, cluster_id):
    return cueclient(request).clusters.delete(cluster_id)


def flavor(request, flavor_id):
    return api.nova.flavor_get(request, flavor_id)
