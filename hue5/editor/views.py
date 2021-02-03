from django.shortcuts import render

from django.http import HttpResponse

from editor.api import execute


# curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 10001"}'  | jq

def query(request):

    data = execute(request)

    return data
