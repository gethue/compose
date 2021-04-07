# -- coding: utf-8 --
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.urls import re_path

from . import api

app_name = "connector"


urlpatterns = [
    re_path(r"^api2/get_config/?$", api.get_config, name="get_config"),
    re_path(  # To not support anymore going forward, unused
        r"^api2/context/namespaces/(?P<id>\d+)/?$",
        api.get_namespaces,
        name="get_namespaces",
    ),
]
