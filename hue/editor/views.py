
from django.shortcuts import render
from editor.api import execute
from rest_framework.decorators import api_view


@api_view(["POST"])
def query(request, dialect=None):
    data = execute(request)
    return data
