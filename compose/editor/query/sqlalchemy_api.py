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

import datetime
import json
import logging
import re
import textwrap
import uuid
from string import Template

from sqlalchemy import MetaData, Table, create_engine, inspect
from sqlalchemy.exc import (
    CompileError,
    NoSuchTableError,
    OperationalError,
    UnsupportedCompilationError,
)

from compose.editor.query.exceptions import (
    AuthenticationRequired,
    QueryError,
    QueryExpired,
)

ENGINES = {}  # Sessions
CONNECTIONS = {}  # Query Handles
ENGINE_KEY = "%(username)s-%(connector_name)s"
URL_PATTERN = "(?P<driver_name>.+?://)(?P<host>[^:/ ]+):(?P<port>[0-9]*).*"

LOG = logging.getLogger(__name__)


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
            message = str(e)
            if (
                "Invalid query handle" in message
                or "Invalid OperationHandle" in message
            ):
                raise QueryExpired(e)
            else:
                LOG.exception("Query Error")
                raise QueryError(message)

    return decorator


# Api vs Client
# Handle the DB client. Also reuse qhandles, session caches?
class SqlAlchemyInterface:
    def __init__(self, username, interpreter):
        # super(SqlAlchemyApi, self).__init__(user=user, interpreter=interpreter)
        self.username = username
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

    def _get_engine_key(self):  # --> to Executor?
        return ENGINE_KEY % {
            "username": self.username,
            "connector_name": self.interpreter["name"],
        }

    def _get_engine(self):
        engine_key = self._get_engine_key()

        if engine_key not in ENGINES:
            ENGINES[engine_key] = self._create_engine()

        return ENGINES[engine_key]

    def _create_engine(self):
        if (
            "${" in self.options["url"]
        ):  # URL parameters substitution, should be in Engine as custom to Hue globally
            vars = {"USER": self.username}

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

        # --> to move to py Hooks in connector types
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
                % {"driver_name": driver_name, "username": self.username},
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

    def query(self, query):
        return self.execute(query, is_async=False)

    # @query_error_handler
    def execute(self, query, is_async=True):
        guid = uuid.uuid4().hex

        # session = self._get_session(notebook, snippet)
        # if session is not None:
        #     self.options["session"] = session

        engine = self._get_engine()
        connection = self._create_connection(engine)
        statement = query["statement"]

        if self.interpreter["dialect_properties"].get("trim_statement_semicolon", True):
            statement = statement.strip().rstrip(";")

        if self.interpreter["dialect_properties"].get(
            "has_use_statement"
        ) and query.get("database"):
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
        print(result)

        # cache == sa_query_handle
        cache = {
            "connection": connection,  # Session
            "result": result,  # Handle
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
            "has_result_set": result.cursor != None,
        }
        CONNECTIONS[guid] = cache

        return {
            "sync": not is_async,
            "has_result_set": cache["has_result_set"],
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

    def check_status(self, query_id):
        handle = CONNECTIONS.get(query_id)

        response = {"status": "canceled"}

        if handle:
            cursor = handle["result"].cursor
            if self.options["url"].startswith("presto://") and cursor and cursor.poll():
                response["status"] = "running"
            elif handle["has_result_set"]:
                response["status"] = "available"
            else:
                response["status"] = "success"
        else:
            raise QueryExpired()

        return response

    def fetch_result(self, query_id, rows=100, start_over=False):
        handle = CONNECTIONS.get(query_id)

        if handle:
            data = handle["result"].fetchmany(rows)
            meta = handle["meta"]
            self._assign_types(data, meta)
        else:
            raise QueryExpired()

        return {
            "has_more": data and len(data) >= rows or False,
            "data": data if data else [],
            "meta": meta if meta else [],
            "type": "table",
        }

    def autocomplete(
        self,
        database=None,
        table=None,
        column=None,
        nested=None,
        operation=None,
    ):
        if self.interpreter["dialect"] == "phoenix":
            if database:
                database = database.upper()
            if table:
                table = table.upper()
        engine = self._get_engine()
        inspector = inspect(engine)

        assist = Assist(inspector, engine, backticks=self.backticks)
        response = {"status": -1}

        if operation == "functions":
            response["functions"] = []
        elif operation == "function":
            response["function"] = {}
        elif database is None:
            response["databases"] = [db or "" for db in assist.get_databases()]
        elif table is None and operation == "models":
            response["models"] = [t for t in assist.get_models(database)]
        elif table is None:
            tables_meta = []
            for t in assist.get_table_names(database):
                t = self._fix_bigquery_db_prefixes(t)
                tables_meta.append({"name": t, "type": "Table", "comment": ""})
            for t in assist.get_view_names(database):
                t = self._fix_bigquery_db_prefixes(t)
                tables_meta.append({"name": t, "type": "View", "comment": ""})
            response["tables_meta"] = tables_meta
        elif column is None:
            columns = assist.get_columns(database, table)

            response["columns"] = [col["name"] for col in columns]
            response["extended_columns"] = [
                {
                    "autoincrement": col.get("autoincrement"),
                    "comment": col.get("comment"),
                    "default": col.get("default"),
                    "name": col.get("name"),
                    "nullable": col.get("nullable"),
                    "type": self._get_column_type_name(col),
                }
                for col in columns
            ]

            if (
                not self.options["url"].startswith("phoenix://")
                and operation != "model"
            ):
                response.update(assist.get_keys(database, table))
        else:
            columns = assist.get_columns(database, table)
            response["name"] = next(
                (col["name"] for col in columns if column == col["name"]), ""
            )
            response["type"] = next(
                (str(col["type"]) for col in columns if column == col["name"]), ""
            )

        response["status"] = 0
        return response

    def _assign_types(self, results, meta):
        result = results and results[0]
        if result:
            for index, col in enumerate(result):
                if isinstance(col, int):
                    meta[index]["type"] = "INT_TYPE"
                elif isinstance(col, float):
                    meta[index]["type"] = "FLOAT_TYPE"
                elif isinstance(col, bool):
                    meta[index]["type"] = "BOOLEAN_TYPE"
                elif isinstance(col, datetime.date):
                    meta[index]["type"] = "TIMESTAMP_TYPE"
                else:
                    meta[index]["type"] = "STRING_TYPE"

    def _get_column_type_name(self, col):
        try:
            name = str(col.get("type"))
        except (UnsupportedCompilationError, CompileError):
            name = col.get("type").__visit_name__.lower()

        return name

    def _fix_bigquery_db_prefixes(self, identifier):
        if type(identifier) == dict and identifier.get("type") == "model":
            identifier["type"] = "Model"

        if self.options["url"].startswith("bigquery://"):
            identifier["name"] = identifier["name"].rsplit(".", 1)[-1]

        return identifier


class Assist(object):
    def __init__(self, db, engine, backticks, api=None):
        self.db = db
        self.engine = engine
        self.backticks = backticks
        self.api = api

    def get_databases(self):
        return self.db.get_schema_names()

    def get_table_names(self, database, table_names=[]):
        return self.db.get_table_names(database)

    def get_view_names(self, database, view_names=[]):
        return self.db.get_view_names(database)

    def get_tables(self, database, table_names=[]):
        return self.get_table_names(database) + self.get_view_names(database)

    def get_models(self, database):
        return [
            t for t in self.db.get_table_names(database) if isinstance(t, dict)
        ]  # Currently only supported by pybigquery

    def get_columns(self, database, table):
        try:
            return self.db.get_columns(table, database)
        except NoSuchTableError:
            return []

    def get_sample_data(self, database, table, column=None, operation=None):
        if operation == "hello":
            statement = "SELECT 'Hello World!'"
        elif operation == "model":
            return [], []
        elif operation is not None and operation != "default":
            statement = (
                "SELECT * FROM (%s) LIMIT 1000" % operation
                if operation.strip().lower().startswith("select")
                else operation
            )
        else:
            column = (
                "%(backticks)s%(column)s%(backticks)s"
                % {"backticks": self.backticks, "column": column}
                if column
                else "*"
            )
            statement = textwrap.dedent(
                """\
        SELECT %(column)s
        FROM %(backticks)s%(database)s%(backticks)s.%(backticks)s%(table)s%(backticks)s
        LIMIT %(limit)s
        """
                % {
                    "database": database,
                    "table": table,
                    "column": column,
                    "limit": 100,
                    "backticks": self.backticks,
                }
            )

        connection = self.api._create_connection(self.engine)
        try:
            result = connection.execute(statement)
            return result.cursor.description, result.fetchall()
        finally:
            connection.close()

    def get_keys(self, database, table):
        meta = MetaData()
        metaTable = Table(
            table, meta, schema=database, autoload=True, autoload_with=self.engine
        )

        return {
            "foreign_keys": [
                {"name": fk.parent.name, "to": fk.target_fullname}
                for fk in metaTable.foreign_keys
            ],
            "primary_keys": [{"name": pk.name} for pk in metaTable.primary_key.columns],
        }
