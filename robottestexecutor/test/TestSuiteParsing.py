"""
A Test file for verifying the parsing of robot tests from a directory or file using the robot.testdoc.TestSuiteFactory

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
import os
from robot.testdoc import TestSuiteFactory

def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))

    tests = "LargeTestCountSuite.robot"
    tests = current_path
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
