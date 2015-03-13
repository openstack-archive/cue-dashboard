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

from django.conf.urls import patterns
from django.conf.urls import url
from cuedashboard.queues import views


CLUSTERS = r'^(?P<cluster_id>[^/]+)/%s$'

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(),
                           name='index'),
                       url(CLUSTERS % '', views.DetailView.as_view(),
                           name='detail'),
                       url(r'^create$', views.CreateClusterView.as_view(),
                           name='create'),
                       )
