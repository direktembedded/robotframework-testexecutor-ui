#
# To execute run
#   python.exe ProgrammaticListenerExample.py TestRobotCustomDialogs.robot
# Note there is a close tie between listener and the custom dialog
#

*** Settings ***
Documentation    A test to check how to integrate a robot listener and dialogs
# The caller must ensure CUSTOMDIALOGS variable is set. e.g. CUSTOMDIALOGS:ListenerDialogs
Library          ${CUSTOMDIALOGS}
# We only need to provide the default Dialogs library if our CUSTOMDIALOGS library does not provide all keywords
Library          Dialogs
Suite Setup      Run Keywords   Set Library Search Order    ${CUSTOMDIALOGS}  Dialogs  AND
...                             Set Log Level  INFO

*** Test Cases ***
Forced Fail
    Should Be Equal    Force  A Fail

Forced Fail Custom
    Should Be Equal    Force  A Fail  Custom error message  values=False

Forced Fail Both
    Should Be Equal    Force  A Fail  Custom error message

Verify Device ID
    Should Be Equal    ${devicekey}   12345   Invalid device

Force Internal Error
    An Unknown Keyword

*** Keywords ***

