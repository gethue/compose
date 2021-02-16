from django.urls import path, re_path

from . import views

urlpatterns = [
    # Hue 5
    re_path(r"^query/(?P<dialect>.+)/?$", views.query, name="execute"),
]
