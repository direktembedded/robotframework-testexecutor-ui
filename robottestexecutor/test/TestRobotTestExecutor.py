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
    # An example postgresql config file is also provided but requires server access to work.
    #db_file = os.path.join(current_path, "testarchiver_postgre_db_config.json")
    db_file = os.path.join(current_path, "testarchiver_sqlite_db_config.json")
    mySuiteGroup = TestSuiteGroup()
    mySuiteGroup.addData(TestExecutorController("Station 1", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 2", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 3", db_config_file=db_file))
    mySuiteGroup.addData(TestExecutorController("Station 4", db_config_file=db_file))

    # messy style: material
    # workable styles: fusion, imagine, universal
    #sys.argv += ['--style', 'fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Sample Multiple Runner (TE {0})".format(te.__version__))
    windowModel.config = config

    exit(windowModel.exec())
