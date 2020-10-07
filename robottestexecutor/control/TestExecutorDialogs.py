"""
This is a library to use if robot is run in same Process as testexecutor. Otherwise, use the version in proxy package.
"""
from robot.libraries.BuiltIn import BuiltIn
from robot.version import get_version

__version__ = get_version()

class TestExecutorDialogs:

    def __init__(self):
        pass

    def pause_execution(self, message=None):
        """
        ``message`` is the message that will be given to the listener.
        """
        te = BuiltIn().get_variable_value("${testexecutor}")
        te.userInstructions("", message, expectResponse=True)
        print("exampletest", te.exampletest)

    def feedback(self, message):
        te = BuiltIn().get_variable_value("${testexecutor}")
        ctest = BuiltIn().get_variable_value("${TEST NAME}")
        te.feedback(ctest, message)
