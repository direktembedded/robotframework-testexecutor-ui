"""

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from multiprocessing import Process, Pipe
from robot import run
from .TestExecutorIPCListener import TestExecutorIPCListener
from .proxy.TestExecutorLogger import TestExecutorLogger
from .TestExecutorIPC import IPCCommands, IPCCommand, TestExecutionInfo

class RobotProcessController(Process):

    def __init__(self, connection):
        self.listener = TestExecutorIPCListener(connection)
        self.logger = TestExecutorLogger(connection)
        self.running = False
        Process.__init__(self, target=self.process, args=(connection,))

    def process(self, connection):
        self.running = True
        while self.running:
            if connection.poll(1):
                rc = connection.recv()
                if rc.op == IPCCommands.EXECUTE_SUITE:
                    source = rc.data[TestExecutionInfo.SOURCE]
                    suites = rc.data[TestExecutionInfo.SUITES]
                    tests = rc.data[TestExecutionInfo.TESTS]
                    includes = rc.data[TestExecutionInfo.TAGS]
                    variables =rc.data[TestExecutionInfo.VARIABLES]
                    print(rc.op, rc.data)
                    self._process(source, suites, tests, includes, variables)
                    print("out of run")

    def _process(self, source, suites, tests, includes, variables):
        variables.append("CUSTOMDIALOGS:robottestexecutor.TestExecutorIPCDialogs")
        from robot.output import LOGGER
        LOGGER.register_logger(self.logger)
        run(source, listener=self.listener,
            suite=suites,
            test=tests,
            variable=variables,
            include=includes,
            prerunmodifier=["robottestexecutor.TestExecutorSuitePreRunModifier"],  # TODO probably not using this
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

