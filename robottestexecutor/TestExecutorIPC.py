"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""


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


class IPCCommand:
    def __init__(self, op, data={}):
        self.op = op
        self.data = data
    op = None
    data = {}


class IPCCommands:
    def __init__(self):
        pass
    EXECUTE_SUITE = "execute_suite"


class TestExecutionInfo:
    def __init__(self):
        pass
    SOURCE = "Source"
    SUITES = "Suites"
    TAGS = "Tags"
    TESTS = "Tests"
    VARIABLES = "Variables"

