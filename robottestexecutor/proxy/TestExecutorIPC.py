#  Copyright 2021 Direkt Embedded Pty Ltd
#  Copyright (c) 2020 Sipke Vriend
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


class IPCTest:
    def __init__(self, test, result=None, message=None):
        self.name = test
        self.result = result
        self.message = message
    name = None
    result = None
    message = None


class IPCMessage:
    def __init__(self, title, message=None):
        self.title = title
        self.message = message
    title = None
    message = None


class IPCSuite:
    def __init__(self, test, result=None, statistics=None):
        self.name = test
        self.result = result
        self.statistics = statistics
    name = None
    result = None
    statistics = None


class TestExecutorIPC:
    def __init__(self, op, data=None):
        self.op = op
        self.data = data
    op = None
    data = None


class IPCTypes:
    def __init__(self):
        pass
    FEEDBACK = "feedback"
    PAUSE_EXECUTION = "pause_execution"
    START_SUITE = "start_suite"
    END_SUITE = "end_suite"
    START_TEST = "start_test"
    END_TEST = "end_test"
    END_EXECUTION = "end_execution"
    LOG_MESSAGE = "log_message"
    EXECUTE_MANUAL_STEP = "execute_manual_step"
    GET_VALUE_FROM_USER = "get_value_from_user"


class IPCUserInteraction:
    def __init__(self, message, default, hidden, *values):
        self.default = default
        self.values = values
        self.message = message
        self.hidden = hidden
    values = None
    message = None
    default = None
    hidden = False


class IPCCommand:
    def __init__(self, op, data=None):
        if not data:
            data = {}
        self.op = op
        self.data = data
    op = None
    data = {}


class IPCCommands:
    def __init__(self):
        pass
    EXECUTE_SUITE = "execute_suite"
    TERMINATE = "terminate"


class TestExecutionInfo:
    def __init__(self):
        pass
    SOURCE = "Source"
    SUITES = "Suites"
    TAGS = "Tags"
    TESTS = "Tests"
    VARIABLES = "Variables"

