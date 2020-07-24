"""

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

from robot.libraries.BuiltIn import BuiltIn
from testexecutor.control.TestSuiteListener import TestSuiteListener
from ..TestExecutorIPC import TestExecutorIPC, IPCMessage, IPCTypes


class TestExecutorLogger:
    """
    A proxy robot framework logger which sends respective logged message to the TestExecutor Controller via an IPC
    message.
    
    Use by adding to robot framework's LOGGER instance.
        from robot.output import LOGGER
        from .proxy.TestExecutorLogger import TestExecutorLogger
        ...
        logger = TestExecutorLogger(connection)
        LOGGER.register_logger(logger)
    """
    def __init__(self, connection):
        self.connection = connection

    def start_suite(self, suite):
        #TODO Could send through the suite tests, so test results could be pre-populated
        pass

    def message(self, msg):
        self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(msg.level, msg.message)))

