"""

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from multiprocessing import Process, Pipe
from robot.output import LOGGER
from robot import run
from .TestExecutorIPCListener import TestExecutorIPCListener
from .proxy.TestExecutorLogger import TestExecutorLogger

class RobotProcessController(Process):

    def __init__(self, args=None):
        Process.__init__(self, target=self._process, args=args)

    def process(self):
        pass

    def _process(self, testsuite, connection, variables):
        variables.append("CUSTOMDIALOGS:robottestexecutor.TestExecutorIPCDialogs")
        listener = TestExecutorIPCListener(connection)
        logger = TestExecutorLogger(connection)
        LOGGER.register_logger(logger)
        run(testsuite, listener=listener,
            variable=variables,
            prerunmodifier=["robottestexecutor.TestExecutorSuitePreRunModifier"],
            console="none",
            loglevel="INFO",
            output="NONE",
            report="NONE",
            log="NONE"
            )


#output = "{0}-output.xml".format(instance),
#report = "{0}-report.html".format(instance),
#log = "{0}-log.html".format(instance)

