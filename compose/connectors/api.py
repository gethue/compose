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

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def get_types(request):
    return Response({"connectors": [], "categories": []})


@api_view(["POST"])
def get_instances(request):
    return Response({"connectors": []})


@api_view(["POST"])
def get_config(request):
    return Response(
        {
            "app_config": {
                "editor": {
                    "name": "editor",
                    "displayName": "Editor",
                    "buttonName": "Query",
                    "interpreters": [
                        {
                            "name": "MySQL",
                            "type": "1",
                            "id": "1",
                            "displayName": "MySQL",
                            "buttonName": "Query",
                            "tooltip": "MySQL Query",
                            "optimizer": "api",
                            "page": "/editor/?type=1",
                            "is_sql": True,
                            "is_batchable": True,
                            "dialect": "mysql",
                            "dialect_properties": {
                                "is_sql": True,
                                "sql_identifier_quote": "`",
                                "sql_identifier_comment_single": "--",
                                "has_catalog": True,
                                "has_database": True,
                                "has_table": True,
                                "has_live_queries": False,
                                "has_optimizer_risks": True,
                                "has_optimizer_values": True,
                                "has_auto_limit": False,
                                "has_reference_language": False,
                                "has_reference_functions": False,
                                "has_use_statement": False,
                                "trim_statement_semicolon": False,
                            },
                        }
                    ],
                    "default_limit": 5000,
                    "interpreter_names": ["1"],
                    "page": "/editor/?type=1",
                    "default_sql_interpreter": "1",
                },
                "catalogs": [],
                "browser": {},
                "home": {
                    "name": "home",
                    "displayName": "Home",
                    "buttonName": "Saved Queries",
                    "interpreters": [],
                    "page": "/home",
                },
            },
            "main_button_action": {},
            "button_actions": [],
            "default_sql_interpreter": "1",
            "cluster_type": "direct",
            "has_computes": False,
            "hue_config": {"enable_sharing": True, "is_admin": True},
            "clusters": [
                {
                    "id": "default",
                    "name": "demo.gethue.com",
                    "type": "direct",
                    "credentials": {},
                }
            ],
            "documents": {"types": ["query-mysql", "directory"]},
            "status": 0,
        }
    )
