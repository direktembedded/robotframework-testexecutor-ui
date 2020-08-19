#
# A suite with large number of dummy tests to demonstrate a long test run and Tag filtering for robot-testexecutor
#

*** Settings ***
Documentation    A test suite with larger number of tagged tests
# The caller must ensure CUSTOMDIALOGS variable is set. e.g. CUSTOMDIALOGS:ListenerDialogs
Library          ${CUSTOMDIALOGS}
# We only need to provide the default Dialogs library if our CUSTOMDIALOGS library does not provide all keywords
Library          Dialogs
Suite Setup      Run Keywords   Set Library Search Order    ${CUSTOMDIALOGS}  Dialogs  AND
...                             Set Log Level  INFO

*** Test Cases ***
Network Test 1
    [Tags]    Network
    Log    Network found

Network Test 2
    [Tags]    Network
    Log    Network found

Network Test 3
    [Tags]    Network
    Log    Network found

Network Test 4
    [Tags]    Network
    Log    Network found

Network Test 5
    [Tags]    Network
    Log    Network found

Network Test 6
    [Tags]    Network
    Log    Network found

Network Test 7
    [Tags]    Network
    Log    Network found

Network Test 8
    [Tags]    Network
    Log    Network found

Network Test 9
    [Tags]    Network
    Log    Network found

Network Test 10
    [Tags]    Network
    Log    Network found

CPU Test 1
    [Tags]    CPU
    Log    CPU works

CPU Test 2
    [Tags]    CPU
    Log    CPU works

CPU Test 3
    [Tags]    CPU
    Log    CPU works

CPU Test 4
    [Tags]    CPU
    Log    CPU works

CPU Test 5
    [Tags]    CPU
    Log    CPU works

CPU Test 6
    [Tags]    CPU
    Log    CPU works

CPU Test 7
    [Tags]    CPU
    Log    CPU works

CPU Test 8
    [Tags]    CPU
    Log    CPU works

CPU Test 9
    [Tags]    CPU
    Log    CPU works

CPU Test 10
    [Tags]    CPU
    Log    CPU works

CPU Test 11
    [Tags]    CPU
    Log    CPU works

CPU Test 12
    [Tags]    CPU
    Log    CPU works

CPU Test 13
    [Tags]    CPU
    Log    CPU works

CPU Test 14
    [Tags]    CPU
    Log    CPU works

USB Test 1
    [Tags]    USB
    Log    USB port works

USB Test 2
    [Tags]    USB
    Log    USB port works

USB Test 3
    [Tags]    USB
    Log    USB port works

USB Test 4
    [Tags]    USB
    Log    USB port works

USB and Port Test 5
    [Tags]    USB  Port
    Log    USB and Port works

USB and Port Test 6
    [Tags]    USB  Port
    Log    USB and port works

USB and Port Test 7
    [Tags]    USB  Port
    Log    USB and port works

USB and Port Test 8
    [Tags]    USB  Port
    Log    USB and port works

USB and Port Test 9
    [Tags]    USB  Port
    Log    USB and port works

Port Test 1
    [Tags]    Port
    Log    USB and port works

Port Test 2
    [Tags]    Port
    Log    USB and port works

Port Test 3
    [Tags]    Port
    Log    USB and port works

Port Test 4
    [Tags]    Port
    Log    USB and port works

Port Test 5
    [Tags]    Port
    Log    USB and port works

Port Test 6
    [Tags]    Port
    Log    USB and port works

Port Test 7
    [Tags]    Port
    Log    USB and port works

Port Test 8
    [Tags]    Port
    Log    USB and port works

Port Test 9
    [Tags]    Port
    Log    USB and port works

Port Test 10
    [Tags]    Port
    Log    USB and port works

Port Test 11
    [Tags]    Port
    Log    USB and port works

Port Test 12
    [Tags]    Port
    Log    USB and port works

Port Test 13
    [Tags]    Port
    Log    USB and port works

Port Test 14
    [Tags]    Port
    Log    USB and port works

Port Test 15
    [Tags]    Port
    Log    USB and port works

Port Test 16
    [Tags]    Port
    Log    USB and port works

Port Test 17
    [Tags]    Port
    Log    USB and port works

Port Test 18
    [Tags]    Port
    Log    USB and port works

Port Test 19
    [Tags]    Port
    Log    USB and port works

Port Test 20
    [Tags]    Port
    Log    USB and port works

Port Test 21
    [Tags]    Port
    Log    USB and port works

Port Test 22
    [Tags]    Port
    Log    USB and port works

Port Test 23
    [Tags]    Port
    Log    USB and port works

Port Test 24
    [Tags]    Port
    Log    USB and port works

Port Test 25
    [Tags]    Port
    Log    USB and port works

Port Test 26
    [Tags]    Port
    Log    USB and port works

Port Test 27
    [Tags]    Port
    Log    USB and port works

