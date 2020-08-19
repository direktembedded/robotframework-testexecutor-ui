#
# A test suite used to demonstrate robot-testexecutor's Dialogs library to UI usage.
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
Manual Step
    [Tags]    Dialogs
    Pause Execution      This test will ask you to manually pass and then fail a test
    Execute Manual Step  Is it a full moon?\nPlease press Yes to pass
    Execute Manual Step  Is it not full moon?\nPlease press Yes to pass or No to fail    The moon was not full, fail the test

Log Destination
    [Tags]    Dialogs
    Log To Suite
    Log                  Change Logs to go to suite instruction window and then to test result feedback
    Sleep                2
    Log To Test
    Log                  This logs to the test result feedback window
    Sleep                2
    FOR                  ${progress}  IN  10  20  30  40  50  100
        Sleep            0.5
        Log              ${progress}
    END

Pausing Test
    [Tags]    Dialogs
    Log To Both
    Pause Execution      Please press the button to complete this test
    Log                  This test just paused and waited for you to press a button

# Dialogs methods not implemented yet
#    ${user} =     Get Selection From User    Select user  one  two  three
#    Log    ${user}
#    ${users} =    Get Selections From User   Select multiple users  one  two  three
#    Log    ${users}
#    ${value} =    Get Value From User        Please enter a value

*** Keywords ***

