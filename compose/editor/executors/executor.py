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

import opentracing

from compose.editor.executors.sql_alchemy import SqlAlchemyConnector


class Executor:
    def __init__(self, username, interpreter):
        # self.interface = interface

        # connector py / Hue connector instance
        # session / _get_engine() ...
        self.connector = SqlAlchemyConnector(
            username, interpreter
        )  # Compo vs Inheritance

    def execute(self):
        return self.connector.execute()


# def fetch_status(self, session_id, job_id):


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
    interpreter = Executor(user.username, interpreter=interpreter)

    with opentracing.tracer.start_span("interpreter") as span:
        # interpreter.execute needs the sessions, but we don't want to persist them
        # pre_execute_sessions = notebook['sessions']
        # notebook['sessions'] = sessions
        response["handle"] = interpreter.execute(notebook, snippet)
        # notebook['sessions'] = pre_execute_sessions

    response["status"] = 0

    return response
