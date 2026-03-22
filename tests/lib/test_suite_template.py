"""
Template for a test suite
"""

from tests.lib.test_suite import TestSuite


class TestSuiteTest(TestSuite):

    def test_something(self):
        pass


if __name__ == "__main__":

    TestSuiteTest().run()
