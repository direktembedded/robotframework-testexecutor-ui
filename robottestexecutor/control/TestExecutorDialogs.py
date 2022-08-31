#  Copyright 2021 Direkt Embedded Pty Ltd
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

    def feedback(self, message):
        te = BuiltIn().get_variable_value("${testexecutor}")
        ctest = BuiltIn().get_variable_value("${TEST NAME}")
        te.feedback(ctest, message)

