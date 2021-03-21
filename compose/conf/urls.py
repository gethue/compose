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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    path("iam/v1/get/auth-token/", obtain_jwt_token),
    path("iam/v1/verify/auth-token/", verify_jwt_token),
    path("iam/v1/auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += [
    path("editor/v1/", include("compose.editor.urls", namespace="editor")),
    path("notebook/api/", include("compose.editor.urls_hue4", namespace="hue4")),
]

urlpatterns += [
    path("connectors/v1/", include("compose.connectors.urls", namespace="connectors"))
]

urlpatterns += [
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
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
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
