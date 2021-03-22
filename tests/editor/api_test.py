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

import json
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestExecutor:
    def setup_method(self, method):
        self.c = Client()

        user = User.objects.create_user(username="test", password="test")
        assert self.c.login(username="test", password="test")

    def test_query(self):
        resp = self.c.post(reverse("editor:query", kwargs={"dialect": "mysql"}))
        data = json.loads(resp.content)

        assert data.get("handle")
        assert data["handle"].get("guid")

    def test_execute(self):
        resp = self.c.post(reverse("editor:execute", kwargs={"dialect": "mysql"}))
        data = json.loads(resp.content)

        assert data["uuid"] == "abc"

    def test_check_status(self):
        with patch("compose.editor.api.Executor.check_status") as check_status:
            check_status.return_value = {"status": "running"}

            resp = self.c.post(
                reverse("editor:check_status"),
            )
            data = json.loads(resp.content)

            assert data["status"] == "running"
