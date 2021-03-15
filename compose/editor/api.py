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

import logging

from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.decorators import api_view

from .query.engines import Executor

LOG = logging.getLogger(__name__)


@extend_schema(
    description="Minimal API for submitting an SQL statement synchronously",
    request={"application/json": OpenApiTypes.OBJECT},
    responses=OpenApiTypes.STR,
)
@api_view(["POST"])
def query(request, dialect=None):
    print(request.data)
    print(request.POST)

    statement = request.data.get("statement") or "SELECT 1, 2, 3"

    # connector = {}
    # query = Query(statement...)

    data = Executor(username=request.user).execute(statement=statement)
    # qhandle = Executor(dialect='dialect').execute(statement=statement)
    # qhandle = Executor(connector).execute(query)

    # data = Executor(connector).query(query)

    return JsonResponse(data)


@extend_schema(
    description="Submitting an SQL statement asynchronously",
    request=OpenApiTypes.STR,
    responses=OpenApiTypes.STR,
)
@api_view(["POST"])
def execute(request, dialect=None):
    request.data.get("statement") or "SELECT 1, 2, 3"

    response = {"uuid": "abc", "handle": {}}

    return JsonResponse(response)


@api_view(["POST"])
def autocomplete(
    request, server=None, database=None, table=None, column=None, nested=None
):
    print(request.data)
    print(request.POST)
    data = execute(request)
    return data


@api_view(["POST"])
def check_status(request):
    query_id = request.data.get("query_id")
    # operation_id = request.POST.get('operationId')

    data = Executor(username=request.user).check_status(query_id=query_id)

    return JsonResponse(data)


@api_view(["POST"])
def fetch_result_data(request):
    pass


@api_view(["POST"])
def get_logs(request):
    pass


# API specs
# Operation: https://swagger.io/specification/#operation-object
# Some possibilities, obviously going more manual if we don't have models. Can be case per case depending on API popularity.
# - Manual text docs like on current API docs
# - Reuse/Create a DRF serializer
# - Manual request to text and example object
# - Manual request body (and response)
@extend_schema(
    description="Minimal API for submitting an SQL statement synchronously",
    request={"application/json": OpenApiTypes.OBJECT},
    responses=OpenApiTypes.STR,
    examples=[
        OpenApiExample(
            name="SELECT 1, 2, 3",
            value={"statement": "SELECT 1, 2, 3"},
        )
    ],
    # Full override, all manual
    # https://github.com/tfranzel/drf-spectacular/issues/279
    # https://github.com/tfranzel/drf-spectacular/blob/6f12e8d9310ca2aaa833a1167d0d5f7795e2d635/tests/test_extend_schema.py#L160-L186
    # Note: seems to lose Parameters when set?
    operation={
        "operationId": "manual_endpoint",
        "tags": ["editor"],
        # https://swagger.io/specification/#request-body-object
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "examples": {
                        "1, 2, 3": {
                            "summary": "List of numbers",
                            "value": ["1", "2", "3"],
                        },
                    },
                    # "schema": {
                    #     "type": "object",
                    #     "properties": {"statement": {"type": "string"}},
                    #     "example": {"statement": "SELECT 1, 2, 3"}
                    # },
                }
            },
        },
    },
)
@api_view(["POST"])
def hello(request, message=None):
    print(request.data)
    print(request.POST)

    return JsonResponse({"data": request.data, "message": message})
