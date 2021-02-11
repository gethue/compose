from django.http import JsonResponse
from django.shortcuts import render
from editor.api import execute
from rest_framework.decorators import api_view


@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    # data = execute(request)
    return JsonResponse({"aa": 11})
    return data
