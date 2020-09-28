"""

Copyright (c) 2020 Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

import threading
from multiprocessing import Pipe
from robot import run
from robot.errors import DataError
from robot.testdoc import TestSuiteFactory
from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.model.KeyValueModel import KeyValueModel, KeyValue
from testexecutor.model.ResultModel import ResultModel
from testexecutor.model.TreeSelectorModel import TreeSelectorModel
from testexecutor.model.TestSuiteControlModel import TestSuiteControlModel
from ..proxy.RobotProcessController import RobotProcessController
from .TestExecutorListener import TestExecutorListener
from ..proxy.TestExecutorIPC import IPCTypes, IPCCommand, IPCCommands, TestExecutionInfo
from ..config.IdentificationConfig import IdentifierListSchema
from ..config.IdentificationConfig import default_id_config


TAGS = "Tags"
SUITES = "Suites"
default_filters = {SUITES: [], TAGS: []}


def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)


class TestExecutorController(TestSuiteModel, TestExecutorListener):

    INSTANCE = 0

    def __init__(self, title="Robot Listener", id_config=None, db_config_file=None, useselector=False):
        if not id_config:
            id_config = default_id_config

        self._db_config_file = db_config_file
        self._id_data = KeyValueModel()
        self.id_config = None
        self._populate_id_data(id_config)

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
            self._process_run()
        else:
            self.parent_conn.send(IPCCommand(IPCCommands.EXECUTE_SUITE, self._get_execution_info()))

    def close(self):
        self.running = False

    def _process_run(self):
        try:
            self.parent_conn, child_conn = Pipe()
            p = RobotProcessController(child_conn, self._db_config_file)
            p.start()
            self._runner = threading.Thread(target=self._parent_run, args=(p,))
            self._runner.start()
        except FileNotFoundError as fe:
            self.userInstructions(fe.strerror, fe.filename, expectResponse=False)
        except Exception as ex:
            from sys import exc_info
            self.userInstructions("SYSTEM ERROR", str(exc_info()), expectResponse=False)

    def _parent_run(self, child_process):
        parent_conn = self.parent_conn
        self.running = True
        active_test = None
        self.parent_conn.send(IPCCommand(IPCCommands.EXECUTE_SUITE, self._get_execution_info()))
        while child_process.is_alive() and self.running:
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
                        self._allow_start(self.input_filter.instructions)
                elif rc.op == IPCTypes.LOG_MESSAGE:
                    self.userInstructions(rc.data.title, rc.data.message, expectResponse=False)
                    #print("\nTEC log_message", rc.data.title, rc.data.message, "END\n")
                #print(rc)

        if self._terminateProcess(child_process):
            if active_test:
                self.testCompleted(active_test, False)
            self.suitestate = TestSuiteModel.STATE_STOPPED
        self._runner = None

    def _terminateProcess(self, p):
        wasalive = p.is_alive()
        if wasalive:
            p.terminate()
            p.join()
        return wasalive

    def _selectionFilterChanged(self, name, selected):
        if name == TAGS:
            self.selected_tags = selected.getItems()
        elif name == SUITES:
            self.selected_suitenames = selected.getItems()
        self._set_controller_data(self.controller, self.selected_tags, self.selected_suitenames)

    def _input_filter(self, input):
        inputs = input.split('\n')
        for input in inputs:
            key, ready = self.input_filter.filter(input, self._id_data)
            if key:
                self._id_data.setValue(key, input)
            if ready:
                self.suitestate = TestSuiteModel.STATE_READY
                self._allow_start(self.input_filter.instructions)

    def _allow_start(self, instructions="Press start to start test"):
        self.asyncInstructions(self._id_data.getValue(self.DEVICEKEY), instructions, callback=self._start_suite, control=["Start"])
        self.suitestate = TestSuiteModel.STATE_RESTART

    def _start_suite(self, response=None):
        self.clear_results_on_start = False  # We may have multiple suites in a single run, so keep test results
        self.results.clear()
        self.start()

    def _stop_suite(self):
        self.running = False
        self.clear_results_on_start = False  # We may have multiple suites in a single run, so keep test results

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

    def _set_controller_data(self, controller, include_tags=[], suitenamesin=[]):
        """

        :param controller:
        :param includes: Array of case insensitive tags to include. use AND OR etc like usbANDport as necessary.
        :return:
        """
        suites = controller.testselector
        tests = self.testpath
        variables = ["dummyvar:true"]

        suites.clear()
        tags = []
        suitenames = []

        dataError = None
        try:
            suitestructure = parse(tests,
                                   variable=variables,
                                   include=include_tags,
                                   suite=suitenamesin
                                   )
            # TODO subdirectories need to have their suites extracted
            if len(suitestructure.tests) > 0:
                for test in suitestructure.tests:
                    data = [test.name, test.doc]
                    suites.appendChild(data)
            else:
                for suite in suitestructure.suites:
                    suitenames.append(suite.name)
                    data = [suite.name, suite.doc]
                    newparent = suites.appendChild(data)
                    for test in suite.tests:
                        data = [test.name, test.doc]
                        newparent.appendChild(data)
                        for tag in test.tags:
                            if tag not in tags:
                                tags.append(tag)
            if len(tags) > 0:
                tags.insert(0, '')
            if len(suitenames) > 0:
                suitenames.insert(0, '')
        except DataError as err:
            dataError = err

        if dataError:
            raise dataError

        return tags, suitenames

    def _get_execution_info(self):
        if self.controller:
            return self._get_execution_info_from_controller()
        else:
            info = {}
            info[TestExecutionInfo.VARIABLES] = self._get_variables()
            # TODO verify file/directory exists, here or in Process controller.
            info[TestExecutionInfo.SOURCE] = self._get_test_path()
            return info

    def _get_execution_info_from_controller(self):

        tests = []
        controller = self.controller
        selection = self.controller.testselector.selection
        rows = selection.selectedIndexes()
        # If any tests are selected then list them and only these will be executed. If none were selected then all
        # will be executed based on suites and tags selected. That is how robot framework executes tests.
        for index in rows:
            row = selection.model().itemData(index)
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

    def _get_test_path(self):
        test_suite = self.input_filter.get_suite(self.id_config.suites, self._id_data)
        return test_suite

    def _populate_id_data(self, id_config):
        self.id_config = IdentifierListSchema().loads(id_config)
        import importlib
        module = importlib.import_module(self.id_config.module)
        filter_class = getattr(module, self.id_config.implementation)
        self.input_filter = filter_class(self.id_config, self._id_data)

    DEVICEKEY = 'devicekey'