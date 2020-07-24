"""

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
from multiprocessing import Process, Pipe
from robot import run
from .TestExecutorIPCListener import TestExecutorIPCListener
from .proxy.TestExecutorLogger import TestExecutorLogger
from .TestExecutorIPC import IPCCommands, IPCCommand

class RobotProcessController(Process):

    def __init__(self, connection, testsuite=None):
        self.listener = TestExecutorIPCListener(connection)
        self.logger = TestExecutorLogger(connection)
        self.running = False
        self.testsuite = testsuite #TODO this should come in via command
        Process.__init__(self, target=self.process, args=(connection,))

    def process(self, connection):
        self.running = True
        while self.running:
            if connection.poll(1):
                rc = connection.recv()
                if rc.op == IPCCommands.EXECUTE_SUITE:
                    variables = self._get_variables(rc.data)
                    print(rc.op, rc.data)
                    self._process(variables)
                    print("out of run")

    def _process(self, variables):
        variables.append("CUSTOMDIALOGS:robottestexecutor.TestExecutorIPCDialogs")
        from robot.output import LOGGER
        LOGGER.register_logger(self.logger)
        run(self.testsuite, listener=self.listener,
            variable=variables,
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

