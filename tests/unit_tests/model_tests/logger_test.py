"""
Unit test for the logger.
"""

import src.app_data as AppData

from src.models.logger import Logger

from tests.lib.test_suite import TestSuite


class LoggerTest(TestSuite):

    _TEST_MESSAGES = [
        ("info", "This is an info message"),
        ("debug", "This is a debug message"),
        ("error", "This is a error message"),
        ("stdout", "This is a standard output message"),
        ("info", "This is a\nmulti line message"),
    ]
    _logger = None

    def setup(self):
        self._logger = Logger(AppData.APP_LOG_FILE)

    def teardown(self):
        self._logger.shut_down()

    def test_log_file_empty(self):
        filename = AppData.APP_LOG_FILE
        with open(filename, "r", encoding="utf-8") as fp:
            content = fp.read().strip()
        self.fail_if(content != "", "The log file is not empty")

    def test_logger(self):
        for message in self._TEST_MESSAGES:
            if message[0] == "info":
                self._logger.info(message[1])
            elif message[0] == "debug":
                self._logger.debug(message[1])
            elif message[0] == "error":
                self._logger.error(message[1])
            elif message[0] == "stdout":
                print(message[1])

        filename = AppData.APP_LOG_FILE
        with open(filename, "r", encoding="utf-8") as fp:
            lines = list(map(lambda x: x.rstrip(), fp.readlines()))
        self.fail_if(len(lines) == 0, "The log file is empty")

        for message in self._TEST_MESSAGES:
            # Split up multi line messages
            parts = message[1].split("\n")
            n_found = 0
            for part in parts:
                for line in lines:
                    if line.endswith(f"| {part}") and f"| {message[0].upper():6} |" in line:
                        n_found += 1
            if n_found != len(parts):
                self.fail(f"Message '{message}' not found in the log file")

    def test_exception(self):
        def _generate_error():
            _ = 1 / 0

        # Clear the file
        filename = AppData.APP_LOG_FILE
        with open(filename, "w", encoding="utf-8") as fp:
            fp.close()
        # To prevent this from failing, we generate an error in a thread
        t = self.start_thread(_generate_error)
        while t.is_alive():
            pass

        with open(filename, "r", encoding="utf-8") as fp:
            lines = list(map(lambda x: x.rstrip(), fp.readlines()))
        self.fail_if(len(lines) == 0, "The log file is empty")
        self.fail_if(len(lines) < 4, "The log file has less than 4 lines")

        for line in lines:
            self.fail_if("| STDERR |" not in line, f"Message is not type STDERR '{line}'")

        self.fail_if("| STDERR | Exception in thread Thread" not in lines[0],
                     f"First line does not match with the exception message '{lines[0]}'")

        self.fail_if("| STDERR | Traceback (most recent call last):" not in lines[1],
                     f"Second line does not match with the traceback message '{lines[1]}'")

        self.fail_if("| STDERR | ZeroDivisionError: division by zero" not in lines[-1],
                     f"Last line does not match with the division by zero message '{lines[-1]}'")


if __name__ == "__main__":

    LoggerTest().run(True)
