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

"""
A test library providing dialogs for interacting with users.

``Dialogs`` is Robot Framework's standard library that provides means
for pausing the test execution and getting input from users.
This implementation ``TestExecutorDialogs`` is an interface library
which communicates with a running ``TestExecutor`` instance to display
messages and receive commands and data.
This implementation extends the Dialogs library to include a few extra
key words: feedback

Long lines in the provided messages are wrapped automatically. If you want
to wrap lines manually, you can add newlines using the ``\\n`` character
sequence.

The library has a known limitation that it cannot be used with timeouts
on Python. Support for IronPython was added in Robot Framework 2.9.2.

Unimplemented: 'get_value_from_user', 'get_selection_from_user', 'get_selections_from_user'

"""
from robot.libraries.BuiltIn import BuiltIn
from robot.version import get_version
from robottestexecutor.proxy.TestExecutorIPC import TestExecutorIPC, IPCMessage, IPCTypes, \
                                                    IPCUserInteraction
from robot.errors import ExecutionFailed

__version__ = get_version()
__all__ = ['TestExecutorDialogs']


class TestExecutorDialogs:

    def __init__(self):
        pass

    def pause_execution(self, message='Test execution paused. Press OK to continue.'):
        """Pauses test execution until user clicks ``Ok`` button.

        ``message`` is the message shown in the dialog.
        """
        connection = BuiltIn().get_variable_value("${connection}")
        connection.send(TestExecutorIPC(IPCTypes.PAUSE_EXECUTION, message))
        response = connection.recv()

    def execute_manual_step(self, message, default_error=None):
        """Pauses test execution until user sets the keyword status.

        User can press either ``PASS`` or ``FAIL`` button. In the latter case execution
        fails and an additional dialog is opened for defining the error message.

        ``message`` is the instruction shown in the initial dialog and
        ``default_error`` is the default value shown in the possible error message
        dialog.
        """
        connection, ctest = self._executor_info()
        connection.send(TestExecutorIPC(IPCTypes.EXECUTE_MANUAL_STEP, IPCMessage(ctest, message)))
        response = connection.recv()
        if not _validate_user_input(response):
            raise AssertionError("No response for step")
        else:
            if response != "yes":
                if not default_error:
                    default_error = "Manual step failed"
                raise AssertionError(default_error)

    def get_value_from_user(self, message, default_value='', hidden=False):
        """Pauses test execution and asks user to input a value.

        Value typed by the user, or the possible default value, is returned.
        Returning an empty value is fine, but pressing ``Cancel`` fails the keyword.

        ``message`` is the instruction shown in the dialog and ``default_value`` is
        the possible default value shown in the input field.

        If ``hidden`` is given a true value, the value typed by the user is hidden.
        ``hidden`` is considered true if it is a non-empty string not equal to
        ``false``, ``none`` or ``no``, case-insensitively. If it is not a string,
        its truth value is got directly using same
        [http://docs.python.org/library/stdtypes.html#truth|rules as in Python].

        Example:
        | ${username} = | Get Value From User | Input user name | default    |
        | ${password} = | Get Value From User | Input password  | hidden=yes |
        """
        connection, ctest = self._executor_info()
        msg = IPCMessage(ctest, message)
        command = IPCUserInteraction(msg, default_value, hidden)
        connection.send(TestExecutorIPC(IPCTypes.GET_VALUE_FROM_USER, command))
        # how to handle cancel
        response = connection.recv()
        if not _validate_user_input(response):
            if default_value:
                response = default_value
            else:
                raise AssertionError("No response for step and no default value provided")
        return response

    def user_choice(self, message):
        """Pauses test execution until user returns choice.

        User can press either ``Yes`` or ``No`` button, or provide text of control buttons

        ``message`` is the instruction shown in the initial dialog and
        ``control`` is an optional list of control buttons to show
        """
        connection, ctest = self._executor_info()
        connection.send(TestExecutorIPC(IPCTypes.EXECUTE_MANUAL_STEP, IPCMessage(ctest, message)))
        response = connection.recv()
        if not _validate_user_input(response):
            raise AssertionError("No response for step")
        return response

    def log_to_suite(self):
        BuiltIn().set_suite_variable("${logdestination}", "suite")

    def log_to_both(self):
        BuiltIn().set_suite_variable("${logdestination}", "both")

    def log_to_test(self):
        BuiltIn().set_suite_variable("${logdestination}", "test")

    def log_to_none(self):
        BuiltIn().set_suite_variable("${logdestination}", "none")

    def user_repeat_on_fail(self, keyword, *args):
        count = int(BuiltIn().get_variable_value("${user_repeat_on_fail_count}", default=100))
        fail_exit = BuiltIn().get_variable_value("${user_repeat_on_fail_exit}", default=True)
        exit_on_fail = DataHelper.convert_to_bool(fail_exit)
        keyword_err = None
        for step in range(count):
            try:
                BuiltIn().run_keyword(keyword, *args)
                keyword_err = None
                break
            except ExecutionFailed as err:
                keyword_err = err
                if not self._ask_user_to_repeat(err):
                    keyword_err.exit = exit_on_fail
                    raise keyword_err
        if keyword_err:
            raise keyword_err

    def _ask_user_to_repeat(self, err):
        connection = BuiltIn().get_variable_value("${connection}")
        title = "Repeat Step?"
        fail_msg = "{} {}".format(BuiltIn().get_variable_value("${TEST NAME}"), "Failed")
        message = '\n'.join([fail_msg, str(err)])
        connection.send(TestExecutorIPC(IPCTypes.EXECUTE_MANUAL_STEP, IPCMessage(title, message)))
        response = connection.recv()
        return not (response != "yes")

    def _executor_info(self):
        connection = BuiltIn().get_variable_value("${connection}")
        ctest = BuiltIn().get_variable_value("${TEST NAME}")
        return connection, ctest


class DataHelper:
    @staticmethod
    def convert_to_bool(value):
        if isinstance(value, bool):
            bool_ed = value
        elif isinstance(value, str):
            bool_ed = DataHelper.str_to_bool(value)
        else:
            bool_ed = bool(value)
        return bool_ed

    @staticmethod
    def str_to_bool(str):
        return str.lower() in ['true', '1', 't', 'y', 'yes']


def _validate_user_input(value):
    if value is None:
        raise RuntimeError('No value provided by user.')
    return value
