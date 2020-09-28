#
# A test suite used for Default Identification's ModelA demonstration.
# See config/IdentificationConfig.py
#

*** Settings ***
Documentation    A test to check how to integrate a robot listener and dialogs
# The caller must ensure CUSTOMDIALOGS variable is set. e.g. CUSTOMDIALOGS:ListenerDialogs
Library          ${CUSTOMDIALOGS}
# We only need to provide the default Dialogs library if our CUSTOMDIALOGS library does not provide all keywords
Library          Dialogs
Suite Setup      Set Library Search Order    ${CUSTOMDIALOGS}  Dialogs

*** Test Cases ***
Manual Step Test Case
    [Tags]    Dialogs
    Pause Execution      This test will ask you to manually pass and then fail a test
    Execute Manual Step  Is it a full moon?\nPlease press Yes to pass
    Execute Manual Step  Is it not full moon?\nPlease press Yes to pass or No to fail    The moon was not full, fail the test

Test With Logging
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

Test With Instruction
    [Tags]    Dialogs
    Log To Both
    Pause Execution      Please press the button to complete this test
    Log                  This test just paused and waited for you to press a button

Slow Network Test A
    [Tags]    Network
    Sleep  10
    Log    Network found

Slow Network Test B
    [Tags]    Network
    Sleep  3
    Log    Network found

Slow Network Test C
    [Tags]    Network
    Sleep  10
    Log    Network found

Slow CPU Test A
    [Tags]    CPU
    Sleep  3
    Log    CPU works

Slow CPU Test B
    [Tags]    CPU
    Sleep  5
    Log    CPU works

Slow CPU Test C
    [Tags]    CPU
    Sleep  4
    Log    CPU works

Slow CPU Test D
    [Tags]    CPU
    Sleep  10
    Log    CPU works

Slow USB Test A
    [Tags]    USB
    [Documentation]  A USB Test we give the name A
    Sleep  6
    Log    USB port works

Slow USB Test B
    [Tags]    USB
    [Documentation]  A USB Test we give the name B
    Sleep  3
    Log    USB port works

Slow Port Test A
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name A
    Sleep  4
    Log    USB and Port works

Slow Port Test B
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name B
    Sleep  7
    Log    USB and Port works

*** Keywords ***

