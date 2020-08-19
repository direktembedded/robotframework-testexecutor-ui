#
# Copyright (c) 2020 Sipke Vriend
# Licensed under BSD-3-Clause, refer LICENSE
#

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
from robottestexecutor.proxy.TestExecutorIPC import TestExecutorIPC, IPCMessage, IPCTypes

__version__ = get_version()
__all__ = ['execute_manual_step',
           'pause_execution']


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
        connection = BuiltIn().get_variable_value("${connection}")
        ctest = BuiltIn().get_variable_value("${TEST NAME}")
        connection.send(TestExecutorIPC(IPCTypes.EXECUTE_MANUAL_STEP, IPCMessage(ctest, message)))
        response = connection.recv()
        if not _validate_user_input(response):
            raise AssertionError("No response for step")
        else:
            if response != "yes":
                if not default_error:
                    default_error = "Manual step failed"
                raise AssertionError(default_error)

    def log_to_suite(self):
        BuiltIn().set_suite_variable("${logdestination}", "suite")

    def log_to_both(self):
        BuiltIn().set_suite_variable("${logdestination}", "both")

    def log_to_test(self):
        BuiltIn().set_suite_variable("${logdestination}", "test")


def _validate_user_input(value):
    if value is None:
        raise RuntimeError('No value provided by user.')
    return value
