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
from robottestexecutor.proxy.TestExecutorIPC import TestExecutorIPC, IPCTest, IPCMessage, IPCTypes


class TestExecutorListener():
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, connection):
        self.ROBOT_LIBRARY_LISTENER = self
        self.connection = connection
        #print("\nTestExecutorProxyListener.__init__")

    def start_suite(self, name, result):
        #print("\nTestExecutorProxyListener.start_suite", name.name, result.starttime)
        # This provides a link between TestExecutorDialogs and TextExecutorListener!
        BuiltIn().set_suite_variable("${connection}", self.connection)
        self.connection.send(TestExecutorIPC(IPCTypes.START_SUITE, name.name))

    def start_test(self, name, result):
        #print("\nTestExecutorIPCListener.start_test", name, result.status, result.passed)
        self.connection.send(TestExecutorIPC(IPCTypes.START_TEST, IPCTest(name.name, result.passed)))

    def end_test(self, name, result):
        #print("\nTestExecutorIPCListener.end_test", name.name, result.status, result.passed)
        self.connection.send(TestExecutorIPC(IPCTypes.END_TEST, IPCTest(name.name, result.passed, result.message)))

    def end_suite(self, name, result):
        #print("\nTestExecutorIPCListener.end_suite", name, result.endtime)
        self.connection.send(TestExecutorIPC(IPCTypes.END_SUITE, name.name))

    def log_message(self, msg):
        block = [TestExecutorIPC.__name__, 'logdestination']
        skip = False
        for item in block:
            if item in msg.message:
                skip = True
                break
        if not skip:
            ctest = BuiltIn().get_variable_value("${TEST NAME}")
            csuite = BuiltIn().get_variable_value("${SUITE NAME}")
            logdestination = BuiltIn().get_variable_value("${logdestination}")
            if ctest:
                if not logdestination or (logdestination == "test"):
                    self.connection.send(TestExecutorIPC(IPCTypes.FEEDBACK, IPCMessage(ctest, msg.message)))
                elif logdestination == "both":
                    self.connection.send(TestExecutorIPC(IPCTypes.FEEDBACK, IPCMessage(ctest, msg.message)))
                    self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(ctest, msg.message)))
                elif logdestination == "suite":
                    self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(ctest, msg.message)))
            elif csuite:
                self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(csuite, msg.message)))

    def close(self):
        # We do not want to close the connection as we want the process to stay alive
        # self.connection.close()
        pass

