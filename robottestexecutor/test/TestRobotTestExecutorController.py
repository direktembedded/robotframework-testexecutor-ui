"""
Test module to kick off text-executor gui with controller/test selector enabled, so different tests can be run.
execute as python3 <filename.py>

Copyright (c) 2020- Sipke Vriend, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""

from testexecutor.model.TestSuiteGroup import TestSuiteGroup
from testexecutor.model.MultiTestWindowModel import MultiTestWindowModel
from testexecutor.test.SampleTestSuiteWrapper import SampleTestSuiteWrapper
from testexecutor.model.FilterGroupModel import FilterGroupModel
from testexecutor.model.FilterModel import FilterModel
from testexecutor.model.TestSuiteControlModel import TestSuiteControlModel
from testexecutor.model.TreeSelectorModel import TreeSelectorModel

config = '''{
    "states": {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}}
    },

    "proportion": {
      "title": 0.1,
      "identification": 0.2,
      "instructions": 0.4,
      "status": 0.04
    },

    "results": {
      "viewableCount": 8,
      "color": "#e5e2e2",
      "item": {
        "proportion": {
            "name": 0.3,
            "time": 0.2
        },
        "color": "#605b5b",
        "border": {"color": "#00000000"},
        "name": {
            "color": "#00000000",
            "text": {"color": "#e5e2e2"}
        },
        "feedback": {
            "color": "#8e8a8a",
            "border": {"color": "#b9e5e2e2"},
            "text": {"color": {"default": "black", "progress": "#e5e2e2"}},
            "progress": {"color": "green"}
        },
        "time": {
            "color": "#00000000",
            "text": {"color": "#e5e2e2"}
        }
      }
    },

    "identification": {
      "proportion": {"input": 0.15},
      "item": { 
            "proportion": {
              "name": 0.4
            },
            "color": "#605b5b",
            "border": { "color": "#00000000" },
            "name": {
              "color": "#00000000",
              "text": {"color": "#e5e2e2"},
              "border": {"color": "#00000000"}
            },
            "value": {
              "color": "#ffffff",
              "border": {"color": "#b9e5e2e2"},
              "text": {"color": "black"}
            }
      }
    },
    
    "instructions": {
        "color": "yellow",
        "proportion": {"header": 0.33, "textHeight": 0.05, "control": 0.1}
    }
}
'''

import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtQuick import QQuickView
from robot.testdoc import TestSuiteFactory
from testexecutor.model.TreeSelectorModel import TreeSelectorModel, TreeItem
from testexecutor.ui import __file__ as uifiles

TAGS = "Tags"
SUITES = "Suites"
filters = {SUITES: [], TAGS: []}


def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)


def set_controller_data(controller, includes=[]):
    """

    :param controller:
    :param includes: Array of case insensitive tags to include. use AND OR etc like usbANDport as necessary.
    :return:
    """
    suites = controller.testselector
    current_path = os.path.dirname(os.path.abspath(__file__))
    #test_path = os.path.join(current_path, '..', 'test', 'dummy')
    test_path = current_path
    tests = test_path
    variables = ["dummyvar:true"]

    suitestructure = parse(tests,
                           variable=variables,
                           include=includes
                           )
    suites.clear()
    tags = []
    if len(suitestructure.tests) > 0:
        print(suitestructure.name)
        for test in suitestructure.tests:
            data = [test.name, test.doc]
            suites.appendChild(data)
            print(test.name)
    else:
        for suite in suitestructure.suites:
            print(suite.name)
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
    return tags


if __name__ == "__main__":
    import testexecutor as te
    controller = None

    def selectionFilterChanged(name, selected):
        print("selectionFilterChanged", name, selected.getItems())
        if name == TAGS:
            set_controller_data(controller, selected.getItems())

    mySuiteGroup = TestSuiteGroup()
    suite = SampleTestSuiteWrapper("Diagnostics")
    controller = TestSuiteControlModel(filtercallback=selectionFilterChanged, filters=filters)
    controller.testselector = TreeSelectorModel()
    tags = set_controller_data(controller)
    controller.filters.updateData(TAGS, tags)
    suite.controller = controller
    mySuiteGroup.addData(suite)

    # messy style: material
    # workable styles: fusion, imagine, universal
    #import sys
    #sys.argv += ['--style', 'fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Controller (TE {0})".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())
