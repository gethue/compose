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

from editor.sql_alchemy import SqlAlchemyApi


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_answer_2():
    assert inc(4) == 5


def test_execute_statement():
    interpreter = {
        "options": {"url": "sqlite:///../db.sqlite3"},
        "name": "sqlite",
        "dialect_properties": {},
    }

    interpreter = SqlAlchemyApi(None, interpreter=interpreter)

    notebook = {}
    snippet = {}
    notebook["sessions"] = []
    snippet["statement"] = "SELECT 1, 2, 3"

    interpreter.execute(notebook, snippet)
