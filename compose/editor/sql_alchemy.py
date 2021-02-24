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
import re
import uuid
from string import Template

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

ENGINES = {}
CONNECTIONS = {}
ENGINE_KEY = "%(username)s-%(connector_name)s"
URL_PATTERN = "(?P<driver_name>.+?://)(?P<host>[^:/ ]+):(?P<port>[0-9]*).*"

LOG = logging.getLogger(__name__)


class SessionExpired(Exception):
    pass


class QueryExpired(Exception):
    def __init__(self, message=None):
        super(QueryExpired, self).__init__()
        self.message = message


class AuthenticationRequired(Exception):
    def __init__(self, message=None):
        super(AuthenticationRequired, self).__init__()
        self.message = message

    def __str__(self):
        return "AuthenticationRequired: %s" % self.message


class OperationTimeout(Exception):
    def __str__(self):
        return "OperationTimeout"


class OperationNotSupported(Exception):
    pass


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


class SqlAlchemyApi:
    def __init__(self, user, interpreter):
        # super(SqlAlchemyApi, self).__init__(user=user, interpreter=interpreter)
        self.user = user
        self.interpreter = interpreter

        self.options = interpreter["options"]

        if interpreter.get("dialect_properties"):
            self.backticks = interpreter["dialect_properties"]["sql_identifier_quote"]
        else:
            self.backticks = (
                '"'
                if re.match(
                    "^(postgresql://|awsathena|elasticsearch|phoenix)",
                    self.options.get("url", ""),
                )
                else "`"
            )

    def _get_engine_key(self):
        return ENGINE_KEY % {
            "username": self.user.username,
            "connector_name": self.interpreter["name"],
        }

    def _get_engine(self):
        engine_key = self._get_engine_key()

        if engine_key not in ENGINES:
            ENGINES[engine_key] = self._create_engine()

        return ENGINES[engine_key]

    def _create_engine(self):
        if "${" in self.options["url"]:  # URL parameters substitution
            vars = {"USER": self.user.username}

            if "${PASSWORD}" in self.options["url"]:
                auth_provided = False
                if "session" in self.options:
                    for _prop in self.options["session"]["properties"]:
                        if _prop["name"] == "user":
                            vars["USER"] = _prop["value"]
                            auth_provided = True
                        if _prop["name"] == "password":
                            vars["PASSWORD"] = _prop["value"]
                            auth_provided = True

                if not auth_provided:
                    raise AuthenticationRequired(
                        message="Missing username and/or password"
                    )

            raw_url = Template(self.options["url"])
            url = raw_url.safe_substitute(**vars)
        else:
            url = self.options["url"]

        if url.startswith("awsathena+rest://"):
            url = url.replace(url[17:37], urllib_quote_plus(url[17:37]))
            url = url.replace(url[38:50], urllib_quote_plus(url[38:50]))
            s3_staging_dir = url.rsplit("s3_staging_dir=", 1)[1]
            url = url.replace(s3_staging_dir, urllib_quote_plus(s3_staging_dir))

        if self.options.get("has_impersonation"):
            m = re.search(URL_PATTERN, url)
            driver_name = m.group("driver_name")

            if not driver_name:
                raise QueryError(
                    "Driver name of %(url)s could not be found and impersonation is turned on"
                    % {"url": url}
                )

            url = url.replace(
                driver_name,
                "%(driver_name)s%(username)s@"
                % {"driver_name": driver_name, "username": self.user.username},
            )

        if self.options.get("credentials_json"):
            self.options["credentials_info"] = json.loads(
                self.options.pop("credentials_json")
            )

        # Enables various SqlAlchemy args to be passed along for both Hive & Presto connectors
        # Refer to SqlAlchemy pyhive for more details
        if self.options.get("connect_args"):
            self.options["connect_args"] = json.loads(self.options.pop("connect_args"))

        options = self.options.copy()
        options.pop("session", None)
        options.pop("url", None)
        options.pop("has_ssh", None)
        options.pop("has_impersonation", None)
        options.pop("ssh_server_host", None)

        options["pool_pre_ping"] = True

        return create_engine(url, **options)

    def _get_session(self, notebook, snippet):
        for session in notebook["sessions"]:
            if session["type"] == snippet["type"]:
                return session

        return None

    def _create_connection(self, engine):
        connection = None
        try:
            connection = engine.connect()
        except Exception as e:
            engine_key = self._get_engine_key()
            ENGINES.pop(engine_key, None)

            raise AuthenticationRequired(
                message="Could not establish connection to datasource: %s" % e
            )

        return connection

    # @query_error_handler
    def execute(self, notebook, snippet):
        guid = uuid.uuid4().hex
        is_async = False

        session = self._get_session(notebook, snippet)
        if session is not None:
            self.options["session"] = session

        engine = self._get_engine()
        connection = self._create_connection(engine)
        statement = snippet["statement"]

        if self.interpreter["dialect_properties"].get("trim_statement_semicolon", True):
            statement = statement.strip().rstrip(";")

        if self.interpreter["dialect_properties"].get(
            "has_use_statement"
        ) and snippet.get("database"):
            connection.execute(
                "USE %(sql_identifier_quote)s%(database)s%(sql_identifier_quote)s"
                % {
                    "sql_identifier_quote": self.interpreter["dialect_properties"][
                        "sql_identifier_quote"
                    ],
                    "database": snippet["database"],
                }
            )

        result = connection.execute(statement)

        cache = {
            "connection": connection,
            "result": result,
            "meta": [
                {
                    "name": col[0]
                    if (type(col) is tuple or type(col) is dict)
                    else col.name
                    if hasattr(col, "name")
                    else col,
                    "type": "STRING_TYPE",
                    "comment": "",
                }
                for col in result.cursor.description
            ]
            if result.cursor
            else [],
        }
        CONNECTIONS[guid] = cache

        return {
            "sync": False,
            "has_result_set": result.cursor != None,
            "modified_row_count": 0,
            "guid": guid,
            "result": {
                "has_more": result.cursor != None,
                "data": []
                if is_async
                else [[col for col in row] for row in result.fetchmany(10)],
                "meta": cache["meta"],
                "type": "table",
            },
        }
