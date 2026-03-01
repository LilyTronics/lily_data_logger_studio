"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import lily_unit_test


class TestSuite(lily_unit_test.TestSuite):

    def __init__(self, *args):
        super().__init__(*args)


if __name__ == "__main__":

    ts = TestSuite()
