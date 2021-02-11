from django.shortcuts import render

from rest_framework.decorators import api_view

from editor.api import execute

from django.http import JsonResponse


@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    # data = execute(request)
    return JsonResponse({"aa": 11})
    return data
