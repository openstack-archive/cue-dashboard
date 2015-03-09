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

from django.conf import settings
from cueclient.v1 import client
from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v2
from collections import namedtuple
from openstack_dashboard.api import base
from horizon.utils.memoized import memoized  # noqa


@memoized
def cueclient(request):
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    auth_url = base.url_for(request, 'identity')
    auth = v2.Token(auth_url, request.user.token.id,
                    tenant_id=request.user.tenant_id,
                    tenant_name=request.user.tenant_name)
    session = ksc_session.Session(auth=auth, verify=cacert)
    return client.Client(session=session)


def clusters_list(request, marker=None):
    clusters = []
    clusters_dict = cueclient(request).clusters.list()
    for cluster_dict in clusters_dict:
        clusters.append(_to_cluster_object(cluster_dict))
    return clusters


def cluster_get(request, cluster_id):
    cluster_dict = cueclient(request).clusters.get(cluster_id)
    cluster = _to_cluster_object(cluster_dict['cluster'])
    return cluster


def cluster_create(request, name, nic, flavor, size, volume_size):
    return cueclient(request).clusters.create(name, nic,flavor,
                                              size, volume_size)


def delete_cluster(request, cluster_id):
    return cueclient(request).clusters.delete(cluster_id)


#todo
#This is needed because the cue client returns a dict
#instead of a cluster object.
def _to_cluster_object(cluster_dict):
    return namedtuple('Cluster', cluster_dict)(**cluster_dict)