from django.shortcuts import render

from django.http import HttpResponse

from editor.api import execute


def query(request):

    data = execute(request)

    return data
