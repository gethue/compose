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

from unittest.mock import patch

import pytest

from compose.editor.query.engines import Executor


@pytest.mark.django_db
def test_execute():

    with patch("compose.editor.query.engines.SqlAlchemyInterface.execute") as execute:
        execute.return_value = {"guid": "abc"}

        data = Executor(username="test").execute(statement="SELECT 1, 2, 3")

        assert data["handle"].get("guid") == "abc"


@pytest.mark.django_db
def test_check_status():

    with patch(
        "compose.editor.query.engines.SqlAlchemyInterface.check_status"
    ) as check_status:
        check_status.return_value = {"status": "running"}

        data = Executor(username="test").check_status(query_id="abc")

        assert data["status"] == "running"


@pytest.mark.django_db
def test_execute_query_flow():
    """
    Test flow with Compose handle (non DB native handle).
    Compose Editor API (non native DB api)
    """

    with patch("compose.editor.query.engines.SqlAlchemyInterface.execute") as execute:
        execute.return_value = {"guid": "abc"}

        data = Executor(username="test").execute(statement="SELECT 1, 2, 3")

        assert data["handle"].get("guid") == "abc"

    with patch(
        "compose.editor.query.engines.SqlAlchemyInterface.check_status"
    ) as check_status:
        check_status.return_value = {"status": "running"}

        data = Executor(username="test").check_status(query_id="abc")

        assert data["status"] == "running"

    # get_logs

    with patch(
        "compose.editor.query.engines.SqlAlchemyInterface.check_status"
    ) as check_status:
        check_status.return_value = {"status": "ready"}

        data = Executor(username="test").check_status(query_id="abc")

        assert data["status"] == "ready"

    # fetch_result

    # fetch_result next

    # re-fetch result from 0 (download)

    # close query
