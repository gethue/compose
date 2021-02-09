from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.query, name='query'),

    # url(r'^api/execute(?:/(?P<dialect>.+))?/?$', notebook_api.execute, name='execute'),
    re_path(r'^api/execute/(?P<dialect>.+)/?$', views.query, name='execute'),
]
