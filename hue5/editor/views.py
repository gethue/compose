from django.shortcuts import render

from rest_framework.decorators import api_view

from editor.api import execute


# @api_view(['POST'])
def query(request, dialect=None):
  data = execute(request)

  return data
