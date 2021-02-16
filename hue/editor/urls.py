from django.urls import path, re_path

from . import views

urlpatterns = [
    # path("", views.query, name="query"),
    # url(r'^api/execute(?:/(?P<dialect>.+))?/?$', notebook_api.execute, name='execute'),
    # Hue 5
    re_path(r"^execute/(?P<dialect>.+)/?$", views.query, name="execute"),

    # Hue 4
    # Actually just don't port
    re_path(r"^api/execute/(?P<dialect>.+)/?$", views.query, name="hue4_execute"),
]
