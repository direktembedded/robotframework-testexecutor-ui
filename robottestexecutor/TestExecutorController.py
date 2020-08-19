"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

import threading
import os
from multiprocessing import Process, Pipe
from PySide2.QtCore import Qt
from robot import run
from robot.libraries.BuiltIn import BuiltIn
from robot.output import LOGGER
from robot.testdoc import TestSuiteFactory
from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.model.KeyValueModel import KeyValueModel, KeyValue
from testexecutor.model.ResultModel import ResultModel
from testexecutor.model.TreeSelectorModel import TreeSelectorModel
from testexecutor.model.TestSuiteControlModel import TestSuiteControlModel
from .RobotProcessController import RobotProcessController
from .TestExecutorListener import TestExecutorListener
from .TestExecutorIPCListener import TestExecutorIPCListener
from .TestExecutorIPC import TestExecutorIPC, IPCTypes, IPCCommand, IPCCommands, TestExecutionInfo
from .proxy.TestExecutorLogger import TestExecutorLogger


TAGS = "Tags"
SUITES = "Suites"
default_filters = {SUITES: [], TAGS: []}


def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)


class TestExecutorController(TestSuiteModel, TestExecutorListener):

    INSTANCE = 0

    def __init__(self, title="Robot Listener", ids=None, testpath=None, useselector=False):
        if ids:
            # TODO make this an import of json?
            self._id_data = ids
        else:
            # If no identification is given at least populate with one, devicekey.
            self._id_data = KeyValueModel()
            self._id_data.add(self.DEVICEKEY, KeyValue('Device', ''))
        self._results = ResultModel()
        self._runner = None
        self.running = False
        TestExecutorController.INSTANCE = TestExecutorController.INSTANCE + 1
        self._instance = TestExecutorController.INSTANCE
        TestSuiteModel.__init__(self, self._id_data, self._results, self._input_filter,
                                setstate_callback=self._state_control_callback, title=title)
        self.suitestate = TestSuiteModel.STATE_IDLE
        TestExecutorListener.__init__(self, model=self)
        self.selected_tags = []
        self.selected_suitenames = []
        self.testpath = testpath
        if useselector:
            self.controller = TestSuiteControlModel(filtercallback=self._selectionFilterChanged, filters=default_filters)
            self.controller.testselector = TreeSelectorModel()
            tags = []
            suitenames = []
            if self.testpath:
                tags, suitenames = self._set_controller_data(self.controller)
            self.controller.filters.updateData(TAGS, tags)
            self.controller.filters.updateData(SUITES, suitenames)

    def start(self):
        if not self._runner:
            import datetime
            #self._runner = threading.Thread(target=self._thread_run, args=(self.exampletest,))
            self._runner = threading.Thread(target=self._process_run, args=())
            self._runner.start()
        else:
            self.parent_conn.send(IPCCommand(IPCCommands.EXECUTE_SUITE, self._get_execution_info()))
        

    def _thread_run(self, testsuite):
        # TODO possibly temporary entry/start method.
        #print("threadrun", self._instance)
        run(testsuite, listener=self,
            variable=["CUSTOMDIALOGS:robottestexecutor.TestExecutorDialogs"],
            output="{0}-output.xml".format(self._instance),
            report="{0}-report.html".format(self._instance),
            log="{0}-log.html".format(self._instance)
            )

    def _process_run(self):
        import datetime
        self.parent_conn, child_conn = Pipe()
        p = RobotProcessController(child_conn)
        p.start()

        parent_conn = self.parent_conn
        self.running = True
        active_test = None
        self.parent_conn.send(IPCCommand(IPCCommands.EXECUTE_SUITE, self._get_execution_info()))
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
                    if rc.data.message:
                        self.feedback(rc.data.name, rc.data.message)
                elif rc.op == IPCTypes.END_EXECUTION:
                    self.clear_results_on_start = True
                    if self.controller:
                        self._allow_start()
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

    def _selectionFilterChanged(self, name, selected):
        if name == TAGS:
            self.selected_tags = selected.getItems()
        elif name == SUITES:
            self.selected_suitenames = selected.getItems()
        self._set_controller_data(self.controller, self.selected_tags, self.selected_suitenames)

    def _input_filter(self, input):
        #TODO this does not consider user filter yet
        if input:
            self._id_data.setValue('devicekey', input)
            self.suitestate = TestSuiteModel.STATE_READY
            self._allow_start()

    def _allow_start(self):
        self.asyncInstructions(self._id_data.getValue(self.DEVICEKEY), "Press start to start test", callback=self._start_suite, control=["Start"])
        self.suitestate = TestSuiteModel.STATE_RESTART

    def _start_suite(self, response=None):
        self.clear_results_on_start = False  # We may have multiple suites in a single run, so keep test results
        self.results.clear()
        self.start()

    def _stop_suite(self):
        #TODO tell robot run to stop
        # we are not stopping process  -- self.running = False
        self.clear_results_on_start = False  # We may have multiple suites in a single run, so keep test results
        pass

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

    def _set_controller_data(self, controller, include_tags=[], suitenames=[]):
        """

        :param controller:
        :param includes: Array of case insensitive tags to include. use AND OR etc like usbANDport as necessary.
        :return:
        """
        suites = controller.testselector
        tests = self.testpath
        variables = ["dummyvar:true"]

        suitestructure = parse(tests,
                               variable=variables,
                               include=include_tags,
                               suite=suitenames
                               )
        suites.clear()
        tags = []
        suitenames = []
        # TODO subdirectories need to have their suites extracted
        if len(suitestructure.tests) > 0:
            print(suitestructure.name)
            for test in suitestructure.tests:
                data = [test.name, test.doc]
                suites.appendChild(data)
                print(test.name)
        else:
            for suite in suitestructure.suites:
                print(suite.name)
                suitenames.append(suite.name)
                data = [suite.name, suite.doc]
                newparent = suites.appendChild(data)
                for test in suite.tests:
                    print(test.name)
                    data = [test.name, test.doc]
                    newparent.appendChild(data)
                    for tag in test.tags:
                        if tag not in tags:
                            tags.append(tag)
        print(TAGS, tags)
        return tags, suitenames

    def _get_execution_info(self):
        tests = []
        controller = self.controller
        selection = self.controller.testselector.selection
        rows = selection.selectedIndexes()
        # If any tests are selected then list them and only these will be executed. If none were selected then all
        # will be executed based on suites and tags selected. That is how robot framework executes tests.
        for index in rows:
            row = selection.model().itemData(index)
            print(index.row(), row)
            if len(row[0].childItems) == 0:
                test = row[0]
                tests.append(test.itemData[0])
        info = {}
        info[TestExecutionInfo.VARIABLES] = self._get_variables()
        info[TestExecutionInfo.TESTS] = tests
        info[TestExecutionInfo.SUITES] = self.selected_suitenames
        info[TestExecutionInfo.SOURCE] = self.testpath
        info[TestExecutionInfo.TAGS] = self.selected_tags
        return info

    def _get_variables(self):
        variables = []
        ids = self._id_data.getValues()
        if ids:
            for item in ids.items():
                variables.append("{0}:{1}".format(item[0], item[1]))
        return variables

    DEVICEKEY = 'devicekey'