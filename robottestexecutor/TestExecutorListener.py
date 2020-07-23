"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from robot.libraries.BuiltIn import BuiltIn
from testexecutor.control.TestSuiteListener import TestSuiteListener


class TestExecutorListener(TestSuiteListener):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, model):
        self.ROBOT_LIBRARY_LISTENER = self
        TestSuiteListener.__init__(self, model=model)
        print("\nTestExecutorListener.__init__")

    def start_suite(self, name, result):
        print("\nTestExecutorListener.start_suite", name, result.starttime)
        # This provides a link between TestExecutorDialogs and TextExecutorListener!
        BuiltIn().set_suite_variable("${testexecutor}", self)
        self.suiteStart(name.name)

    def start_test(self, name, result):
        print("\nTestExecutorListener.start_test", name, result.status, result.passed)
        self.testStarted(name.name)

    def end_test(self, name, result):
        print("\nTestExecutorListener.end_test", name, result.status, result.passed)
        self.testCompleted(name.name, result.passed)

    def end_suite(self, name, result):
        print("\nTestExecutorListener.end_suite", name, result.endtime)
        self.suiteEnd(name.name) # TODO set failures?

    def log_message(self, msg, level=None):
        print("log_message", msg)
        #self.feedback(name, msg)

    def close(self):
        print("\nDialogsListener.close()")

