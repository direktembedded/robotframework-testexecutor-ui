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
    Log                This test waits a little and then forces a fail
    Sleep              3
    Should Be Equal    Force  A Fail

Forced Fail Custom
    Log                This test waits a little and then forces a fail with a custom message, but no values
    Sleep              3
    Should Be Equal    Force  A Fail  Custom error message  values=False

Forced Fail Both
    Log                This test waits a little and then forces a fail with a custom message and failed values
    Sleep              3
    Should Be Equal    Force  A Fail  Custom error message

Verify Device ID
    Log                This test waits a little and then verifies if your device id value is ${expected_key}
    Sleep              3
    Should Be Equal    ${devicekey}   12345   Invalid device

Force Internal Error
    An Unknown Keyword

*** Keywords ***

*** Variables ***
${expected_key}  12345