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

from robot.libraries.BuiltIn import BuiltIn
from testexecutor.control.TestSuiteListener import TestSuiteListener


class TestExecutorListener(TestSuiteListener):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, model):
        self.ROBOT_LIBRARY_LISTENER = self
        TestSuiteListener.__init__(self, model=model)

    def start_suite(self, name, result):
        print("\nTestExecutorListener.start_suite", name, result.starttime)
        # This provides a link between TestExecutorDialogs and TextExecutorListener!
        BuiltIn().set_suite_variable("${testexecutor}", self)
        self.suite_start(name.name)

    def start_test(self, name, result):
        print("\nTestExecutorListener.start_test", name, result.status, result.passed)
        self.test_started(name.name)

    def end_test(self, name, result):
        print("\nTestExecutorListener.end_test", name, result.status, result.passed)
        self.test_completed(name.name, result.passed)

    def end_suite(self, name, result):
        print("\nTestExecutorListener.end_suite", name, result.endtime)
        self.suite_end(name.name)

    def log_message(self, msg, level=None):
        print("log_message", msg)
        #self.feedback(name, msg)

    def close(self):
        print("\nDialogsListener.close()")

