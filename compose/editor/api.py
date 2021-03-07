#!/usr/bin/env python
# -- coding: utf-8 --
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging

import opentracing
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import api_view

from .sql_alchemy import SqlAlchemyApi

LOG = logging.getLogger(__name__)


@extend_schema(
    description="Minimal API for submitting an SQL statement synchronously",
    request=OpenApiTypes.STR,
    responses=OpenApiTypes.STR,
    examples=[
        OpenApiExample(name="SELECT 1, 2, 3", value='{"statement":"SELECT 1, 2, 3"}')
    ],
)
@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    print(request.POST)

    statement = request.data.get("statement") or "SELECT 1, 2, 3"

    data = _execute(user=request.user, dialect=dialect, statement=statement)

    return JsonResponse(data)


@extend_schema(
    description="Submitting an SQL statement asynchronously",
    request=OpenApiTypes.STR,
    responses=OpenApiTypes.STR,
)
@api_view(["POST"])
def execute(request, dialect=None):
    json.loads(request.POST.get("notebook", "{}"))
    json.loads(request.POST.get("snippet", "{}"))

    statement = request.data.get("statement") or "SELECT 1, 2, 3"

    response = _execute(request.user, dialect, statement)

    return JsonResponse(response)


@api_view(["POST"])
def autocomplete(
    request, server=None, database=None, table=None, column=None, nested=None
):
    print(request.data)
    print(request.POST)
    data = execute(request)
    return data


def _execute(user, dialect, statement):
    notebook = {}
    snippet = {}

    # Added
    notebook["sessions"] = []
    snippet["statement"] = statement

    if dialect:
        notebook["dialect"] = dialect

    with opentracing.tracer.start_span("notebook-execute") as span:
        span.set_tag("user-id", user.username)

        response = _execute_notebook(user, notebook, snippet)

        span.set_tag("query-id", response.get("handle", {}).get("guid"))

        return response


def _execute_notebook(user, notebook, snippet):
    response = {"status": -1}

    interpreter = {
        "options": {"url": "sqlite:///db-demo.sqlite3"},
        "name": "sqlite",
        "dialect_properties": {},
    }
    interpreter = SqlAlchemyApi(user, interpreter=interpreter)
    # interpreter = get_api(request, snippet)

    with opentracing.tracer.start_span("interpreter") as span:
        # interpreter.execute needs the sessions, but we don't want to persist them
        # pre_execute_sessions = notebook['sessions']
        # notebook['sessions'] = sessions
        response["handle"] = interpreter.execute(notebook, snippet)
        # notebook['sessions'] = pre_execute_sessions

    response["status"] = 0

    return response
