# coding=utf-8
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

from testexecutor.model.TestSuiteGroup import TestSuiteGroup
from testexecutor.model.MultiTestWindowModel import MultiTestWindowModel
from robottestexecutor.control.TestExecutorController import TestExecutorController

config = '''{
    "states": {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}}
    },

    "proportion": {
      "title": 0.1,
      "identification": 0.12,
      "instructions": 0.4,
      "status": 0.04
    },

    "results": {
      "viewableCount": 15,
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
      "proportion": {"input": 0.25},
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
        "proportion": {"header": 0.1, "textHeight": 0.05, "control": 0.1}
    }
}
'''

if __name__ == "__main__":
    import testexecutor as te
    import os

    current_path = os.path.dirname(os.path.abspath(__file__))

    # sqlite database is the default and will create a robot_te_results.db database.
    # Note only one test should be run at a time with sqlite, multiple connections will cause errors in the
    # test archiver robot listener.
    # An example postgresql config file is also provided but requires server access to work.
    db_file = os.path.join(current_path, "testarchiver_postgre_db_config.json")
    #db_file = os.path.join(current_path, "testarchiver_sqlite_db_config.json")
    mySuiteGroup = TestSuiteGroup()
    mySuiteGroup.addData(TestExecutorController("Station 1", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 2", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 3", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 4", db_config_file=db_file))

    # messy style: material
    # workable styles: fusion, imagine, universal
    import sys
    sys.argv += ['--style', 'Fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Multiple Runner (TE {0})".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())
