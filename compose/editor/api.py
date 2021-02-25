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
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view

from .sql_alchemy import SqlAlchemyApi

LOG = logging.getLogger(__name__)


@extend_schema(
    # Json https://github.com/tfranzel/drf-spectacular/issues/279
    # Should define properly json POST attributes
    parameters=[
        OpenApiParameter(
            name="snippet",
            type={
                "type": "json",
                "minItems": 4,
                "maxItems": 6,
                "items": {"type": "number"},
            },
            location=OpenApiParameter.QUERY,
            required=False,
            style="form",
            explode=False,
        )
    ],
    responses=OpenApiTypes.OBJECT,
)
@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    print(request.POST)
    data = execute(request)
    return data


@api_view(["POST"])
def autocomplete(
    request, server=None, database=None, table=None, column=None, nested=None
):
    print(request.data)
    print(request.POST)
    data = execute(request)
    return data


def _execute_notebook(request, notebook, snippet):
    response = {"status": -1}

    interpreter = {
        "options": {"url": "sqlite:///../db.sqlite3"},
        "name": "sqlite",
        "dialect_properties": {},
    }
    interpreter = SqlAlchemyApi(request.user, interpreter=interpreter)
    # interpreter = get_api(request, snippet)

    with opentracing.tracer.start_span("interpreter") as span:
        # interpreter.execute needs the sessions, but we don't want to persist them
        # pre_execute_sessions = notebook['sessions']
        # notebook['sessions'] = sessions
        response["handle"] = interpreter.execute(notebook, snippet)
        # notebook['sessions'] = pre_execute_sessions

    response["status"] = 0

    return response


def execute(request, dialect=None):
    notebook = json.loads(request.POST.get("notebook", "{}"))
    snippet = json.loads(request.POST.get("snippet", "{}"))

    # Added
    notebook["sessions"] = []
    if not snippet.get("statement"):
        snippet["statement"] = "SELECT 1, 2, 3"

    if dialect:
        notebook["dialect"] = dialect

    with opentracing.tracer.start_span("notebook-execute") as span:
        span.set_tag("user-id", request.user.username)

        response = _execute_notebook(request, notebook, snippet)

        span.set_tag("query-id", response.get("handle", {}).get("guid"))

    return JsonResponse(response)
