from robot.api import SuiteVisitor


class TestExecutorSuitePreRunModifier(SuiteVisitor):

    def visit_test(self, test):
        super().visit_test(test)