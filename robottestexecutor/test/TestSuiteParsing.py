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
A Test file for verifying the parsing of robot tests from a directory or file using the robot.testdoc.TestSuiteFactory
"""
import os
from robot.testdoc import TestSuiteFactory

def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, 'suites')

    tests = "LargeTestCountSuite.robot"
    tests = test_path
    variables = ["dummyvar:true"]
    includes = ["usb", "Port"]  # Case insensitive. use AND OR etc like usbANDport as necessary.
    suitestructure = parse(tests,
                           variable=variables,
                           include=includes
                           )
    tags = []
    for suite in suitestructure.suites:
        print(suite.name)
        for test in suite.tests:
            print(test.name)
            for tag in test.tags:
                if tag not in tags:
                    tags.append(tag)
    if len(suitestructure.tests) > 0:
        print(suitestructure.name)
        for test in suitestructure.tests:
            print(test.name)
    print("Tags", tags)
