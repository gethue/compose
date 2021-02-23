"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
    path("v1/editor/", include("editor.urls")),
]

urlpatterns += [path("v1/connectors/", include("connectors.urls"))]

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
