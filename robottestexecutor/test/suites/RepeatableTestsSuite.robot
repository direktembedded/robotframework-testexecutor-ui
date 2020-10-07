#
# A suite to demonstrate use of Test Template to have all test steps repeatable
#
*** Settings ***
Library          robottestexecutor.proxy.TestExecutorDialogs
Test Template    User Repeat On Fail

*** Test Cases ***
Multiple Test Steps
    Pause Execution        This is the first test step which does not fail
    Execute Manual Step    Click No, to fail this FIRST step and you will be asked if you want to repeat it.\nClick Yes to repeat, then Yes to pass the test    FIRST Manual Step Failed
    Execute Manual Step    Click Yes, to pass this SECOND step immediately   SECOND Manual Step Failed
    Pause Execution        If you are here, you passed all test, congradulations.

Single Test Step with Composed Test
    Multiple Keywords    This test has the same steps as Multiple Test Steps, but not every step is repeatable

*** Keywords ***
Multiple Keywords
    [Arguments]  ${message}
    Pause Execution        ${message}
    Execute Manual Step    Click Yes, to immediately pass this INITIAL step    INITIAL Manual Step Failed
    Execute Manual Step    Click No, to fail this SECONDARY step and you will be asked if you want to repeat all steps.\nClick Yes to repeat and you will notice the INITIAL steps happen again.\nClick Yes to all after this to pass all.    SECONDARY Manual Step Failed
    Pause Execution        If you are here, you passed all previous test, congradulations.

*** Variables ***
${user_repeat_on_fail_count}  3