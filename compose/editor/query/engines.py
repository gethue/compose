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


from compose.editor.query.sqlalchemy_api import SqlAlchemyInterface

ENGINES = {}
CONNECTIONS = {}

"""
just make it work, kiss, refacto clean decoupled starting from API
then task
User --> Sessions --> Queries (Saved vs History)
Connector

Can use either module directly
- model
- api: Django REST
- executor: engine (0 Django)
- interface: sqlalchemy_client (native session_id, job_id)

Decoupled REST API, Py API [Editor API, native client API]
SqlAlchemy based only (leverage dialects API --> sqlachemy, flink... (until getting a sqlalchemy client? or not worth it, easier to do dialect) except hue-proxy...)
Session reuse / Cache py or persistence
Goal is to support connectors, return uuid, offer reuse of session or not. Flink INSERT job, CREATE MODEL --> Hue id
Easy support via Task, scheduled Task

asyncio / stream
more than 1 hue, task server? Handle routids?
Multi concurrent queries
Result Explorer
Auto schedule...
"""

# 2 levels max: Executor / Interface

# Caches
# - handles
# - sessions

# Editor specific executor
class Executor:
    """
    Compose specific: highest/simplest possible, "Fake" Editor API, combo Connectors/Sessions under hood
    Pure exec in Client (sqlalchemy)
    Hue UUID wrapper around native handle, manage caches, dialects
    """

    def __init__(self, username, dialect="hive"):  # dialect or connector id?
        self.username = username
        self.dialect = dialect

        # connector py / Hue connector instance
        # session
        #   py: process, _get_engine() ... Session table? Or pure frontend/py var? (--> decoupled py/rest...)
        #   argument: e.g. Editor page, still valid with SqlAlchemy, Task Server?
        # QueryHistory / connection
        interpreter = {
            "options": {"url": "sqlite:///db-demo.sqlite3"},
            "name": "sqlite",
            "dialect_properties": {},
        }
        # Currently we only have sqlalchemy as interface
        self.connector = SqlAlchemyInterface(username, interpreter)  # Api + Client

    # For under the cover operations like install examples
    def query(self, statement):
        pass

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
            "dialect": self.dialect,
        }
        response["handle"] = self.connector.execute(query)
        # notebook['sessions'] = pre_execute_sessions

        response["status"] = 0

        return response

    def check_status(self, query_id):
        data = self.connector.check_status(query_id)

        return {"status": data["status"]}

    def autocomplete(self):
        pass


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
