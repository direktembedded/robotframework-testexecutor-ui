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

from robot.output.loggerhelper import LEVELS
from robottestexecutor.proxy.TestExecutorIPC import TestExecutorIPC, IPCMessage, IPCTypes


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
        whitelist = []
        avoid = (LEVELS[msg.level] < LEVELS['WARN'])
        if avoid:
            if execution_ended in msg.message:
                self.connection.send(TestExecutorIPC(IPCTypes.END_EXECUTION))
                avoid = True
            for item in whitelist:
                if item in msg.message:
                    avoid = False
                    break
        if not avoid:
            self.connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(msg.level, msg.message)))
