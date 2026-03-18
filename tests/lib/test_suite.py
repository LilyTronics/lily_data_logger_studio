"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import lily_unit_test


class TestSuite(lily_unit_test.TestSuite):

    # Works as the application logger for objects needing a logger
    class _TestLogger():
        def __init__(self, logger):
            self._logger = logger

        def debug(self, message):
            self._logger.debug(f"(test logger) {message}")

    def __init__(self, *args):
        super().__init__(*args)
        self.app_test_logger = self._TestLogger(self.log)


if __name__ == "__main__":

    ts = TestSuite()
