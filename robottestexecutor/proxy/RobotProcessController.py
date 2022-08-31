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

from multiprocessing import Process
from robot import run
from robottestexecutor.proxy.TestExecutorListener import TestExecutorListener
from robottestexecutor.proxy.TestExecutorLogger import TestExecutorLogger
from robottestexecutor.proxy.TestExecutorIPC import IPCCommands, TestExecutionInfo, IPCMessage, IPCTypes, \
    TestExecutorIPC, IPCCommand
from test_archiver.ArchiverRobotListener import ArchiverRobotListener


class RobotProcessController(Process):

    def __init__(self, connection, db_config_file):
        self.listener = TestExecutorListener(connection)
        self.logger = TestExecutorLogger(connection)
        self.db_listener = None
        self._db_config_file = db_config_file
        self.running = False
        Process.__init__(self, target=self.process, args=(connection,))

    def process(self, connection):
        self.running = True
        while self.running:
            if connection.poll(1):
                rc = connection.recv()
                if isinstance(rc, IPCCommand) and rc.op == IPCCommands.EXECUTE_SUITE:
                    source = []
                    suites = []
                    tests = []
                    includes = []
                    variables = []
                    start = False
                    if TestExecutionInfo.SOURCE in rc.data:
                        source = rc.data[TestExecutionInfo.SOURCE]
                        start = self._try_find_source(connection, source)
                    if TestExecutionInfo.SUITES in rc.data:
                        suites = rc.data[TestExecutionInfo.SUITES]
                    if TestExecutionInfo.TESTS in rc.data:
                        tests = rc.data[TestExecutionInfo.TESTS]
                    if TestExecutionInfo.TAGS in rc.data:
                        includes = rc.data[TestExecutionInfo.TAGS]
                    if TestExecutionInfo.VARIABLES in rc.data:
                        variables =rc.data[TestExecutionInfo.VARIABLES]
                    if start:
                        self._process(connection, source, suites, tests, includes, variables)

    def _process(self, connection, source, suites, tests, includes, variables):
        self._try_init_db(connection)
        metadata = variables.copy()
        variables.append("CUSTOMDIALOGS:robottestexecutor.proxy.TestExecutorDialogs")
        from robot.output import LOGGER
        LOGGER.register_logger(self.logger)
        listeners = [self.listener]
        if self.db_listener:
            listeners.append(self.db_listener)
        run(source, listener=listeners,
            suite=suites,
            test=tests,
            variable=variables,
            include=includes,
            console="none",
            loglevel="INFO",
            metadata=metadata,
            xoutputtimeinfo=True,
            formattimestamp="iso8601utc",
            # TODO do we want to allow dated output files with some ID formatting?
            output="NONE",
            report="NONE",
            log="NONE"
            )
        LOGGER.unregister_logger(self.logger)

    def _try_find_source(self, connection, source):
        import os
        success = False
        error = None
        if not source:
            error = "Test Suite is not defined"
        elif not os.path.isfile(source) and not os.path.isdir(source):
            error = f"Test Suite is not a file {source}"
        else:
            success = True
        if not success:
            connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage("Execution Error", error)))
        return success

    def _try_init_db(self, connection):
        success = False
        try:
            if self._db_config_file:
                self.db_listener = ArchiverRobotListener(self._db_config_file, adjust_with_system_timezone=True)
            success = True
        except FileNotFoundError as fe:
            connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage(fe.strerror, fe.filename)))
        except Exception as ex:
            from sys import exc_info
            # TODO, this is not caught at higher level, so although system error shows briefly it is "lost" and not noticed
            connection.send(TestExecutorIPC(IPCTypes.LOG_MESSAGE, IPCMessage("SYSTEM ERROR", str(exc_info()))))
        return success

    def _get_variables(self, dict):
        variables = []
        if dict:
            for item in dict.items():
                variables.append("{0}:{1}".format(item[0], item[1]))
        return variables


#output = "{0}-output.xml".format(instance),
#report = "{0}-report.html".format(instance),
#log = "{0}-log.html".format(instance)

