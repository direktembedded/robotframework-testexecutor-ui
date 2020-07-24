"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

import threading
from multiprocessing import Process, Pipe
from robot import run
from robot.libraries.BuiltIn import BuiltIn
from robot.output import LOGGER
from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.model.KeyValueModel import KeyValueModel, KeyValue
from testexecutor.model.ResultModel import ResultModel
from .TestExecutorListener import TestExecutorListener
from .TestExecutorIPCListener import TestExecutorIPCListener
from .TestExecutorIPC import TestExecutorIPC, IPCTypes
from .proxy.TestExecutorLogger import TestExecutorLogger



def _process(testsuite, connection, instance, variables):
    variables.append("CUSTOMDIALOGS:robottestexecutor.TestExecutorIPCDialogs")
    listener = TestExecutorIPCListener(connection)
    logger = TestExecutorLogger(connection)
    LOGGER.register_logger(logger)
    run(testsuite, listener=listener,
        variable=variables,
        prerunmodifier=["robottestexecutor.TestExecutorSuitePreRunModifier"],
        console="none",
        loglevel = "none",
        output="NONE",
        report="NONE",
        log="NONE"
        )


#output = "{0}-output.xml".format(instance),
#report = "{0}-report.html".format(instance),
#log = "{0}-log.html".format(instance)


class TestExecutorController(TestSuiteModel, TestExecutorListener):

    INSTANCE = 0

    def __init__(self, title="Robot Listener", ids=None, exampletest=None):
        if ids:
            # TODO make this an import of json?
            self._id_data = ids
        else:
            # If no identification is given at least populate with one, devicekey.
            self._id_data = KeyValueModel()
            self._id_data.add(self.DEVICEKEY, KeyValue('device', ''))
        self._results = ResultModel()
        self._runner = None
        self.running = False
        TestExecutorController.INSTANCE = TestExecutorController.INSTANCE + 1
        self._instance = TestExecutorController.INSTANCE
        self.exampletest = exampletest
        TestSuiteModel.__init__(self, self._id_data, self._results, self._input_filter,
                                setstate_callback=self._state_control_callback, title=title)
        self.suitestate = TestSuiteModel.STATE_IDLE
        TestExecutorListener.__init__(self, model=self)

    def start(self):
        if not self._runner:
            #self._runner = threading.Thread(target=self._thread_run, args=(self.exampletest,))
            self._runner = threading.Thread(target=self._process_run, args=(self.exampletest,))
            self._runner.start()

    def _thread_run(self, testsuite):
        # TODO possibly temporary entry/start method.
        #print("threadrun", self._instance)
        run(testsuite, listener=self,
            variable=["CUSTOMDIALOGS:robottestexecutor.TestExecutorDialogs"],
            output="{0}-output.xml".format(self._instance),
            report="{0}-report.html".format(self._instance),
            log="{0}-log.html".format(self._instance)
            )

    def _process_run(self, testsuite):
        # TODO: Overall exception capture for system errors at this point
        #print("_processrun", self._instance)
        parent_conn, child_conn = Pipe()
        p = Process(target=_process, args=(testsuite, child_conn, self._instance, self._get_variables()))
        p.start()

        object_list = None
        self.running = True
        active_test = None
        while p.is_alive() and self.running:
            if parent_conn.poll(1):
                rc = parent_conn.recv()
                if rc.op == IPCTypes.FEEDBACK:
                    self.feedback(rc.data.title, rc.data.message)
                elif rc.op == IPCTypes.PAUSE_EXECUTION:
                    response = self.userInstructions("", rc.data, expectResponse=True)
                    parent_conn.send(response)
                elif rc.op == IPCTypes.EXECUTE_MANUAL_STEP:
                    response = self.userDecision(rc.data.title, rc.data.message)
                    parent_conn.send(response)
                elif rc.op == IPCTypes.START_SUITE:
                    self.suiteStart(rc.data)
                elif rc.op == IPCTypes.END_SUITE:
                    self.suiteEnd(rc.data)
                elif rc.op == IPCTypes.START_TEST:
                    active_test = rc.data.name
                    self.testStarted(rc.data.name)
                elif rc.op == IPCTypes.END_TEST:
                    self.testCompleted(rc.data.name, rc.data.result)
                    active_test = None
                elif rc.op == IPCTypes.LOG_MESSAGE:
                    self.userInstructions(rc.data.title, rc.data.message, expectResponse=False)
                    #print("\nTEC log_message", rc.data.title, rc.data.message, "END\n")
                #print(rc)

        if p.is_alive():
            p.terminate()  # TODO use message sent to slave robot process to close gracefully if we can
            p.join()
            if active_test:
                self.testCompleted(active_test, False)
            self.suitestate = TestSuiteModel.STATE_STOPPED
        self._runner = None

    def _get_variables(self):
        variables = []
        ids = self._id_data.getValues()
        if ids:
            for item in ids.items():
                variables.append("{0}:{1}".format(item[0], item[1]))
        return variables

    def _input_filter(self, input):
        #TODO this does not consider user filter yet
        self._id_data.setValue('devicekey', input)
        self.suitestate = TestSuiteModel.STATE_READY
        self.asyncInstructions(self._id_data.getValue(self.DEVICEKEY), "Press start to start test", callback=self._start_suite, control=["Start"])

    def _start_suite(self, response=None):
        self.start()

    def _stop_suite(self):
        #TODO tell robot run to stop
        self.running = False

    def _clear_suite(self):
        self.clear()

    def _state_control_callback(self, st):
        newstate = None
        runningStates = [TestSuiteModel.STATE_RUNNING, TestSuiteModel.STATE_STARTING]
        if st == TestSuiteModel.STATE_STOPPING:
            if self.suitestate in runningStates:
                newstate = st
                self._stop_suite()
        else:
            newstate = st
        return newstate

    DEVICEKEY = 'devicekey'