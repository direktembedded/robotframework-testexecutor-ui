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

    def end_suite(self, suite):
        failed = [err for err in suite.tests if not err.passed]
        if len(failed) > 0:
            summary = ["{0}: {1}".format(t.name, t.message) for t in failed]
            self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage("Failed", summary)))

    def message(self, msg):
        execution_ended = 'Tests execution ended'
        blacklist = [execution_ended, 'Created keyword', 'Imported library', 'Initializing namespace', 'In library'
                     'Found test library']
        print("message from log:", msg.level, msg)
        avoid = False
        for item in blacklist:
            if execution_ended in msg.message:
                self.connection.send(TestExecutorIPC(IPCTypes.END_EXECUTION))
                avoid = True
            elif item in msg.message:
                avoid = True
                break
        if not avoid:
            self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(msg.level, msg.message)))

