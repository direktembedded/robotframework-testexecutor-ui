"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from robot.libraries.BuiltIn import BuiltIn
from testexecutor.control.TestSuiteListener import TestSuiteListener
from .TestExecutorIPC import TestExecutorIPC, IPCTest, IPCMessage, IPCTypes


class TestExecutorIPCListener():
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
        if TestExecutorIPC.__name__ not in msg.message:
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

