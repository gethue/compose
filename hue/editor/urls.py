from django.urls import re_path

from . import api

urlpatterns = [
    re_path(r"^query/(?P<dialect>.+)/?$", api.query, name="execute"),
    re_path(r"^autocomplete/?$", api.autocomplete, name="autocomplete_databases"),
    re_path(
        r"^autocomplete/(?P<database>[^/?]*)/?$",
        api.autocomplete,
        name="autocomplete_tables",
    ),
    re_path(
        r"^autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/?$",
        api.autocomplete,
        name="autocomplete_columns",
    ),
    re_path(
        r"^autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/(?P<column>\w+)/?$",
        api.autocomplete,
        name="autocomplete_column",
    ),
    re_path(
        r"^autocomplete/(?P<database>[^/?]*)/(?P<table>[\w_\-]+)/(?P<column>\w+)/(?P<nested>.+)/?$",
        api.autocomplete,
        name="autocomplete_nested",
    ),
]
