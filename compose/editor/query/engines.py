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

"""
Can use either module directly:
- API: Django REST
- Editor model: (load, save, historify, execute...) doc2 model, connector models, user models
- Editor executor: engine (zero Django/models but dict inputs: interpreter, username). Editor API with execute and /autocomp
- SQL client: sqlalchemy_client (native session_id, job_id), Flink? --> make a dialect instead. SQL based only. Live queries?
"""

from compose.editor.query.sqlalchemy_api import SqlAlchemyInterface

SESSIONS = {}
HANDLES = {}


class Executor:
    """
    Compose specific: highest/simplest possible, Editor API, combo Connectors/Dialects/Sessions data under hood
    Pure exec is in Client (sqlalchemy)
    Hue UUID wrapper around native handle, manage caches, dialects
    Session reuse / Cache py or persistence
    Goal is to support connectors, return uuid, offer reuse of session or not. Flink INSERT job, CREATE MODEL --> Hue id (Multi concurrent queries)
    Easy support via Task, scheduled Task, importer create table "jobs", Result Explorer tasks ...
    """

    def __init__(self, username, interpreter):
        self.username = username
        self.interpreter = interpreter
        self.connector = SqlAlchemyInterface(
            username, interpreter
        )  # Only SqlAlchemy as interface --> client

    # For under the cover operations like install examples
    def query(self, statement):
        query = {
            "statement": statement,
            "database": None,
            "dialect": self.interpreter["dialect"],
        }
        return self.connector.query(query)

    # Query Object? simple statement?
    # execute --> query
    def execute(self, statement):
        # sessions id or None or auto?
        # hue uuid/id(if historify) + native handle
        # async if TS, check poll/stream too

        response = {"status": -1}

        # interpreter.execute needs the sessions, but we don't want to persist them
        # pre_execute_sessions = notebook['sessions']
        # notebook['sessions'] = sessions
        # session = self._get_session(notebook, snippet)
        query = {
            "statement": statement,
            "database": None,
            "dialect": self.interpreter["dialect"],
        }
        response["handle"] = self.connector.execute(query)
        # notebook['sessions'] = pre_execute_sessions

        response["status"] = 0

        return response

    def check_status(self, query_id):
        data = self.connector.check_status(query_id)

        return {"status": data["status"]}

    def fetch_result(self, query_id, rows=100, start_over=False):
        data = self.connector.fetch_result(query_id, rows=rows, start_over=start_over)

        return {"result": data}

    def autocomplete(self, database=None, table=None, column=None, nested=None):
        data = self.connector.autocomplete(
            database=database, table=table, column=column, nested=nested
        )

        return data


# class ExecutorTracer():

#     def pre_execute(self, *args, **kwargs):
#         with opentracing.tracer.start_span("notebook-execute") as span:
#             span.set_tag("user-id", self.username)

#     def post_execute(self):
#         span.set_tag("query-id", response.get("handle", {}).get("guid"))


# class Executor
#  query
#  execute / fetch_status / fetch_results / fetch_logs
#  autocomplete
#  explain (smart)
#  schedule
# class SessionExecutor
#      ... Tracer
# class HistorifyExecutor


def query_error_handler(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            message = str(e)
            if "1045" in message:  # 'Access denied' # MySQL
                raise AuthenticationRequired(message=message)
            else:
                raise e
        except AuthenticationRequired:
            raise
        except QueryExpired:
            raise
        except Exception as e:
            message = force_unicode(e)
            if (
                "Invalid query handle" in message
                or "Invalid OperationHandle" in message
            ):
                raise QueryExpired(e)
            else:
                LOG.exception("Query Error")
                raise QueryError(message)

    return decorator
