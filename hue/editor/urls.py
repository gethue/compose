from django.urls import path, re_path

from . import api

urlpatterns = [
    re_path(r"^query/(?P<dialect>.+)/?$", api.query, name="execute"),
    # url(r'^api/autocomplete/?$', notebook_api.autocomplete, name='api_autocomplete_databases'),
    # url(r'^api/autocomplete/(?P<database>[^/?]*)/?$', notebook_api.autocomplete, name='api_autocomplete_tables'),
    # url(r'^api/autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/?$', notebook_api.autocomplete, name='api_autocomplete_columns'),
    # url(r'^api/autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/(?P<column>\w+)/?$', notebook_api.autocomplete, name='api_autocomplete_column'),
    # url(r'^api/autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/(?P<column>\w+)/(?P<nested>.+)/?$', notebook_api.autocomplete, name='api_autocomplete_nested'),
]
