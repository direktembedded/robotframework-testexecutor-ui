"""

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from multiprocessing import Process
from robot import run
from robottestexecutor.proxy.TestExecutorListener import TestExecutorListener
from robottestexecutor.proxy.TestExecutorLogger import TestExecutorLogger
from robottestexecutor.proxy.TestExecutorIPC import IPCCommands, TestExecutionInfo

class RobotProcessController(Process):

    def __init__(self, connection):
        self.listener = TestExecutorListener(connection)
        self.logger = TestExecutorLogger(connection)
        self.running = False
        Process.__init__(self, target=self.process, args=(connection,))

    def process(self, connection):
        self.running = True
        while self.running:
            if connection.poll(1):
                rc = connection.recv()
                if rc.op == IPCCommands.EXECUTE_SUITE:
                    source = []
                    suites = []
                    tests = []
                    includes = []
                    variables = []
                    if TestExecutionInfo.SOURCE in rc.data:
                        source = rc.data[TestExecutionInfo.SOURCE]
                    if TestExecutionInfo.SUITES in rc.data:
                        suites = rc.data[TestExecutionInfo.SUITES]
                    if TestExecutionInfo.TESTS in rc.data:
                        tests = rc.data[TestExecutionInfo.TESTS]
                    if TestExecutionInfo.TAGS in rc.data:
                        includes = rc.data[TestExecutionInfo.TAGS]
                    if TestExecutionInfo.VARIABLES in rc.data:
                        variables =rc.data[TestExecutionInfo.VARIABLES]
                    self._process(source, suites, tests, includes, variables)

    def _process(self, source, suites, tests, includes, variables):
        variables.append("CUSTOMDIALOGS:robottestexecutor.proxy.TestExecutorDialogs")
        from robot.output import LOGGER
        LOGGER.register_logger(self.logger)
        run(source, listener=self.listener,
            suite=suites,
            test=tests,
            variable=variables,
            include=includes,
            prerunmodifier=["robottestexecutor.control.TestExecutorSuitePreRunModifier"],  # TODO probably not using this
            console="none",
            loglevel="INFO",
            output="NONE",
            report="NONE",
            log="NONE"
            )
        LOGGER.unregister_logger(self.logger)

    def _get_variables(self, dict):
        variables = []
        if dict:
            for item in dict.items():
                variables.append("{0}:{1}".format(item[0], item[1]))
        return variables


#output = "{0}-output.xml".format(instance),
#report = "{0}-report.html".format(instance),
#log = "{0}-log.html".format(instance)

