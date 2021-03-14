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

import pytest

from compose.editor.sql_alchemy import SqlAlchemyApi


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


@pytest.mark.live
@pytest.mark.parametrize(
    ("dialect", "url"),
    [
        ("sqllite", "sqlite:///../db-demo.sqlite3"),
        ("mysql", "mysql://root:password@127.0.0.1:13306/mysql"),
    ],
)
def test_execute_statement(dialect, url):
    class User:
        def __init__(self):
            self.username = "test"

    interpreter = {
        "options": {"url": url},
        "name": dialect,
        "dialect_properties": {},
    }

    interpreter = SqlAlchemyApi(user=User(), interpreter=interpreter)

    notebook = {}
    snippet = {}
    notebook["sessions"] = []
    snippet["statement"] = "SELECT 1, 2, 3"

    resultset = interpreter.execute(notebook, snippet)

    assert resultset["result"]["data"] == [[1, 2, 3]]
