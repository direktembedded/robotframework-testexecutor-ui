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

import threading
import os
import json
import copy
from multiprocessing import Pipe
from robot import run
from robot.errors import DataError
from robot.testdoc import TestSuiteFactory
from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.model.KeyValueModel import KeyValueModel, KeyValue
from testexecutor.model.ResultModel import ResultModel
from testexecutor.model.TestSuiteControlModel import TestSuiteControlModel
from ..proxy.RobotProcessController import RobotProcessController
from .TestExecutorListener import TestExecutorListener
from ..proxy.TestExecutorIPC import IPCTypes, IPCCommand, IPCCommands, TestExecutionInfo
from ..config.IdentificationConfig import IdentifierListSchema
from ..config.IdentificationConfig import default_id_config
from marshmallow.exceptions import ValidationError as MarshMallowValidationError
from PySide6.QtCore import Signal, Qt


TAGS = "Tags"
SUITES = "Suites"
default_filters = {SUITES: [], TAGS: []}


def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)


class TestExecutorController(TestExecutorListener, TestSuiteModel):

    INSTANCE = 0

    def __init__(self, title="Robot Listener", id_config=None, db_config_file=None, useselector=False, testpath=None,
                 instance_table_records=None, id_monitor=None, output_folder=None, unique_ids=None):
        if not id_config:
            id_config = default_id_config

        self.parent_conn = None
        self._exited = False
        self.id_monitor = None
        self._db_config_file = db_config_file
        self._output_folder = output_folder
        self._unique_ids = unique_ids
        if unique_ids is None:
            self._unique_ids = []
        self._id_data = KeyValueModel()
        self.id_config = None
        self._populate_id_data(id_config)
        self.testpath = testpath
        self.instance_table_records = None
        if instance_table_records:
            self.instance_table_records = instance_table_records

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
            tags = []
            suitenames = []
            if self.testpath:
                tags, suitenames = self._set_controller_data(self.controller)
            self.controller.filters.updateData(TAGS, tags)
            self.controller.filters.updateData(SUITES, suitenames)
        self.startProcessSignal.connect(self._process_run, Qt.QueuedConnection)
        self.postInputSignal.connect(self._post_input, Qt.QueuedConnection)
        self.postReadyToMonitor.connect(self._post_ready_to_monitor, Qt.QueuedConnection)
        self.postEndToMonitor.connect(self._post_end_to_monitor, Qt.QueuedConnection)
        self._awaiting_start = False
        if id_monitor:
            self.id_monitor = id_monitor
            self._start_monitor()

    def start(self):
        if self.id_monitor:
            # If we are starting a suite, then no longer monitor the ID input
            self.id_monitor.stop()
        if not self._runner:
            # Always start process from the main thread
            self.startProcessSignal.emit()
        else:
            self.parent_conn.send(IPCCommand(IPCCommands.EXECUTE_SUITE, self._get_execution_info()))

    def close(self):
        if self.parent_conn:
            self.parent_conn.send(IPCCommand(IPCCommands.TERMINATE))
        self._exited = True
        self.running = False
        if self.id_monitor:
            self.id_monitor.stop()

    def _process_run(self):
        try:
            self.parent_conn, child_conn = Pipe()
            p = RobotProcessController(child_conn, self._db_config_file, self._output_folder)
            p.start()
            self._runner = threading.Thread(target=self._parent_run, args=(p,))
            self._runner.start()
        except FileNotFoundError as fe:
            self.user_instructions(fe.strerror, fe.filename, expectResponse=False)
        except Exception as ex:
            from sys import exc_info
            # TODO: this should probably stop the system from continuing, currently does not
            self.user_instructions("SYSTEM ERROR", str(exc_info()), expectResponse=False)

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
                    response = self.user_instructions("", rc.data, expectResponse=True)
                    parent_conn.send(response)
                elif rc.op == IPCTypes.EXECUTE_MANUAL_STEP:
                    response = self.user_decision(rc.data.title, rc.data.message)
                    parent_conn.send(response)
                elif rc.op == IPCTypes.START_SUITE:
                    self.suite_start(rc.data)
                elif rc.op == IPCTypes.END_SUITE:
                    self.suite_end(rc.data.name, failures=rc.data.statistics.failed, message=rc.data.statistics.message)
                    self.postEndToMonitor.emit(rc.data.result)
                elif rc.op == IPCTypes.START_TEST:
                    active_test = rc.data.name
                    self.test_started(rc.data.name)
                elif rc.op == IPCTypes.END_TEST:
                    self.test_completed(rc.data.name, rc.data.result)
                    active_test = None
                    if rc.data.message:
                        self.feedback(rc.data.name, rc.data.message)
                elif rc.op == IPCTypes.END_EXECUTION:
                    self.clear_results_on_start = True
                    if self.controller:
                        self._allow_start(self.input_filter.instructions)
                elif rc.op == IPCTypes.LOG_MESSAGE:
                    self.user_instructions(rc.data.title, rc.data.message, expectResponse=False)
                elif rc.op == IPCTypes.GET_VALUE_FROM_USER:
                    message = rc.data.message
                    info = rc.data
                    input, response = self.user_input(message.title, message.message, None, info.default,
                                                      info.hidden, info.values)
                    parent_conn.send((input, response))

        if self._terminateProcess(child_process):
            if active_test:
                self.test_completed(active_test, False)
            self.suitestate = TestSuiteModel.STATE_STOPPED
        self._runner = None

    def _terminateProcess(self, p, count=1):
        is_alive = wasalive = p.is_alive()
        if wasalive:
            while is_alive and count > 0:
                p.terminate()
                is_alive = p.is_alive()
                count = count - 1
        return wasalive

    def _selectionFilterChanged(self, name, selected):
        if name == TAGS:
            self.selected_tags = selected.getItems()
        elif name == SUITES:
            self.selected_suitenames = selected.getItems()
        self._set_controller_data(self.controller, self.selected_tags, self.selected_suitenames)

    def _input_filter(self, input):
        return self._id_input_filter(input)

    def _post_input(self, input):
        """
        Set the model's newid value in case it has some processsing, this
        will in turn call _id_input_filter
        """
        self.newid = input

    def _post_ready_to_monitor(self):
        if self.id_monitor:
            self.id_monitor.ready()

    def _post_end_to_monitor(self, result):
        if self.id_monitor:
            self.id_monitor.end_suite(result)

    def _id_monitor_input(self, input):
        """
        Relay via queued signal to ensure synchronous communications with monitor
        """
        self.postInputSignal.emit(input)

    def _id_input_filter(self, input):
        ready = False
        try:
            inputs = input.split('\n')
            for input in inputs:
                if input.lower() == TestSuiteModel.ACTION_CLEAR.lower():
                    self.clear()
                    continue
                key, ready = self.input_filter.filter(input, self._id_data)
                if key:
                    self._id_data.setValue(key, input)
                if ready:
                    if self._awaiting_start and input.lower() == 'start':
                        # Id Monitor can start the suite by sending through 'start' as input once id data is ready
                        self._start_suite(input)
                    elif not self._awaiting_start:
                        self.suitestate = TestSuiteModel.STATE_READY
                        self._allow_start(self.input_filter.get_instructions(self._id_data, self.testpath))
        except FileNotFoundError as f_err:
            self.async_instructions("File Not Found", str(f_err), callback=self._error_accepted, control=["Ok"])
        except Exception as err:
            self.async_instructions("Error", str(err), callback=self._error_accepted, control=["Ok"])
        return ready

    def _error_accepted(self, response):
        self.clear_instructions()

    def _allow_start(self, instructions="Press start to start test"):
        self._awaiting_start = True
        self.async_instructions(self._id_data.getValue(self.DEVICEKEY), instructions, callback=self._start_suite, control=["Start"])
        self.suitestate = TestSuiteModel.STATE_RESTART

    def _start_suite(self, response=None):
        started = False
        if response == 'start':  # Matches button text, all lower case
            self._awaiting_start = False
            self.clear_instructions()
            self.clear_results_on_start = False  # We may have multiple suites in a single run, so keep test results
            self.results.clear()
            self.start()
            started = True
        return started

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
            completedStates = [TestSuiteModel.STATE_IDLE, TestSuiteModel.STATE_END, TestSuiteModel.STATE_STOPPED]
            if newstate != self.suitestate:
                if newstate in completedStates:
                    self._start_monitor()
                elif newstate == TestSuiteModel.STATE_READY:
                    if self.id_monitor:
                        self.postReadyToMonitor.emit()
        return newstate

    def _start_monitor(self):
        if self.id_monitor and not self._exited:
            self.id_monitor.start(input_callback=self._input_filter)

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
            if len(suitestructure.tests) > 0:
                parent_suite = "."  # Use current directory symbol to indicate base suite
                for test in suitestructure.tests:
                    suites.appendChild(test.name, test.doc, parent_suite)
            else:
                for suite in suitestructure.suites:
                    parent_suite = suite.name
                    suitenames.append(suite.name)
                    for test in suite.tests:
                        suites.appendChild(test.name, test.doc, parent_suite)
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
        table_records = {}
        if self.instance_table_records:
            table_records = copy.deepcopy(self.instance_table_records)
        variables, unique_ids = self._get_identifier_variables(table_records)
        if table_records:
            for table, fields in table_records.items():
                field_str = json.dumps(fields)
                variables.append(f'table#{table}:{field_str}')
        info = {}
        test_path = self._get_test_path(table_records)
        info[TestExecutionInfo.SOURCE] = test_path
        info[TestExecutionInfo.VARIABLES] = variables
        info[TestExecutionInfo.UNIQUE_IDS] = unique_ids
        if self.controller:
            self._get_execution_info_from_controller(info)
        return info

    def _get_execution_info_from_controller(self, info):
        """
        Add the controller variables and override the SOURCE
        """
        tests = []
        rows = self.controller.selectedItems()
        # If any tests are selected then list them and only these will be executed. If none were selected then all
        # will be executed based on suites and tags selected. That is how robot framework executes tests.
        for item in rows:
            tests.append(item.name)
        info[TestExecutionInfo.TESTS] = tests
        info[TestExecutionInfo.SUITES] = self.selected_suitenames
        info[TestExecutionInfo.SOURCE] = self.testpath
        info[TestExecutionInfo.TAGS] = self.selected_tags

    def _get_identifier_variables(self, table_records=None):
        variables = []
        unique_ids = []
        if not table_records:
            # If caller does not want table records, create an internal dictionary which will be lost
            table_records = {}
        ids = self._id_data.getValues()
        if ids:
            for item in ids.items():
                key = item[0]
                if key in self._unique_ids:
                    unique_ids.append(item[1])
                variables.append("{0}:{1}".format(item[0], item[1]))
                self.input_filter.get_identifier_table_fields(item[0], item[1], table_records)
        return variables, unique_ids

    def _get_test_path(self, table_records):
        test_suite = self.input_filter.get_suite(self.id_config.suites, self._id_data, table_records)
        if test_suite and test_suite.startswith(".") and self.testpath:
            test_suite = os.path.join(self.testpath, test_suite)
        return test_suite

    def _populate_id_data(self, id_config):
        try:
            if os.path.isfile(id_config):
                with open(id_config) as f:
                    id_config = f.read()
            self.id_config = IdentifierListSchema().loads(id_config)
            import importlib
            module = importlib.import_module(self.id_config.module)
            filter_class = getattr(module, self.id_config.implementation)
            self.input_filter = filter_class(self.id_config, self._id_data)
        except MarshMallowValidationError as ex:
            raise
        except Exception as ex:
            raise Exception("Failed to load identification data") from ex

    DEVICEKEY = 'devicekey'
    startProcessSignal = Signal()
    postInputSignal = Signal(str)
    postReadyToMonitor = Signal()
    postEndToMonitor = Signal(bool)
