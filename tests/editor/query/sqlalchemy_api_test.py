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

from unittest.mock import Mock, patch

import pytest

from compose.editor.query.sqlalchemy_api import SqlAlchemyInterface


@pytest.mark.django_db
def test_query():
    interpreter = {
        "options": {"url": "sqlite://"},
        "name": "sqlite",
        "dialect_properties": {},
    }
    connector = SqlAlchemyInterface(username="test", interpreter=interpreter)
    query = {"statement": "SELECT 1, 2, 3"}

    data = connector.execute(query=query)

    assert data["result"]["data"] == [[1, 2, 3]]


@pytest.mark.django_db
def test_fetch_status():
    interpreter = {
        "options": {"url": "sqlite://"},
        "name": "sqlite",
        "dialect_properties": {},
    }
    connector = SqlAlchemyInterface(username="test", interpreter=interpreter)
    query_id = "abc"

    with patch("compose.editor.query.sqlalchemy_api.CONNECTIONS") as CONNECTIONS:
        CONNECTIONS.get.return_value = {"result": Mock(), "has_result_set": True}

        data = connector.check_status(query_id=query_id)

        assert data["status"] == "available"


@pytest.mark.django_db
def test_fetch_result():
    interpreter = {
        "options": {"url": "sqlite://"},
        "name": "sqlite",
        "dialect_properties": {},
    }
    connector = SqlAlchemyInterface(username="test", interpreter=interpreter)
    query_id = "abc"

    with patch("compose.editor.query.sqlalchemy_api.CONNECTIONS") as CONNECTIONS:
        CONNECTIONS.get.return_value = {
            "result": Mock(fetchmany=Mock(return_value=[[1], [2], [3]])),
            "meta": [{"type": "STRING_TYPE"}],
        }

        data = connector.fetch_result(query_id=query_id, rows=10, start_over=True)

        assert data["data"] == [[1], [2], [3]]


@pytest.mark.live
@pytest.mark.parametrize(
    ("dialect", "url"),
    [
        ("sqllite", "sqlite:///../db-demo.sqlite3"),
        ("mysql", "mysql://root:password@127.0.0.1:13306/mysql"),
    ],
)
def test_execute_statement(dialect, url):
    interpreter = {
        "options": {"url": url},
        "name": dialect,
        "dialect_properties": {},
    }

    interpreter = SqlAlchemyInterface(user="test", interpreter=interpreter)

    notebook = {}
    snippet = {}
    notebook["sessions"] = []
    snippet["statement"] = "SELECT 1, 2, 3"

    resultset = interpreter.execute(notebook, snippet)

    assert resultset["result"]["data"] == [[1, 2, 3]]
