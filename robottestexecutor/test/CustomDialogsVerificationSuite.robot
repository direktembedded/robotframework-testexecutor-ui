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
Verify Custom Dialogs Library
    [Tags]    DEBUG
    Set Log Level  INFO
    Feedback  A feedback keyword from a custom Dialogs Library
    Pause Execution            Robot "Pause Execution" Key Word redirected to TestExecutor\nvia Custom Dialogs Library
    Log    Now we will verify the Execute Manual Step key word
    Execute Manual Step  Is it a full moon?\nPlease press yes to pass
    Execute Manual Step  Is it a full moon?\nPlease press no to fail    The moon was not full, fail the test

Verify Second Time
    [Tags]    DEBUG
    Log   Another Log keyword from the listener
    Pause Execution            Another example skips the pausing of execution

Verify Once More
    [Tags]    DEBUG
    Log    Something else
    Pause Execution            Final example skips the pausing of execution
#    ${user} =     Get Selection From User    Select user  one  two  three
#    Log    ${user}
#    ${users} =    Get Selections From User   Select multiple users  one  two  three
#    Log    ${users}
#    ${value} =    Get Value From User        Please enter a value
#    Execute Manual Step        Please select pass
#    Execute Manual Step        Please select fail

*** Keywords ***

