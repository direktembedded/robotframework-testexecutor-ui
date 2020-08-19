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
      "identification": 0.1,
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
      "proportion": {"input": 0.4},
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

# TODO continue to make default behaviour for id list
id_config = {
    "class": {
        "DefaultIdentification": {
            "module": "",
            "init_values": [
                {
                    "device": {
                        "name": "Device"
                    }
                },
                {
                    "serial": {
                        "name": "Serial No"
                    }
                },
                {
                    "model": {
                        "name": "Model",
                        "possibles": ["Simple", "Another", "Super SKU"]
                    }
                }
            ]
        }
    }
}


if __name__ == "__main__":
    import testexecutor as te

    # TODO, handle with command line argument
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, 'suites')

    mySuiteGroup = TestSuiteGroup()
    #suite = SampleTestSuiteWrapper("Diagnostics")
    suite = TestExecutorController("Test Suite", testpath=test_path, useselector=True)
    mySuiteGroup.addData(suite)

    # messy style: material
    # workable styles: fusion, imagine, universal
    #import sys
    #sys.argv += ['--style', 'fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Controller (TE {0})".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())
