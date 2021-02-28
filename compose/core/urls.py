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

from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    path("v1/iam/get/auth-token/", obtain_jwt_token),
    path("v1/iam/verify/auth-token/", verify_jwt_token),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")), # Good to delete if live docs auth works
    path("v1/iam/auth/", include("rest_framework.urls", namespace="rest_framework")),
]


# namespace for version?
# https://www.django-rest-framework.org/api-guide/versioning/#urlpathversioning

urlpatterns += [
    path("v1/editor/", include("compose.editor.urls")),
]

urlpatterns += [path("v1/connectors/", include("compose.connectors.urls"))]

urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
