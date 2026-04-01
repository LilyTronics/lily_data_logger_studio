"""
Logger.
"""

import os
import sys

from datetime import datetime


class Logger:

    TYPE_INFO = "INFO"
    TYPE_DEBUG = "DEBUG"
    TYPE_ERROR = "ERROR"
    TYPE_STDOUT = "STDOUT"
    TYPE_STDERR = "STDERR"
    TYPE_EMPTY = "EMPTY"

    _TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    _LOG_FORMAT = "{} | {:6} | {}\n"

    class _StdLogger:

        def __init__(self, logger, std_type):
            self._logger = logger
            self._type = std_type

        def write(self, message):
            self._logger.handle_message(self._type, message)

        def flush(self):
            pass

    def __init__(self, filename, log_to_stdout=False, redirect_stdout=True):
        self._filename = filename
        path = os.path.dirname(self._filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        self._log_to_stdout = log_to_stdout
        with open(self._filename, "w", encoding="utf-8") as fp:
            fp.close()
        self._output = ""
        self._stdout_callback = None

        self._org_stdout = sys.stdout
        self._org_stderr = sys.stderr
        if redirect_stdout:
            sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
            sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    def shut_down(self):
        sys.stdout = self._org_stdout
        sys.stderr = self._org_stderr

    def set_stdout_callback(self, callback):
        self._stdout_callback = callback

    def info(self, message):
        self.handle_message(self.TYPE_INFO, f"{message}\n")

    def debug(self, message):
        self.handle_message(self.TYPE_DEBUG, f"{message}\n")

    def error(self, message):
        self.handle_message(self.TYPE_ERROR, f"{message}\n")

    def empty_line(self):
        self.handle_message(self.TYPE_EMPTY, "\n")

    def handle_message(self, message_type, message_text):
        timestamp = datetime.now().strftime(self._TIME_STAMP_FORMAT)[:-3]
        self._output += message_text
        while "\n" in self._output:
            index = self._output.find("\n")
            message = self._output[:index]
            self._output = self._output[index + 1:]
            if message_type == self.TYPE_EMPTY:
                message = "\n"
            else:
                message = self._LOG_FORMAT.format(timestamp, message_type, message)
            if message_type in [self.TYPE_STDOUT, self.TYPE_STDERR] and \
                self._stdout_callback is not None:
                # Only log STDOUT and STDERR messages to the callback
                self._stdout_callback(message)
            else:
                with open(self._filename, "a", encoding="utf-8") as fp:
                    fp.write(message)
                if self._log_to_stdout:
                    self._org_stdout.write(message)


if __name__ == "__main__":

    from tests.unit_tests.model_tests.logger_test import LoggerTest

    LoggerTest().run()
