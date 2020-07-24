from testexecutor.model.TestSuiteGroup import TestSuiteGroup
from testexecutor.model.MultiTestWindowModel import MultiTestWindowModel
from robottestexecutor.TestExecutorController import TestExecutorController

config = '''{
    "states": {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}}
    },

    "proportion": {
      "title": 0.1,
      "identification": 0.07,
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
      "proportion": {"input": 0.5},
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

    mySuiteGroup = TestSuiteGroup()
    mySuiteGroup.addData(TestExecutorController("Station 1", exampletest="MisspelledSuite.robot"))
    mySuiteGroup.addData(TestExecutorController("Station 2", exampletest="CustomDialogsVerificationSuite.robot"))
    mySuiteGroup.addData(TestExecutorController("Station 3", exampletest="FeedbackVerificationSuite.robot"))

    # messy style: material
    # workable styles: fusion, imagine, universal
    #sys.argv += ['--style', 'fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Multiple Runner (TE {0})".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())

'''
import sys, os
from robot import run
from robottestexecutor.TestExecutorController import TestExecutorController



def run_example(test_path):
    """
    Kick off the robot example test run
    :param test_path: name of a robot file to execute
    :return: None
    """
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, path)
    run(test_path, listener=TestExecutorController(), variable="TESTEXECUTORDIALOGS:robottestexecutor.TestExecutorDialogs")



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please supply robot script name as argument")

    run_example(sys.argv[1])
'''