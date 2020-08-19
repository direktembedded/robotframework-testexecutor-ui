#
# A suite with large number of dummy tests to demonstrate a long test run and Tag filtering for robot-testexecutor
#

*** Settings ***
Documentation    A suite of tests with tagged tests
# The caller must ensure CUSTOMDIALOGS variable is set. e.g. CUSTOMDIALOGS:ListenerDialogs
Library          ${CUSTOMDIALOGS}
# We only need to provide the default Dialogs library if our CUSTOMDIALOGS library does not provide all keywords
Library          Dialogs
Suite Setup      Run Keywords   Set Library Search Order    ${CUSTOMDIALOGS}  Dialogs  AND
...                             Set Log Level  INFO

*** Test Cases ***
Network Test A
    [Tags]    Network
    Log    Network found

Network Test B
    [Tags]    Network
    Log    Network found

Network Test C
    [Tags]    Network
    Log    Network found

CPU Test A
    [Tags]    CPU
    Log    CPU works

CPU Test B
    [Tags]    CPU
    Log    CPU works

CPU Test C
    [Tags]    CPU
    Log    CPU works

CPU Test D
    [Tags]    CPU
    Log    CPU works

USB Test A
    [Tags]    USB
    [Documentation]  A USB Test we give the name A
    Log    USB port works

USB Test B
    [Tags]    USB
    [Documentation]  A USB Test we give the name B
    Log    USB port works

USB and Port Test A
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name A
    Log    USB and Port works

USB and Port Test B
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name B
    Log    USB and Port works

USB and Port Test C
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name C
    Log    USB and Port works

USB and Port Test D
    [Tags]    USB  Port
    [Documentation]  A USB and Port Test we give the name D
    Log    USB port works

Port Test A
    [Tags]    Port
    [Documentation]  A Port Test we give the name A
    Log    Port works

Port Test B
    [Tags]    Port
    [Documentation]  A Port Test we give the name B
    Log    Port works

Port Test C
    [Tags]    Port
    [Documentation]  A Port Test we give the name C
    Log    Port works
