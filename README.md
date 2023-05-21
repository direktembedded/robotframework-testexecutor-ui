# Robot Framework wrapper for Test Executor&trade;

This module provides is a library which provides a test runner using [Robot Framework](https://robotframework.org/) and controller using Test Executor&trade;. [TestArchiver](https://github.com/salabs/TestArchiver) ArchiverRobotListener can be used to archive the test results.

[Test Executor&trade;](https://direktembedded.com) is a generic python UI library for the execution, monitoring and control of python based tests on a device/system.

## Config
Test variables are configured using device identifiers, with the config/DefaulIdentification module provided as a sample which should cover most requirements, but this can be replaced with more complex scenarios.

If archiving via ArchiverRobotListener is to be used a TestArchiver database config file is provided.

Test Executor&trade; is setup by passing in the testexecutor.model.TestSuiteGroup() which defines the robot controllers the UI will load. 


## Framework
Robot Framework instances run as processes each communicating with a Test Executor proxy. 

Robot Framework run() method is executed from the UI and passed configured variables for access by tests.

Copyright &copy; 2022 Direkt Embedded Pty Ltd
 
https://www.direktembedded.com