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
import os

config = '''{
    "states": {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}}
    },

    "proportion": {
      "title": 0.1,
      "identification": 0.13,
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
      "proportion": {"input": 0.28},
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
    },
    
    "controller": {
        "proportion": {
          "indicator": 0.02,
          "name": 0.15,
          "count": 0.03
        },
        "header": {
            "color": {"default": "lightgray"},
            "text": {"color": "green"},
            "name": "Test",
            "description": "Description"
        },
        "section": {
            "color": {"default": "#8e8a8a", "selected": "goldenrod"},
            "text": {"color": {"default": "black"}},
            "border": {"color": "lightgray", "width": 1},
            "dimension": {"height": 25}
        },
        "row": {
            "color": {"default": "snow", "alternate": "whitesmoke", "selected": "burlywood"},
            "text": {"color": {"default": "black"}}
        },
        "indicators": {"0":"⮞", "1":"⮟"},
        "viewableCount": 25,
        "filter": {
            "item": {
                "list": {
                    "background": {"color": "lightgray"},
                    "border": {"color": "green"}
                },
                "item": {                
                    "background": {"color": "white"},
                    "border": {"color": "green"},
                    "button": {
                        "gradient": {"start": {"off": "darkgreen", "pressed": "white"},
                                     "end": {"off": "white", "pressed": "goldenrod"}} 
                    }
                }
            }
        }
    }    
}
'''

if __name__ == "__main__":
    import testexecutor as te

    # TODO, handle with command line argument
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, 'suites')

    mySuiteGroup = TestSuiteGroup()
    #suite = SampleTestSuiteWrapper("Diagnostics")
    # TODO when moving to application need to catch ValidationError and report nicely to user on command line
    suite = TestExecutorController("Test Suite", useselector=True, testpath=test_path)
    mySuiteGroup.addData(suite)

    # messy style: material
    # workable styles: Fusion, imagine, universal
    import sys
    sys.argv += ['--style', 'Fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Controller".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())
