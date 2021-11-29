# coding=utf-8
"""
Test module to kick off text-executor gui with controller/test selector enabled, so different tests can be run.
execute as python3 <filename.py>

Copyright (c) 2020- Sipke Vriend, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""

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
