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

from django.utils.encoding import smart_text


class QueryError(Exception):
    def __init__(self, message, handle=None):
        super(QueryError, self).__init__(message)
        self.message = message or _("No error message, please check the logs.")
        self.handle = handle
        self.extra = {}

    def __unicode__(self):
        return smart_text(self.message)


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
