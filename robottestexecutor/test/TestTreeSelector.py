"""
A Test file for testing the display of robot tests parsed using robot.testdoc.TestSuiteFactory into a tree structure.
Utilises the tree selector model from testexecutor.

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtQuick import QQuickView
from robot.testdoc import TestSuiteFactory
from testexecutor.model.TreeSelectorModel import TreeSelectorModel, TreeItem
from testexecutor.ui import __file__ as uifiles

def parse(*tests, **options):
    return TestSuiteFactory(*tests, **options)


def set_suite_data(parent):
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, '..', 'test')

    tests = test_path
    variables = ["dummyvar:true"]
    includes = ["usb", "Port"]  # Case insensitive. use AND OR etc like usbANDport as necessary.
    suitestructure = parse(tests,
                           variable=variables,
                           include=includes
                           )
    tags = []
    if len(suitestructure.tests) > 0:
        print(suitestructure.name)
        for test in suitestructure.tests:
            data = [test.name, test.doc]
            parent.rootItem.appendChild(TreeItem(data, parent))
            print(test.name)
    else:
        for suite in suitestructure.suites:
            print(suite.name)
            data = (suite.name, suite.doc)
            newparent = TreeItem(data, parent.rootItem)
            parent.rootItem.appendChild(newparent)
            for test in suite.tests:
                print(test.name)
                data = [test.name, test.doc]
                newparent.appendChild(TreeItem(data, newparent))
                for tag in test.tags:
                    if tag not in tags:
                        tags.append(tag)
    print("Tags", tags)


if __name__ == '__main__':

    import sys
    import os

    model = TreeSelectorModel()
    set_suite_data(model)
    app = QApplication(sys.argv)
    #current_path = os.path.dirname(sys.argv[0]) #os.path.abspath(os.path.dirname(__file__))
    current_path = os.path.dirname(uifiles)
    ui_path = os.path.join(current_path, '')
    qml_file = os.path.join(ui_path, 'TreeSelector.qml')
    url = QUrl.fromLocalFile(qml_file)

    view = QQuickView()
    view.rootContext().setContextProperty("theModel", model)
    view.setSource(url)
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    if view.status() == QQuickView.Error:
        oops = view.errors()
        print(oops)
        import sys
        sys.exit(-1)
    else:
        #view.rootContext().setContextProperty("theModel", model)
        view.show()
        view.rootContext().setContextProperty("theModel", model)
    app.exec_()
